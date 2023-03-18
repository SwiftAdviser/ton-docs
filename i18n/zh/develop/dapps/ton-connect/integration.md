# Integration manual

:::info
Information present on this page might become outdated. Though, a strong effort is made to create such an article that will allow developers to handle everything new that is introduced in the future.
:::

In this tutorial, we are going to create a sample web app supporting TON Connect 2.0 authentication. It will be able to check signatures so user would be unable to impersonate someone else without establishing an agreement with that party.

## Documentation links

1. [SDK documentation](https://www.npmjs.com/package/@tonconnect/sdk)  
2. [Protocol of wallet-application message exchange](https://github.com/ton-connect/docs/blob/main/requests-responses.md), includes manifest format.
3. [Tonkeeper implementation of wallet side](https://github.com/tonkeeper/wallet/tree/main/src/tonconnect)

## Prerequisites

The web app must have a manifest accessible by users' wallet applications. Thus, the prerequisite is a host for static files. For example, you may wish to use GitHub Pages, or deploy your site with TON Sites technology and host it on your computer. From now we will assume the web app site is publicly accessible.

## Getting wallets support list

TON Connect 2.0 is technology that is going to be widely adopted, so many wallet applications are going to support this. When this article's subject was suggested, only Tonkeeper was supporting it; at the moment of writing there are two wallets, Tonkeeper and OpenMask. We are going to support **every** wallet application that works with TON Connect 2.0.

So, at the moment our sample web app does following:
1. loads TON Connect SDK (helper library for easy integration),
2. creates a connector (currently without application manifest),
3. and loads list of supported wallets (from [wallets.json on GitHub](https://raw.githubusercontent.com/ton-connect/wallets-list/main/wallets.json)).

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <script src="https://unpkg.com/@tonconnect/sdk@latest/dist/tonconnect-sdk.min.js" defer></script>  <!-- (1) -->
  </head>
  <body>
    <script>
      window.onload = async () => {
        const connector = new TonConnectSDK.TonConnect();  // (2)
        const walletsList = await connector.getWallets();  // (3)
        
        console.log(walletsList);
      }
    </script>
  </body>
</html>
```

If you load this page in browser and look into console, you may get something like that:

```js
> Array [ {…}, {…} ]

0: Object { name: "Tonkeeper", imageUrl: "https://tonkeeper.com/assets/tonconnect-icon.png", aboutUrl: "https://tonkeeper.com", … }
  aboutUrl: "https://tonkeeper.com"
  bridgeUrl: "https://bridge.tonapi.io/bridge"
  deepLink: undefined
  embedded: false
  imageUrl: "https://tonkeeper.com/assets/tonconnect-icon.png"
  injected: false
  jsBridgeKey: "tonkeeper"
  name: "Tonkeeper"
  tondns: "tonkeeper.ton"
  universalLink: "https://app.tonkeeper.com/ton-connect"

1: Object { name: "OpenMask", imageUrl: "https://raw.githubusercontent.com/OpenProduct/openmask-extension/main/public/openmask-logo-288.png", aboutUrl: "https://www.openmask.app/", … }
  aboutUrl: "https://www.openmask.app/"
  embedded: false
  imageUrl: "https://raw.githubusercontent.com/OpenProduct/openmask-extension/main/public/openmask-logo-288.png"
  injected: false
  jsBridgeKey: "openmask"
  name: "OpenMask"
  tondns: undefined
```

According to TON Connect 2.0 specification, wallet app information has the following format:
```js
{
    name: string;
    imageUrl: string;
    tondns?: string;
    aboutUrl: string;
    universalLink?: string;
    deepLink?: string;
    bridgeUrl?: string;
    jsBridgeKey?: string;
    injected?: boolean; // true if this wallet is injected to the webpage
    embedded?: boolean; // true if the dapp is opened inside this wallet's browser
}
```

## Showing buttons for each wallet

Buttons may vary according to your web app style.  
Current page produces the following result:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <script src="https://unpkg.com/@tonconnect/sdk@latest/dist/tonconnect-sdk.min.js" defer></script>

    // highlight-start
    <style>
      body {
        width: 1000px;
        margin: 0 auto;
        font-family: Roboto, sans-serif;
      }
      .section {
        padding: 20px; margin: 20px;
        border: 2px #AEFF6A solid; border-radius: 8px;
      }
      #tonconnect-buttons>button {
        display: block;
        padding: 8px; margin-bottom: 8px;
        font-size: 18px; font-family: inherit;
      }
      .featured {
        font-weight: 800;
      }
    </style>
    // highlight-end
  </head>
  <body>
    // highlight-start
    <div class="section" id="tonconnect-buttons">
    </div>
    // highlight-end
    
    <script>
      const $ = document.querySelector.bind(document);
      
      window.onload = async () => {
        const connector = new TonConnectSDK.TonConnect();
        const walletsList = await connector.getWallets();

        // highlight-start
        let buttonsContainer = $('#tonconnect-buttons');
        
        for (let wallet of walletsList) {
          let connectButton = document.createElement('button');
          connectButton.innerText = 'Connect with ' + wallet.name;
          
          if (wallet.embedded) {
            // `embedded` means we are browsing the app from wallet application
            // we need to mark this sign-in option somehow
            connectButton.classList.add('featured');
          }
          
          if (!wallet.bridgeUrl && !wallet.injected && !wallet.embedded) {
            // no `bridgeUrl` means this wallet app is injecting JS code
            // no `injected` and no `embedded` -> app is inaccessible on this page
            connectButton.disabled = true;
          }
          
          buttonsContainer.appendChild(connectButton);
        }
	// highlight-end
      };
    </script>
  </body>
</html>
```

Please note we haven't ever started connecting users but we already have a rather complex code! Let's look at two details:
1. If user is seeing our page through wallet application, it sets property `embedded` to `true`. So we should highlight this login option as it's the easiest to user and probably it is what he wants.
2. If some wallet is JS-only (it has no `bridgeUrl`) and it hasn't set property `injected` (or `embedded`, for safety), then it is clearly inaccessible so we should disable that button.

## Connection without app manifest

Script shall be changed as following:

```js
      const $ = document.querySelector.bind(document);
      
      window.onload = async () => {
        const connector = new TonConnectSDK.TonConnect();
        const walletsList = await connector.getWallets();
        
        const unsubscribe = connector.onStatusChange(
          walletInfo => {
            console.log('Connection status:', walletInfo);
          }
        );
        
        let buttonsContainer = $('#tonconnect-buttons');

        for (let wallet of walletsList) {
          let connectButton = document.createElement('button');
          connectButton.innerText = 'Connect with ' + wallet.name;
          
          if (wallet.embedded) {
            // `embedded` means we are browsing the app from wallet application
            // we need to mark this sign-in option somehow
            connectButton.classList.add('featured');
          }
          
          // highlight-start
          if (wallet.embedded || wallet.injected) {
            connectButton.onclick = () => {
              connectButton.disabled = true;
              connector.connect({jsBridgeKey: wallet.jsBridgeKey});
            };
          } else if (wallet.bridgeUrl) {
            connectButton.onclick = () => {
              connectButton.disabled = true;
              console.log('Connection link:', connector.connect({
                universalLink: wallet.universalLink,
                bridgeUrl: wallet.bridgeUrl
              }));
            };
          } else {
            // wallet app does not provide any auth method
            connectButton.disabled = true;
          }
	  // highlight-end
          
          buttonsContainer.appendChild(connectButton);
        }
      };
```

Now we are logging status changes (to see whether TON Connect works). Showing modals with QR codes for connection is out of scope for this article; for testing you may either use browser extension or send connection link to your phone via any means (for example, Telegram works well).

Please note we haven't created app manifest yet. We're trying to see what happens if we don't fulfill this requirement.

### Logging in with Tonkeeper

Link created for auth (provided for reference):
```
https://app.tonkeeper.com/ton-connect?v=2&id=3c12f5311be7e305094ffbf5c9b830e53a4579b40485137f29b0ca0c893c4f31&r=%7B%22manifestUrl%22%3A%22null%2Ftonconnect-manifest.json%22%2C%22items%22%3A%5B%7B%22name%22%3A%22ton_addr%22%7D%5D%7D
```
When decoded, `r` parameter produces the following JSON:
```js
{"manifestUrl":"null/tonconnect-manifest.json","items":[{"name":"ton_addr"}]}
```

Upon tapping the link on mobile phone, Tonkeeper app automatically opened and then closed, dismissing the request. Also, an error appeared in web app page console: `Error: [TON_CONNECT_SDK_ERROR] Can't get null/tonconnect-manifest.json`.
   
Conclusion: application manifest must be available for downloading.

### Logging in with OpenMask

OpenMask didn't inject its information in the window so connecting with it failed. The most probable reason is using local page for web app.

## Connection with app manifest

Starting from here, you need to host your files (mostly tonconnect-manifest.json) somewhere.
I will use manifest of *other* webapp. This is not recommended but it's possible.

You have to replace script lines
```js
      window.onload = async () => {
        const connector = new TonConnectSDK.TonConnect();
        
        const walletsList = await connector.getWallets();
        
        const unsubscribe = connector.onStatusChange(
          walletInfo => {
            console.log('Connection status:', walletInfo);
          }
        );
```
with
```js
      window.onload = async () => {
        const connector = new TonConnectSDK.TonConnect({manifestUrl: 'https://ratingers.pythonanywhere.com/ratelance/tonconnect-manifest.json'});
        // highlight-next-line
        window.connector = connector;  // for experimenting in browser console
        
        const walletsList = await connector.getWallets();
        
        const unsubscribe = connector.onStatusChange(
          walletInfo => {
            console.log('Connection status:', walletInfo);
          }
        );
	// highlight-next-line
        connector.restoreConnection();
```

We added storing local `connector` variable in `window` for it to be accessible in browser console. Also we use `restoreConnection` for user not to log in on each webapp page.

### Logging in with Tonkeeper

First of all, I tested declining the request. The result that appeared in console was `Error: [TON_CONNECT_SDK_ERROR] Wallet declined the request`.

Then, the user is able to accept the same login request if he saves the link. So web app should handle authentication decline as non-final, or else it can be messed up with.

After that, I've accepted login request. It was immediately reflected in browser console:
```js
22:40:13.887 Connection status:
Object { device: {…}, provider: "http", account: {…} }
  account: Object { address: "0:b2a1ec...", chain: "-239", walletStateInit: "te6cckECFgEAAwQAAgE0ARUBFP8A9..." }
  device: Object {platform: "android", appName: "Tonkeeper", appVersion: "2.8.0.261", …}
  provider: "http"
```

So, what do we get is:
1. Account information: address (workchain+hash), network (mainnet/testnet), wallet stateInit that can be used for public key extraction.
2. Device information: name and version of wallet application (name should be equal to that we requested, but we can check that for additional confidence), the platform name and supported features list.
3. Provider: http -- that means all requests and responses between wallet app and web app are served over the bridge.

## Logging out and requesting TonProof

We have logged into our webapp, but... how does backend know that's us? We need to request the wallet ownership proof!
This can be done only at authentication, so we need to log out. Run the following code in console.
```js
connector.disconnect();
```
It returns a promise with no value. Also, when disconnect is complete, you'll see the line `Connection status: null`.

Before we go on adding TonProof, let's tamper with our code to show that current implementation is unsafe.
```js
let connHandler = connector.statusChangeSubscriptions[0];
connHandler({
  device: {
    appName: "Uber Singlesig Cold Wallet App",
    appVersion: "4.0.1",
    features: [],
    maxProtocolVersion: 3,
    platform: "ios"
  },
  account: {
    /* TON Foundation address */
    address: '0:83dfd552e63729b472fcbcc8c45ebcc6691702558b68ec7527e1ba403a0f31a8',
    chain: '-239',
    walletStateInit: 'te6ccsEBAwEAoAAFcSoCATQBAgDe/wAg3SCCAUyXuiGCATOcurGfcbDtRNDTH9MfMdcL/+ME4KTyYIMI1xgg0x/TH9Mf+CMTu/Jj7UTQ0x/TH9P/0VEyuvKhUUS68qIE+QFUEFX5EPKj+ACTINdKltMH1AL7AOjRAaTIyx/LH8v/ye1UAFAAAAAAKamjF3LJ7WtipuLroUqTuQRi56Nnd3vrijj7FbnzOETSLOL/HqR30Q=='
  },
  provider: 'http'
});
```

You'll see lines in console almost identical to those when we connected normally. So if backend doesn't perform user authentication we can pretend to be even TON Foundation, and if balance or some token ownership gives any privileges to user we can get that privilege as well.
Of course, provided code doesn't change any variables in `connector`, but user can do anything unless that `connector` is protected by the closure; and even then it would not be that hard to extract it using debugger and breakpoints.

So that necessity of authenticating user was proved, let's proceed to writing the code.

## Connection with TonProof

According to documentation, we can pass second argument to `.connect()` method. It contains a payload that will be wrapped and signed by the wallet.
New connection code follows:

```js
          if (wallet.embedded || wallet.injected) {
            connectButton.onclick = () => {
              connectButton.disabled = true;
              connector.connect({jsBridgeKey: wallet.jsBridgeKey},
                                {tonProof: 'doc-example-<BACKEND_AUTH_ID>'});
            };
          } else if (wallet.bridgeUrl) {
            connectButton.onclick = () => {
              connectButton.disabled = true;
              console.log('Connection link:', connector.connect({
                universalLink: wallet.universalLink,
                bridgeUrl: wallet.bridgeUrl
              }, {tonProof: 'doc-example-<BACKEND_AUTH_ID>'}));
            };
```

Connection link:
```
https://app.tonkeeper.com/ton-connect?v=2&id=4b0a7e2af3b455e0f0bafe14dcdc93f1e9e73196ae2afaca4d9ba77e94484a44&r=%7B%22manifestUrl%22%3A%22https%3A%2F%2Fratingers.pythonanywhere.com%2Fratelance%2Ftonconnect-manifest.json%22%2C%22items%22%3A%5B%7B%22name%22%3A%22ton_addr%22%7D%2C%7B%22name%22%3A%22ton_proof%22%2C%22payload%22%3A%22doc-example-%3CBACKEND_AUTH_ID%3E%22%7D%5D%7D
```
Expanded and prettified `r` parameter:
```js
{
  "manifestUrl":
    "https://ratingers.pythonanywhere.com/ratelance/tonconnect-manifest.json",
  "items": [
    {"name": "ton_addr"},
    {"name": "ton_proof", "payload": "doc-example-<BACKEND_AUTH_ID>"}
  ]
}
```

Then we transfer this link to phone and open it through Tonkeeper.

And here's full wallet information which we receive upon successful connection:
```js
{
  "device": {
    "platform": "android",
    "appName": "Tonkeeper",
    "appVersion": "2.8.0.261",
    "maxProtocolVersion": 2,
    "features": [
      "SendTransaction"
    ]
  },
  "provider": "http",
  "account": {
    "address": "0:b2a1ecf5545e076cd36ae516ea7ebdf32aea008caa2b84af9866becb208895ad",
    "chain": "-239",
    "walletStateInit": "te6cckECFgEAAwQAAgE0ARUBFP8A9KQT9LzyyAsCAgEgAxACAUgEBwLm0AHQ0wMhcbCSXwTgItdJwSCSXwTgAtMfIYIQcGx1Z70ighBkc3RyvbCSXwXgA/pAMCD6RAHIygfL/8nQ7UTQgQFA1yH0BDBcgQEI9ApvoTGzkl8H4AXTP8glghBwbHVnupI4MOMNA4IQZHN0crqSXwbjDQUGAHgB+gD0BDD4J28iMFAKoSG+8uBQghBwbHVngx6xcIAYUATLBSbPFlj6Ahn0AMtpF8sfUmDLPyDJgED7AAYAilAEgQEI9Fkw7UTQgQFA1yDIAc8W9ADJ7VQBcrCOI4IQZHN0coMesXCAGFAFywVQA88WI/oCE8tqyx/LP8mAQPsAkl8D4gIBIAgPAgEgCQ4CAVgKCwA9sp37UTQgQFA1yH0BDACyMoHy//J0AGBAQj0Cm+hMYAIBIAwNABmtznaiaEAga5Drhf/AABmvHfaiaEAQa5DrhY/AABG4yX7UTQ1wsfgAWb0kK29qJoQICga5D6AhhHDUCAhHpJN9KZEM5pA+n/mDeBKAG3gQFImHFZ8xhAT48oMI1xgg0x/TH9MfAvgju/Jk7UTQ0x/TH9P/9ATRUUO68qFRUbryogX5AVQQZPkQ8qP4ACSkyMsfUkDLH1Iwy/9SEPQAye1U+A8B0wchwACfbFGTINdKltMH1AL7AOgw4CHAAeMAIcAC4wABwAORMOMNA6TIyx8Syx/L/xESExQAbtIH+gDU1CL5AAXIygcVy//J0Hd0gBjIywXLAiLPFlAF+gIUy2sSzMzJc/sAyEAUgQEI9FHypwIAcIEBCNcY+gDTP8hUIEeBAQj0UfKnghBub3RlcHSAGMjLBcsCUAbPFlAE+gIUy2oSyx/LP8lz+wACAGyBAQjXGPoA0z8wUiSBAQj0WfKnghBkc3RycHSAGMjLBcsCUAXPFlAD+gITy2rLHxLLP8lz+wAACvQAye1UAFEAAAAAKamjFyM60x2mt5eboNyOTE+5RGOe9Ee2rK1Qcb+0ZuiP9vb7QJRlz/c="
  },
  "connectItems": {
    "tonProof": {
      "name": "ton_proof",
      "proof": {
        "timestamp": 1674392728,
        "domain": {
          "lengthBytes": 28,
          "value": "ratingers.pythonanywhere.com"
        },
        "signature": "trCkHit07NZUayjGLxJa6FoPnaGHkqPy2JyNjlUbxzcc3aGvsExCmHXi6XJGuoCu6M2RMXiLzIftEm6PAoy1BQ==",
        "payload": "doc-example-<BACKEND_AUTH_ID>"
      }
    }
  }
}
```

Let's verify the received signature. We'll do this with Python to show that this is possible on backend side.
Required libraries: `tonsdk`, `pynacl`.

First of all, we must get wallet's public key. We will NOT use `tonapi.io` or similar services as there are no reasons why we may rely on their answer. We will parse `walletStateInit`.

Also, we have to check that `address` and `walletStateInit` match, or one could sign the payload with their wallet key, provide own wallet in stateInit field and other wallet in address field.

StateInit has two references: one for code and one for data. We want to get public key so we load the second reference. Then we skip 8 bytes (4 bytes are used for `seqno` and 4 for `subwallet_id` in all modern wallet contracts) and load the next 32 bytes (256 bits) -- they are the key.

```python
import nacl.signing
import tonsdk

import hashlib
import base64

received_state_init = 'te6cckECFgEAAwQAAgE0ARUBFP8A9KQT9LzyyAsCAgEgAxACAUgEBwLm0AHQ0wMhcbCSXwTgItdJwSCSXwTgAtMfIYIQcGx1Z70ighBkc3RyvbCSXwXgA/pAMCD6RAHIygfL/8nQ7UTQgQFA1yH0BDBcgQEI9ApvoTGzkl8H4AXTP8glghBwbHVnupI4MOMNA4IQZHN0crqSXwbjDQUGAHgB+gD0BDD4J28iMFAKoSG+8uBQghBwbHVngx6xcIAYUATLBSbPFlj6Ahn0AMtpF8sfUmDLPyDJgED7AAYAilAEgQEI9Fkw7UTQgQFA1yDIAc8W9ADJ7VQBcrCOI4IQZHN0coMesXCAGFAFywVQA88WI/oCE8tqyx/LP8mAQPsAkl8D4gIBIAgPAgEgCQ4CAVgKCwA9sp37UTQgQFA1yH0BDACyMoHy//J0AGBAQj0Cm+hMYAIBIAwNABmtznaiaEAga5Drhf/AABmvHfaiaEAQa5DrhY/AABG4yX7UTQ1wsfgAWb0kK29qJoQICga5D6AhhHDUCAhHpJN9KZEM5pA+n/mDeBKAG3gQFImHFZ8xhAT48oMI1xgg0x/TH9MfAvgju/Jk7UTQ0x/TH9P/9ATRUUO68qFRUbryogX5AVQQZPkQ8qP4ACSkyMsfUkDLH1Iwy/9SEPQAye1U+A8B0wchwACfbFGTINdKltMH1AL7AOgw4CHAAeMAIcAC4wABwAORMOMNA6TIyx8Syx/L/xESExQAbtIH+gDU1CL5AAXIygcVy//J0Hd0gBjIywXLAiLPFlAF+gIUy2sSzMzJc/sAyEAUgQEI9FHypwIAcIEBCNcY+gDTP8hUIEeBAQj0UfKnghBub3RlcHSAGMjLBcsCUAbPFlAE+gIUy2oSyx/LP8lz+wACAGyBAQjXGPoA0z8wUiSBAQj0WfKnghBkc3RycHSAGMjLBcsCUAXPFlAD+gITy2rLHxLLP8lz+wAACvQAye1UAFEAAAAAKamjFyM60x2mt5eboNyOTE+5RGOe9Ee2rK1Qcb+0ZuiP9vb7QJRlz/c='
received_address = '0:b2a1ecf5545e076cd36ae516ea7ebdf32aea008caa2b84af9866becb208895ad'

state_init = tonsdk.boc.Cell.one_from_boc(base64.b64decode(received_state_init))

address_hash_part = base64.b16encode(state_init.bytes_hash()).decode('ascii').lower()
assert received_address.endswith(address_hash_part)

public_key = state_init.refs[1].bits.array[8:][:32]

print(public_key)
# bytearray(b'#:\xd3\x1d\xa6\xb7\x97\x9b\xa0\xdc\x8eLO\xb9Dc\x9e\xf4G\xb6\xac\xadPq\xbf\xb4f\xe8\x8f\xf6\xf6\xfb')

verify_key = nacl.signing.VerifyKey(bytes(public_key))
```

After that, we look into documentation to check what exactly is signed with wallet key.

> ```
> message = utf8_encode("ton-proof-item-v2/") ++  
>           Address ++  
>           AppDomain ++  
>           Timestamp ++  
>           Payload
> 
> signature = Ed25519Sign(
>   privkey,
>   sha256(0xffff ++ utf8_encode("ton-connect") ++ sha256(message))
> )
> ```
> 
> where:
> -   `Address` is the wallet address encoded as a sequence:
>     -   `workchain`: 32-bit signed integer big endian;
>     -   `hash`: 256-bit unsigned integer big endian;
> -   `AppDomain` is Length ++ EncodedDomainName
>     -   `Length` is 32-bit value of utf-8 encoded app domain name length in bytes
>     -   `EncodedDomainName` id `Length`-byte utf-8 encoded app domain name
> -   `Timestamp` 64-bit unix epoch time of the signing operation
> -   `Payload` is a variable-length binary string
> -   `utf8_encode` produces plain byte string with no length prefixes.

Let's reimplement this in Python. Endianness of some integers is not specified so we must look into some example -- for example, you may refer to Tonkeeper implementation: [ConnectReplyBuilder.ts](https://github.com/tonkeeper/wallet/blob/77992c08c663dceb63ca6a8e918a2150c75cca3a/src/tonconnect/ConnectReplyBuilder.ts#L42).

```python
received_timestamp = 1674392728
signature = 'trCkHit07NZUayjGLxJa6FoPnaGHkqPy2JyNjlUbxzcc3aGvsExCmHXi6XJGuoCu6M2RMXiLzIftEm6PAoy1BQ=='

message = (b'ton-proof-item-v2/'
         + 0 .to_bytes(4, 'big') + si.bytes_hash()
         + 28 .to_bytes(4, 'little') + b'ratingers.pythonanywhere.com'
         + received_timestamp.to_bytes(8, 'little')
         + b'doc-example-<BACKEND_AUTH_ID>')
# b'ton-proof-item-v2/\x00\x00\x00\x00\xb2\xa1\xec\xf5T^\x07l\xd3j\xe5\x16\xea~\xbd\xf3*\xea\x00\x8c\xaa+\x84\xaf\x98f\xbe\xcb \x88\x95\xad\x1c\x00\x00\x00ratingers.pythonanywhere.com\x984\xcdc\x00\x00\x00\x00doc-example-<BACKEND_AUTH_ID>'

signed = b'\xFF\xFF' + b'ton-connect' + hashlib.sha256(message).digest()
# b'\xff\xffton-connectK\x90\r\xae\xf6\xb0 \xaa\xa9\xbd\xd1\xaa\x96\x8b\x1fp\xa9e\xff\xdf\x81\x02\x98\xb0)E\t\xf6\xc0\xdc\xfdx'

verify_key.verify(hashlib.sha256(signed).digest(), base64.b64decode(signature))
# b'\x0eT\xd6\xb5\xd5\xe8HvH\x0b\x10\xdc\x8d\xfc\xd3#n\x93\xa8\xe9\xb9\x00\xaaH%\xb5O\xac:\xbd\xcaM'
```

Now, if attacker tries to impersonate someone and doesn't provide valid signature, we will get error: `nacl.exceptions.BadSignatureError: Signature was forged or corrupt`.

## Next steps

When writing your dApp, here's a list of things you should consider as well:
- after successful connection (either restored or new), you should display `Disconnect` button instead of a few `Connect` ones;
- when user disconnects, you'll need to recreate `Connect` buttons;
- wallet code should be checked, because
   - newer wallet versions could place public key in a different location, and
   - currently user may sign in not with wallet but with some other contract, which will luckily contain his public key in expected location.

Good luck and have fun writing dApps!
