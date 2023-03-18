# Sample tutorial structure 

## Introduction

The Introduction heading **must** be H2: `## Introduction`

This section is for you to explain the context of this tutorial and why it is important, what we're going to build and learn in this tutorial.

- Explain this section like you're explaining it to a 5-year-old (**[ELI5](https://www.dictionary.com/e/slang/eli5/)**)
- Explain everything in 5–6 lines maximum.

*For example:*

>A smart contract is just a computer program that runs on the TON Blockchain, or more specifically on its [TVM](/learn/tvm-instructions/tvm-overview) (_TON Virtual Machine_). The contract is made of code (_compiled TVM instructions_) and data (_persistent state_) that are stored at some address on TON.

## Prerequisites

The Prerequisites heading **must** be H2: `## Prerequisites`

This section is for you to explain any prior knowledge needed or any existing tutorials that need to be completed first. Any tokens that are needed—mention them here.

*For example:*

>In this tutorial, we're going to mint Jetton on testnet. Before we continue, make sure that your [testnet](/develop/smart-contracts/environment/testnet) wallet has sufficient balance. 

## Requirements

The Requirements heading **must** be H2: `## Requirements`

**OPTIONAL :** Embed any video content in this section if your tutorial has any.

Any technology that needs to be installed **prior** to starting the tutorial and that the tutorial will not cover (`TON Wallet Extension`, `node`, etc.). Do not list packages that will be installed during the tutorial.

*For example:*

- We'll need the TON Wallet extension in this tutorial; install it from [HERE](https://chrome.google.com/webstore/detail/ton-wallet/nphplpgoakhhjchkkhmiggakijnkhfnd).
- Make sure to have NodeJS 12.0.1+ installed.

## Body of the Tutorial

- Please do not use "Body of the Tutorial" as a heading, use your own heading that is relevant to the material.
  - "Getting started" is acceptable if you can't think of anything else 😉
- Add any text content necessary to guide readers through your tutorial, and ***remember to proofread your content*** for spelling and grammar before you submit your tutorial.
  - [Grammarly](http://grammarly.com) is a good free program that can help you avoid grammar mistakes.

### Key points

- Do not use "Body of the Tutorial" as a heading!
- **Keep all subheadings at H3,** don't go for H4 or any lower.
    - In Markdown syntax, two hashmarks are used for H2 headings: ##
    - Three hashmarks are used for H3 headings: ###
- Add only necessary comments to code blocks. ***Do not*** add # style comments to terminal input code blocks.
- Add all relevant code blocks:
    - Markdown syntax for code blocks consists of three backticks at the beginning and end of the code block.  Also, make sure that there is a newline before and after the backticks in all code blocks. *For example*:
        - 
        \```js  
        const testVariable = 'some string';  
        someFunctionCall();  
        \```  
        
    - ALL code blocks ***must*** have a syntax highlight type. Use ```text if you are not sure.
    - \```text must be used for terminal output, terminal commands, and plaintext.
    - \```javascript *or* ```js can be used for any JavaScript code.
    - \```typescript or ```ts can be used for any TypeScript code.
    - \```jsx is for ReactJS code.
    - \```cpp is for Func code.
    - Use \```graphql when highlighting GraphQL syntax.
    - Use \```json when highlighting valid JSON. (For invalid JSON examples use \```text instead.)
    - \```bash should *only* be used in code blocks where you need to have # style comments. This must be done carefully because in many situations the # character will render as a markdown heading. Typically, the Table of Contents will be affected if this occurs.
- Do not use `pre-formatted text` for emphasis; instead, use only **bold** or *italic* text.
- Add images or code blocks to reflect the expected terminal output.

- Take an error-driven approach when writing your tutorial. Add common errors and troubleshooting steps. *For example:*

> **Unable to connect to Testnet due to an error when executing the
> `node deploy:testnet` command.** 
>
> Let's look at some common causes:
>  
* Make sure you have enough funds in your generated testnet wallet in `.env`. If not, please add some testnet coins from the faucet giver. 
* If you're still experiencing the same issue, reach out to the devs in the [Dev Chat](https://t.me/TonDev_eng/) for help.
>

## Conclusion

The Conclusion heading **must** be H2: `## Conclusion`

This section should summarize what was learned in the tutorial, reinforce key points, and congratulate the learner on completing the tutorial. Use a maximum of 5–6 lines.
*For example*:

> We created a simple new FunC contract with counter functionality. We then built and deployed it on-chain, and finally interacted with it by calling a getter and sending a message.


Please remember that this code is not meant for production; there are still a few other things to consider if you wanted to deploy this to mainnet, such as disabling the transfer method if the token is listed on the market, and so on.
>

## Next Steps *(Optional)*

The Next Steps heading **must** be H2: `## Next Steps`

Use this section to explain what can be done next after this tutorial to continue learning.
Feel free to add recommended projects and articles relating to this tutorial.
If you're working on any other advanced tutorials, you can briefly mention them here.

## About the Author

The About the Author heading **must** be H2: `## About the Author`

Keep it short. One or two lines at most. You can include a link to your GitHub profile + Telegram profile. Please refrain from adding your LinkedIn or Twitter here.

## References

The References heading **must** be H2: `## References`

This section ***must*** be present if you have taken any help in writing this tutorial from other documents, GitHub repos or pre-existing tutorials.

Credit sources by adding their name and a link to the document when possible.

If it is not a digital document, include an ISBN or other form of reference.