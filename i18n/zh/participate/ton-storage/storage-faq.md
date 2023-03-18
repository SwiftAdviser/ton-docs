# TON Storage FAQ

## How to assign a TON domain to a TON Storage bag of files

1. [Upload](/participate/ton-storage/storage-daemon#creating-a-bag-of-files) the bag of files to the network and get the Bag ID

2. Open the Google Chrome browser on your computer.

3. Install [TON extension](https://chrome.google.com/webstore/detail/ton-wallet/nphplpgoakhhjchkkhmiggakijnkhfnd) for Google Chrome.
   You can also use [MyTonWallet](https://chrome.google.com/webstore/detail/mytonwallet/fldfpgipfncgndfolcbkdeeknbbbnhcc).

4. Open the extension, click "Import wallet" and import the wallet that owns the domain, using the recovery phrase.

5. Now open your domain at https://dns.ton.org and click "Edit".

6. Copy your Bag ID into the "Storage" field and click "Save".

## How to host static TON site in TON Storage

1. [Create](/participate/ton-storage/storage-daemon#creating-a-bag-of-files) the Bag from folder with website files, upload it to the network and get the Bag ID. Folder must contain `index.html` file.

2. Open the Google Chrome browser on your computer.

3. Install [TON extension](https://chrome.google.com/webstore/detail/ton-wallet/nphplpgoakhhjchkkhmiggakijnkhfnd) for Google Chrome.
   You can also use [MyTonWallet](https://chrome.google.com/webstore/detail/mytonwallet/fldfpgipfncgndfolcbkdeeknbbbnhcc).

4. Open the extension, click "Import wallet" and import the wallet that owns the domain, using the recovery phrase.

5. Now open your domain at https://dns.ton.org and click "Edit".

6. Copy your Bag ID into the "Site" field, select "Host in TON Storage" checkbox and click "Save".

## How to migrate TON NFT content to TON Storage

If you used a [standard NFT smart contract](https://github.com/ton-blockchain/token-contract/blob/main/nft/nft-collection-editable.fc) for your collection, you need to send a [message](https://github.com/ton-blockchain/token-contract/blob/2d411595a4f25fba43997a2e140a203c140c728a/nft/nft-collection-editable.fc#L132) to the collection smart contract from the collection owner's wallet with a new url prefix.

As an example, if the url prefix used to be https://mysite/my_collection/, the new prefix will be tonstorage://my_bag_id/.

## How to assign a TON domain to a TON Storage bag (Low Level)

You need to assign the following value to the sha256("storage") DNS Record of your TON domain:

```
dns_storage_address#7473 bag_id:uint256 = DNSRecord;
```

## How to host static TON site in TON Storage (Low Level)

[Create](/participate/ton-storage/storage-daemon#creating-a-bag-of-files) the Bag from folder with website files, upload it to the network and get the Bag ID. Folder must contain `index.html` file.

You need to assign the following value to the sha256("site") DNS Record of your TON domain:

```
dns_storage_address#7473 bag_id:uint256 = DNSRecord;
```

