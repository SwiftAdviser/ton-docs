# Mint your first Jetton

Welcome, dev! It's great to have you here. 👋

In this article, we'll tell you about creating your first fungible token (Jetton) on TON.

To mint Jettons we will be using the [TON Minter](https://minter.ton.org/) browser service.

## 📖 What you'll learn

In this article, you'll learn how to:

- deploy a Jetton using your browser
- customize your token
- manage and use your token
- edit the token parameters


## 📌 Prepare before you start

1. First you need to have the [Tonhub](https://ton.app/wallets/tonhub-wallet) wallet or [Chrome extension](https://ton.app/wallets/chrome-plugin).
2. You must have on your balance more than 0.25 Toncoin + funds to cover the blockchain commission. 

:::tip Starter tip
 ~0.5 TON is definitely enough for this tutorial.
:::
 
## 🚀 Let's get started!

Use your web browser to open the service [TON Minter](https://minter.ton.org/).

![image](/img/tutorials/jetton/jetton-main-page.png)

### Deploy a Jetton using your browser

#### Connect Wallet

Click the `Connect Wallet` button to connect your [Tonhub](https://ton.app/wallets/tonhub-wallet) wallet or a [Chrome extension](https://ton.app/wallets/chrome-plugin).

![image](/img/tutorials/jetton/jetton-connect-wallet.png)

**Scan the QR-code** in [Tonhub](https://ton.app/wallets/tonhub-wallet) or **sign in** to the wallet via the [Chrome extension](https://ton.app/wallets/chrome-plugin).

#### Fill in the blanks with relevant information

1. Name (usually 1-3 words).
2. Symbol (usually 3-5 uppercase characters).
3. Amount (for example, 1,000,000).
4. Description of the token (optional).
5. Token logo URL (optional).
6. Deploy your token (Jetton) and complete a transaction in the wallet.


#### Token logo URL

If you want to have an attractive Jetton token, you need a beautiful logo hosted somewhere.  For example:

* https://bitcoincash-example.github.io/website/logo.png

:::info
 You can easily find out about about url placement of the logo in the [repository](https://github.com/ton-blockchain/minter-contract#jetton-metadata-field-best-practices) in paragraph "Where is this metadata stored".

 * On-chain.
 * Off-chain IPFS.
 * Off-chain website.
:::

#### How to create your logo URL?

 1. Prepare a **256x256** PNG image of the token logo with a transparent background.
 2. Get a link to your logo. A good solution is [GitHub Pages](https://pages.github.com/). Let's use them.
 3. [Create a new public repository](https://docs.github.com/en/get-started/quickstart/create-a-repo) with the name `website`.
 4. Upload your prepared image to git and enable `GitHub Pages`.
    1. [Add GitHub Pages to your repository](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).
    2. [Upload your image and get a link](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).
 5. If you have your own domain, then it would be good to use `.org` instead of `github.io`.
 

 ## 💸 Send and receive Jettons
 On the right side of the screen, you see a connected wallet that can **receive tokens.**

![image](/img/tutorials/jetton/jetton-receive-tokens.png)

 Just below you can **send tokens** to multi-currency wallets like [Tonkeeper](https://tonkeeper.com/) or [Tonhub](https://ton.app/wallets/tonhub-wallet).

![image](/img/tutorials/jetton/jetton-send-tokens.png)


:::info
 You always also **burn** your Jettons to reduce their amount.
:::


 ### 📱 Send tokens from phone using Tonkeeper

Prerequisites:

1. You must already have tokens on your balance to send them.
2. There must be at least 0.1 Toncoin to pay transaction fees.

#### Step-by-step guide

Then go to **your token**, set the **amount** to send, and enter the **recipient address.**

![image](/img/tutorials/jetton/jetton-send-tokens.png)

 ## ✏️ Jetton (token) customization

With [FunC](/develop/func/overview) language you can change the behavior of the token in your favor.

To make any changes, begin here:

* https://github.com/ton-blockchain/minter-contract

### Step-by-step guide

 1. Make sure you have all "Dependencies and Requirements" from the [tonstarter-contracts](https://github.com/ton-defi-org/tonstarter-contracts) repo.
 2. Clone the [minter-contract repository](https://github.com/ton-blockchain/minter-contract) and rename the project. 
 3. To install you need to open a terminal at the root and run:

 ```bash npm2yarn
 npm install
 ```

 4. Edit the original smart contract files same way in the root terminal. All contract files are in `contracts/*.fc`

 5. Build a project by using: 

 ```bash npm2yarn
 npm run build
 ```
 The build result will be describes the process of creating the necessary files, as well as the search for smart contracts. 
 
 
 :::info
 Read the console, there are a lot of tips!
 :::
    
 6. You can test your changes by using:

 ```bash npm2yarn
 npm run test
 ```

 7. Edit the **name** and other metadata of the token in `build/jetton-minter.deploy.ts` by changing JettonParams object.

 ```js
// This is example data - Modify these params for your own jetton!
// - Data is stored on-chain (except for the image data itself)
// - Owner should usually be the deploying wallet's address.
   
 const jettonParams = {
  owner: Address.parse("EQD4gS-Nj2Gjr2FYtg-s3fXUvjzKbzHGZ5_1Xe_V0-GCp0p2"),
  name: "MyJetton",
  symbol: "JET1",
  image: "https://www.linkpicture.com/q/download_183.png", // Image url
  description: "My jetton",
};
 ```

 8. To deploy a token use the following command:

 ```bash npm2yarn
 npm run deploy
 ```
 The result of running your project:

    ```js
    > @ton-defi.org/jetton-deployer-contracts@0.0.2 deploy
    > ts-node ./build/_deploy.ts

    =================================================================
    Deploy script running, let's find some contracts to deploy..

    * We are working with 'mainnet'

    * Config file '.env' found and will be used for deployment!
     - Wallet address used to deploy from is: YOUR-ADDRESS
     - Wallet balance is YOUR-BALANCE TON, which will be used for gas

    * Found root contract 'build/jetton-minter.deploy.ts - let's deploy it':
     - Based on your init code+data, your new contract address is: YOUR-ADDRESS
     - Let's deploy the contract on-chain..
     - Deploy transaction sent successfully
     - Block explorer link: https://tonwhales.com/explorer/address/YOUR-ADDRESS
     - Waiting up to 20 seconds to check if the contract was actually deployed..
     - SUCCESS! Contract deployed successfully to address: YOUR-ADDRESS
     - New contract balance is now YOUR-BALANCE TON, make sure it has enough to pay rent
     - Running a post deployment test:
    {
      name: 'MyJetton',
      description: 'My jetton',
      image: 'https://www.linkpicture.com/q/download_183.png',
      symbol: 'JET1'
    }
    ```


## What's next?

If you want to go deeper, read this article by Tal Kol:  
* [How and why to shard your smart contract—studying the anatomy of TON Jettons](https://blog.ton.org/how-to-shard-your-ton-smart-contract-and-why-studying-the-anatomy-of-tons-jettons)


## References

 - Project: https://github.com/ton-blockchain/minter-contract
 - By Slava ([Telegram @delovoyslava](https://t.me/delovoyslava), [delovoyhomie on GitHub](https://github.com/delovoyhomie))
