---
description: At the end of the tutorial, you will write a beautiful bot that will be able to accept payments for your product directly in TON.
---

# Bot for sales of dumplings

In this article, we'll create a simple Telegram bot for accepting payments in TON.

## 🦄 What it looks like

At the end of the tutorial, you will write a beautiful bot that will be able to accept payments for your product directly in TON.

The bot will look like this:

![bot preview](/img/tutorials/js-bot-preview.jpg)

## 📖 What you'll learn
You'll learn how to:
 - Create a Telegram bot in NodeJS using Grammy
 - Work with public TON Center API

> Why do we use Grammy?
Because Grammy is a modern, young, high-level framework for comfortable & fast development of telegram bots on JS/TS/Deno, in addition to this Grammy has great [documentation](https://grammy.dev) and an active community that can always help you.


## ✍️ What you need to get started
Install [NodeJS](https://nodejs.org/en/download/) if you haven't yet.

Also you need these libraries:
 - grammy
 - ton
 - dotenv

You can install them with one command in the terminal.
```bash npm2yarn
npm install ton dotenv grammy @grammyjs/conversations
```

## 🚀 Let's get started!
The structure of our project will look like this:
```
src
    ├── bot
        ├── start.js
        ├── payment.js
    ├── services 
        ├── ton.js
    ├── app.js
.env
```
* `bot/start.js` & `bot/payment.js` - files with handlers for telegram bot
* `src/ton.js` - file with business logic related to TON
* `app.js` - file for initializing and launching the bot


Now let's begin writing code!

## Config
Let's start with `.env`. We just need to set a few parameters in it.

**.env**
```
BOT_TOKEN=
TONCENTER_TOKEN=
NETWORK=
OWNER_WALLET= 
```

Here you need to fill in the values in the first four lines:
 - `BOT_TOKEN` is your Telegram Bot token which you can get after [creating a bot](https://t.me/BotFather).
 - `OWNER_WALLET` is your project's wallet address which will accept all payments. You can just create a new TON wallet and copy its address.
 - `API_KEY` is your API key from TON Center which you can get from [@tonapibot](https://t.me/tonapibot)/[@tontestnetapibot](https://t.me/tontestnetapibot) for the mainnet and testnet, respectively.
 - `NETWORK` is about on what network your bot will run - testnet or mainnet

That's all for the config file, so we can move forward!

## TON Center API
In the `src/services/ton.py` file we'll declare a functions to verify the existence of a transaction and generate links for a quick transition to the wallet application for payment

### Getting the latest wallet transactions

Our task is to check the availability of the transaction we need from a certain wallet. 

We will solve it like this:
1. We will receive the last transactions that were received to our wallet. Why ours? In this case, we do not have to worry about what the user's wallet address is, we do not have to confirm that it is his wallet, we do not have to store this wallet anywhere.
2. Sort and leave only incoming transactions 
3. Let's go through all the transactions, and each time we will check whether the comment and the amount are equal to the data that we have  
4. celebrating the solution of our problem🎉

#### Getting the latest transactions

If we use the TON Center API, then we can refer to their [documentation](https://toncenter.com/api/v2/) and find a method that ideally solves our problem - [getTransactions](https://toncenter.com/api/v2/#/accounts/get_transactions_getTransactions_get)

One parameter is enough for us to get transactions - the wallet address for accepting payments, but we will also use the limit parameter in order to limit the issuance of transactions to 100 pieces.

Let's try to call a test request for the `EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N` address (by the way, this is the TON Foundation address)
```bash
curl -X 'GET' \
  'https://toncenter.com/api/v2/getTransactions?address=EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N&limit=100' \
  -H 'accept: application/json'
```
Great, now we have a list of transactions on hand in ["result"], now let's take a closer look at 1 transaction


```json
{
      "@type": "raw.transaction",
      "utime": 1667148685,
      "data": "*data here*",
      "transaction_id": {
        "@type": "internal.transactionId",
        "lt": "32450206000003",
        "hash": "rBHOq/T3SoqWta8IXL8THxYqTi2tOkBB8+9NK0uKWok="
      },
      "fee": "106508",
      "storage_fee": "6508",
      "other_fee": "100000",
      "in_msg": {
        "@type": "raw.message",
        "source": "EQA0i8-CdGnF_DhUHHf92R1ONH6sIA9vLZ_WLcCIhfBBXwtG",
        "destination": "EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N",
        "value": "1000000",
        "fwd_fee": "666672",
        "ihr_fee": "0",
        "created_lt": "32450206000002",
        "body_hash": "Fl+2CzHNgilBE4RKhfysLU8VL8ZxYWciCRDva2E19QQ=",
        "msg_data": {
          "@type": "msg.dataText",
          "text": "aGVsbG8g8J+Riw=="
        },
        "message": "hello 👋"
      },
      "out_msgs": []
    }
```

From this json file, we can understand some information that can be usefull for us:

- This is an incoming transaction, since the "out_msgs" field is empty
- We can also get a comment of the transaction, its sender and the transaction amount

Now we're ready to create a transaction checker

### Work with TON

Let's start by importing the necessary library TON
```js
import { HttpApi, fromNano, toNano } from "ton";
```

Let's think about how to check if the user has sent the transaction we need.

Everything is elementary simple. We can just sort only incoming transactions to our wallet, and then go through the last 100 transactions, and if a transaction is found that has the same comment and amount, then we have found the transaction we need!


Let's start with initializing the http client, for convenient work with TON
```js
export async function verifyTransactionExistance(toWallet, amount, comment) {
  const endpoint =
    process.env.NETWORK === "mainnet"
      ? "https://toncenter.com/api/v2/jsonRPC"
      : "https://testnet.toncenter.com/api/v2/jsonRPC";
  const httpClient = new HttpApi(
    endpoint,
    {},
    { apiKey: process.env.TONCENTER_TOKEN }
  );
```
Here we simply generate the endpoint url based on which network is selected in the config. And after that we initialize the http client.

So, now we can get the last 100 transactions from the owner's wallet
```js
const transactions = await httpClient.getTransactions(toWallet, {
    limit: 100,
  });
```

and filter, leaving only incoming transactions (if the out_msgs of transaction is empty, we leave it)
```js
let incomingTransactions = transactions.filter(
    (tx) => Object.keys(tx.out_msgs).length === 0
  );
```

Now we just have to go through all the transactions, and provided that the comment and the transaction value match, we return true
```js
  for (let i = 0; i < incomingTransactions.length; i++) {
    let tx = incomingTransactions[i];
    // Skip the transaction if there is no comment in it
    if (!tx.in_msg.msg_data.text) {
      continue;
    }

    // Convert transaction value from nano
    let txValue = fromNano(tx.in_msg.value);
    // Get transaction comment
    let txComment = tx.in_msg.message

    if (txComment === comment && txValue === value.toString()) {
      return true;
    }
  }

  return false;
```
Note that value is in nanotons by default, so we need to divide it by 1 billion or we can just use `fromNano` method from the TON library.
And that's all for the `verifyTransactionExistance` function!

Now we can create function to generate link for a quick transition to the wallet application for payment
```js
export function generatePaymentLink(toWallet, amount, comment, app) {
  if (app === "tonhub") {
    return `https://tonhub.com/transfer/${toWallet}?amount=${toNano(
      amount
    )}&text=${comment}`;
  }
  return `https://app.tonkeeper.com/transfer/${toWallet}?amount=${toNano(
    amount
  )}&text=${comment}`;
}
```
All we need is just to substitute the transaction parameters in the URL. Without forgetting to transfer the value of the transaction to nano.


## Telegram bot

### Initialization

Open the `app.js` file and import all the handlers and modules we need.
```js
import dotenv from "dotenv";
import { Bot, session } from "grammy";
import { conversations, createConversation } from "@grammyjs/conversations";

import {
  startPaymentProcess,
  checkTransaction,
} from "./bot/handlers/payment.js";
import handleStart from "./bot/handlers/start.js";
```

Let's set up dotenv module to comfy work with environment variables that we set at .env file 
```js
dotenv.config();
```

After that we create a function that will run our project. In order for our bot not to stop if any errors appear, we add this code
```js
async function runApp() {
  console.log("Starting app...");

  // Handler of all errors, in order to prevent the bot from stopping
  process.on("uncaughtException", function (exception) {
    console.log(exception);
  });
```

Now initialize the bot and the necessary plugins
```js
  // Initialize the bot
  const bot = new Bot(process.env.BOT_TOKEN);

  // Set the initial data of our session
  bot.use(session({ initial: () => ({ amount: 0, comment: "" }) }));
  // Install the conversation plugin
  bot.use(conversations());

  bot.use(createConversation(startPaymentProcess));
```
Here we use `BOT_TOKEN` from our config that we made at the beginning of the tutorial.  

We initialized the bot but it's still empty. We must add some functions for interaction with the user.
```js
  // Register all handelrs
  bot.command("start", handleStart);
  bot.callbackQuery("buy", async (ctx) => {
    await ctx.conversation.enter("startPaymentProcess");
  });
  bot.callbackQuery("check_transaction", checkTransaction);
```
Reacting to the command/start, the handleStart function will be executed. If the user clicks on the button with callback_data equal to "buy", we will start our "conversation", which we registered just above. And when we click on the button with callback_data equal to "check_transaction", we will execute the checkTransaction function.

And all that remains for us is to launch our bot and output a log about a successful launch
```js
  // Start bot
  await bot.init();
  bot.start();
  console.info(`Bot @${bot.botInfo.username} is up and running`);
```

### Message handlers

#### /start Command

Let's begin with the `/start` command handler. This function will be called when the user launches the bot for the first time, restarts it

```js
import { InlineKeyboard } from "grammy";

export default async function handleStart(ctx) {
  const menu = new InlineKeyboard()
    .text("Buy dumplings🥟", "buy")
    .row()
    .url("Article with a detailed explanation of the bot's work", "/develop/dapps/payment-processing/accept-payments-in-a-telegram-bot-js/");

  await ctx.reply(
    `Hello stranger!
Welcome to the best Dumplings Shop in the world <tg-spoiler>and concurrently an example of accepting payments in TON</tg-spoiler>`,
    { reply_markup: menu, parse_mode: "HTML" }
  );
}
```
Here we first import the InlineKeyboard from the grammy module. After that, we create an inline keyboard in the handler with an offer to buy dumplings and a link to this article (a bit of recursion here😁).
.row() stands for the transfer of the next button to a new line.
After that, we send a welcome message with the text (important, I use html markup in my message to decorate it) along with the created keyboard
The welcome message can be anything you want.

#### Payment process

As always, we will start our file with the necessary imports

```js
import { InlineKeyboard } from "grammy";

import {
  generatePaymentLink,
  verifyTransactionExistance,
} from "../../services/ton.js";
```
After that, we will create a startPaymentProcess handler, which we have already registered in the app.js for execution when a certain button is pressed

In the telegram when you click on the inline button a spinning watch appears in order to remove them, we respond to the callback
```js
  await ctx.answerCallbackQuery();
```
After that, we need to send the user a picture of dumplings, ask him to send the number of dumplings that he wants to buy. And we are waiting for him to enter this number
```js
  await ctx.replyWithPhoto(
    "https://telegra.ph/file/bad2fd69547432e16356f.jpg",
    {
      caption:
        "Send the number of portions of yummy dumplings you want buy\nP.S. Current price for 1 portion: 3 TON",
    }
  );

  // Wait until the user enters the number
  const count = await conversation.form.number();
```
Now we calculate the total amount of the order and generate a random string, which we will use to comment on the transaction and add the dumplings postfix
```js
  // Get the total cost: multiply the number of portions by the price of the 1 portion
  const amount = count * 3;
  // Generate random comment
  const comment = Math.random().toString(36).substring(2, 8) + "dumplings";
```

And we save the resulting data to the session so that we can get this data in the next handler.
```js
  conversation.session.amount = amount;
  conversation.session.comment = comment;
```

We generate links to go to a quick payment and create an inline keyboard
```js
const tonhubPaymentLink = generatePaymentLink(
    process.env.OWNER_WALLET,
    amount,
    comment,
    "tonhub"
  );
  const tonkeeperPaymentLink = generatePaymentLink(
    process.env.OWNER_WALLET,
    amount,
    comment,
    "tonkeeper"
  );

  const menu = new InlineKeyboard()
    .url("Click to pay in TonHub", tonhubPaymentLink)
    .row()
    .url("Click to pay in Tonkeeper", tonkeeperPaymentLink)
    .row()
    .text(`I sent ${amount} TON`, "check_transaction");
```
And we send our message with the keyboard, where we ask the user to send a transaction to our wallet address with a randomly generated comment
```js
  await ctx.reply(
    `
Fine, all you have to do is transfer ${amount} TON to the wallet <code>${process.env.OWNER_WALLET}</code> with the comment <code>${comment}</code>.

<i>WARNING: I am currently working on ${process.env.NETWORK}</i>

P.S. You can conveniently make a transfer by clicking on the appropriate button below and confirm the transaction in the offer`,
    { reply_markup: menu, parse_mode: "HTML" }
  );
}
```

Now all we have to do is create a handler to check for the presence of a transaction
```js
export async function checkTransaction(ctx) {
  await ctx.answerCallbackQuery({
    text: "Wait a bit, I need to check the availability of your transaction",
  });

  if (
    await verifyTransactionExistance(
      process.env.OWNER_WALLET,
      ctx.session.amount,
      ctx.session.comment
    )
  ) {
    const menu = new InlineKeyboard().text("Buy more dumplings🥟", "buy");

    await ctx.reply("Thank you so much. Enjoy your meal!", {
      reply_markup: menu,
    });

    // Reset the session data
    ctx.session.amount = 0;
    ctx.session.comment = "";
  } else {
    await ctx.reply("I didn't receive your transaction, wait a bit");
  }
}
```
All we are doing here is just checking for a transaction, and provided that it exists, we tell the user about it and reset the data in the session


### Bot start

To start use this command:

```bash npm2yarn
npm run app
```

If your bot doesn't work correctly, compare your code with code [from this repository](https://github.com/coalus/DumplingShopBot). If it didn't help, feel free to write me in telegram. You can find my telegram account below

## References

 - Made for TON as part of [ton-footsteps/58](https://github.com/ton-society/ton-footsteps/issues/58)
 - By Coalus ([Telegram @coalus](https://t.me/coalus), [Coalus on GitHub](https://github.com/coalus))
 - [Bot Sources](https://github.com/coalus/DumplingShopBot)
