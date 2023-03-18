# TON Node Types

There are different types of nodes in The Open Network:

* **Lite clients**

  Clients, such as wallets, that do not store the full state of the blockchain but request what is needed from the full nodes.

* **Full Node**

  A node that is synchronized with the blockchain, stores the current state of the blockchain and the block history or part of the block history.

  In a full node, you can enable one or more additional functionalities:

  * **Archive node**
  
     A full node that stores the entire block history is called an archive node.

     An archive node requires a lot of resources and is needed if you are making a blockchain explorer or something like that.

     For most cases, you will be fine with a regular node that only stores the latest blocks and has significantly lower hardware requirements.

  * **Lite server**

     If you enable an endpoint in a full node, then it starts to perform the functions of a lite server - it can receive and respond to requests from lite clients.

     Using this node, your product can interact with TON Blockchain.

      TON Foundation supports a number of **public lite servers** that you can find in the global config ([mainnet](https://ton.org/global-config.json) and [testnet](https://ton.org/testnet-global.config.json)).

     These are endpoints available to everyone, for example, standard wallets connect to them.

  * **Validator** 

     If you enable the validator functionality in the node and you have a sufficient number of Toncoin (stake), then the node will begin to participate in the process of validating new network blocks. 
  
     TON is a Proof-of-Stake blockchain, so validators keep the network running and are rewarded in Toncoin for doing so.