# Site & Domain Management

## How to open a domain for editing

1. Open the Google Chrome browser on your computer.

2. Install the Google Chrome TON extension from this [link](https://chrome.google.com/webstore/detail/ton-wallet/nphplpgoakhhjchkkhmiggakijnkhfnd).

3. Open the extension, click "Import wallet" and import the wallet where the domain is stored.

> Recovery Phrases
>
> Your recovery phrase is the 24 words you wrote down when you created your wallet.
>
> If you lost your phrase, you can restore it using any TON Wallet.
> In Tonkeeper: Settings > Wallet protection > Your private key.
>
> Be sure to write down these 24 words and keep them in a safe place. In case of emergency, you will be able to restore access to the wallet only by recovery phrases.
> Keep your recovery phrases strictly confidential. Anyone who gains access to your recovery phrases will have full access to your funds.

4. Now open your domain on https://dns.ton.org and click the "Edit" button.

## How to link a wallet to a domain

You can link a wallet to a domain, in which case users will be able to send coins to that wallet by entering the domain as the recipient address instead of the wallet address.

1. Open the domain for editing as described above.

2. Copy your wallet address into the "Wallet address" field and click "Save".

3. Confirm sending the transaction in the extension.

## How to link a TON Site to a domain

1. Open the domain for editing as described above.

2. Copy the ADNL Address of your TON Site in HEX format into the "Site" field and click "Save".

3. Confirm sending the transaction in the extension.

## How to set up subdomains


1. Create a smart contract on the network that will manage the subdomains of your website or service. You can use ready-made [manual-dns](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/dns-manual-code.fc) or [auto-dns](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/dns-auto-code.fc) smart contracts, or any other smart contract that implements the TON DNS interface.

2. Open the domain for editing as described above.

3. Copy the smart contract address of the subdomains in the "Subdomains" field and click "Save".

4. Confirm sending the transaction in the extension.


