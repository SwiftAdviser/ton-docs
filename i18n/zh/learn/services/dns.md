# What is TON DNS?

TON DNS is a service for translating human-readable domain names (such as `marketplace.ton` or `candyzoo.gaming.ton`) into TON Network Addresses for accounts, smart contracts, services and network nodes.

## User-friendly TON Addresses

Just like the Internet relies internally on numerical addresses ([IP Addresses](https://en.wikipedia.org/wiki/IP_address)) to identify different connected computers, various entities in the TON Network, such as your TON Wallet, have [raw addresses](https://tonscan.org/address/EQCB8Y_dO37YsKGYoMIxCeq0EZ-pqnz4t2qmmUSLFIrRzleC) that are not necessarily easy to read and remember. A traditional [DNS](https://en.wikipedia.org/wiki/Domain_Name_System) can register meaningful human-readable names such as `amazon.com` to be used instead of the numerical addresses of the Internet. Similarly, TON DNS can register meaningful human-readable names (with the `.ton` extension) to be used instead of the raw internal addresses that are hard to work with.

## Secure, Private and Decentralized DNS

The grand TON Network vision tries to create a version of the Internet that is significantly more secure, private and decentralized. A new Internet that is fairly owned by its users and follows the principles of [Web3](https://en.wikipedia.org/wiki/Web3). The traditional [DNS](https://en.wikipedia.org/wiki/Domain_Name_System) service plays a critical role in the Internet because people rely on human-readable domain names such as `amazon.com` to navigate and find what they need. TON DNS is similar in principle but is more secure, private and fully decentralized.

Internet domain names today are sold by for-profit corporations such as [GoDaddy](https://www.godaddy.com/). They are not directly held by their owners, since registrars like GoDaddy must hold your domain on your behalf. This presents privacy issues because even domains represented as private are not private from the registrar. This also presents security issues because anyone who can convince the registrar that they're you, can effectively hijack your domain.

TON DNS resolves these issues by eliminating intermediaries like GoDaddy. On TON Blockchain,domains are managed by smart contracts instead of for-profit corporations. Domains are purchased by paying Toncoin directly to these contracts. Nobody profits from the sale of names (which are community assets), since all TON proceeds are burned and removed from circulation. The rules of the sale are transparent and immutable, guaranteeing fair and equal access for all. The system is fully private, as no identifying factors or real world identities are stored anywhere. The system is also fully secure, since domain ownership is represented by an NFT which users hold themselves - this is as secure as keeping your private key secret.

## Anonymous Networking Protocol

TON DNS takes the vision of the private Internet a step further. The underlying networking protocol of the TON Network is called ADNL - and one of its features is allowing network entities to remain anonymous. TON DNS can label these anonymous ADNL Addresses with human-readable names to make them easy to access. Consider a website like [WikiLeaks](https://wikileaks.org/) that wants to remain anonymous to resist censorship and avoid prosecution, yet requires a well known name to allow its readers to find it.

Every entity on the TON Network can be labeled by TON DNS; from a wallet address to a validator node, smart contract or any service like TON Sites. To enjoy TON DNS today, end users can install an extension on leading browsers such as Chrome or browse using supporting proxy servers that translate requests automatically. In the future, we can also expect to see TON DNS baked into web browsers directly. Consider Telegram Messenger, which could eventually directly support TON DNS and take advantage of the security, privacy and decentralization it offers in order to facilitate mass adoption.

## Similar projects in other networks

[ENS](https://ens.domains/) (Ethereum Name Service) is a service in the Ethereum ecosystem that is similar in principle to TON DNS. Unlike TON DNS, which is a core service of TON Network, ENS is a [DAO](https://en.wikipedia.org/wiki/The_DAO_(organization)) and not part of the Ethereum protocol. ENS has its own governance token, [ENS](https://coinmarketcap.com/currencies/ethereum-name-service/), that is traded independently from ETH and is used for governance purposes. TON DNS does not have its own separate token and instead relies on Toncoin for its governance and incentives layer - as all TON proceeds from domain sales are burned and removed from circulation for the benefit of all TON holders.

ENS is also limited in mass adoption potential due to the inherent limitations of the Ethereum network. The high cost of gas on Ethereum makes registering billions of subdomains impractical. The cost of registering a subdomain on TON DNS is about 1 cent. TON DNS can easily accomodate a future where every human on earth can securely register and name their assets - everything from an email address to a personal wallet.

## More info

* [TON DNS in Docs](/learn/services/dns)
* [TON DNS Standard](https://github.com/ton-blockchain/TIPs/issues/81)
* [TON DNS in TON Whitepaper - Section 4.3](https://ton-blockchain.github.io/docs/ton.pdf)
* [TON DNS Auction Client](https://dns.ton.org/)