# TON Sites, TON WWW and TON Proxy

![image](/img/docs/main_pic.png)

The TON Project is more than just a blockchain — it also has a unique network technology.

First of all, network protocols were created specifically for TON Blockchain so that nodes could communicate with one another and exchange data. Currently, the network hosts solutions which are so powerful and universal that, together, they are equivalent to a next generation internet.

The TON Network is interesting itself, not even considering TON Blockchain, because it is a fully decentralized, secure and private computer network akin to __[TOR](https://en.wikipedia.org/wiki/Tor_(network))__ or the __[I2P (Invisible Internet Project)](https://en.wikipedia.org/wiki/I2P)__.

TON Network is deeply integrated with TON Blockchain, the project’s native Toncoin cryptocurrency and TON Services — it creates a synergy, elevating the network’s technology to a whole new level.

## TON Network

* **Decentralized**: A peer-to-peer network that has no centralized servers.
* **Stable**: Nodes that go offline have no effect on the network’s functionality.
* **Anonymous**: It’s impossible or difficult to identify a node's IP address.
* **Encrypted**: Data is encrypted when sent to nodes.
* The network uses the UDP/IP and TCP/IP internet protocols.


You can find a more technical explanation of the protocols on the TON Network in Chapter 3 of The Open Network’s __[White Paper](/learn/docs)__.

### TON Blockchain relies on TON Network

For the last three years since the project’s inception, TON Blockchain’s nodes (validators, server, etc.) have been communicating with one another with the help of the TON Network, the combination of which has proved to be stable and effective in practice.

As operations on the blockchain become more complex, more powerful network solutions will eventually be required. The TON Network fully meets the needs of a latest generation blockchain; for example, when TON Blockchain divides into sub-blockchains due to high throughput, each sub-blockchain use its own individual sub-network.

## TON Sites

![image](/img/docs/ton_sites.png)

TON Blockchain is not the only thing that uses TON Network.

Starting today, you can launch a web server with your website and make it available on the TON Network (i.e. you can make a TON Site).

Read the guide __[here](/learn/services/sites-www-proxy)__.

### Mandatory encryption and verifying the authenticity of data

In the early days of the current version of the Internet, all data between users and websites (e.g. conversations on chats) was always exposed where it could be read by someone else on the internet. There was also no way to confirm whether data was altered in transit.

In time, HTTPS appeared, which encrypted and authenticated data.

For over 15 years, HTTPS has been proliferating across the internet; however, around 20% of websites __[don’t use this protocol](https://letsencrypt.org/stats/#percent-pageloads)__ by default.

Nevertheless, there is always the possibility of users’ data being sent through unencrypted channels.

In light of this, the TON Network has its own __mandatory__ encryption and automatically verifies the authenticity of all data traffic.

### No more need for certification authorities

To receive encryption and verify the authenticity of data, regular websites need to have a special certificate. Technically, you can create this certificate yourself, but on the Internet it will not be considered as trustworthy. Usually, certificates can be obtained at certification authorities - some cost money and others are free.

It’s assumed that the authorities check the site’s owner; however, in reality, even expensive __[extended-certificates](https://en.wikipedia.org/wiki/Extended_Validation_Certificate#Criticism)__ aren't always awarded only after due diligence.

In short, these certification authorities are neither effective nor productive.

TON Sites provides encryption and authenticity verification of data via built-in cryptography. Your site will be immediately secure without having to go to any certification authorities.

### No more need for domain names registries

![image](/img/docs/foundation_ton.png)

For regular websites, you rent a domain name from a commercial entity (i.e. a centralized domain name registry).

The biggest problem is that your domain name can be blocked or taken away from you for arbitrary, unknown reasons or erroneously.

Anyone can write to a domain name registry, saying that your website is engaging in illegal activity. It would be a false claim, but the registry’s employee would have to block your site, even without having all the details to fully understand the situation. This would inevitably lead to a lot of headaches and large losses.

TON Sites uses __[TON DNS](/learn/services/dns)__, a fully decentralized domain name system.

Incumbent domain registries require owners to make non-trivial payments, which go to pay for employees and other expenses, whereas with TON DNS, all you have to do is make an annual micropayment as a symbolic “sign of life” to confirm domain ownership.

__[How to link a TON Site to a domain](/participate/web3/site-management#how-to-link-a-ton-site-to-a-domain)__

### Sub-domains

![image](/img/docs/Sub-domains_ton.png)


Like with regular sites, you can have a sub-domain for your TON Site with the help of TON DNS.

To do so, you can use any suitable smart contract.

We’ve developed a few ready-made smart contracts.

With a __[Manual-DNS](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/dns-manual-code.fc)__ Smart Contract, a site’s owner can assign any page to any sub-domain.

If you’re the owner of a service, you can use the __[Auto-DNS](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/dns-auto-code.fc)__ Smart Contract. Users can register a sub-domain to themselves by paying a network fee and an optional payment to the service.

For example, the social network place.ton could allow Alice to independently register alice.place.ton as her personal page by paying a small amount of Toncoin.

You can go one step further and have a full-blown auction for an NFT sub-domain, the same way the first “.ton” domains are __[distributed](https://dns.ton.org)__.

## TON WWW

### Domain names

<div style={{textAlign:'center', margin: '0 auto'}}>
  <video width="300" style={{borderRadius:'10pt', margin:'15pt auto'}} muted={true} autoPlay={true} loop={true}>
    <source src="/docs/img/docs/ton_www.mp4" type="video/mp4" />
  </video>
</div>

Let’s say you go to the http://foundation.ton site and want to donate 10 TON towards the network’s development. How would you do that?

It’s simple: Just send 10 TON from your wallet directly to this domain. No other payments or details are required.

The same is true for sub-domains. Let’s say you go to Alice’s personal page at alice.place.ton on the place.ton social network.

You can send 10 TON as a gift to Alice by entering alice.place.ton as the recipient’s address and Alice will receive the TON in the crypto wallet which she assigned to her account when she created it.

### Authorization

<div style={{textAlign:'center', margin: '0 auto'}}>
  <video width="300" style={{borderRadius:'10pt', margin:'15pt auto'}} muted={true} autoPlay={true} loop={true}>
    <source src="/docs/img/docs/autorization.mp4" type="video/mp4" />
  </video>
</div>

On the internet, you have to register and create a new and different password for every website. This quickly becomes annoying and inconvenient even if you factor in password manager apps. Inexperienced users defer to using one and the same password for all websites with which they interact, which is dangerous.

Besides passwords, logins require an email address or phone number that will immediately become the target of ads.

On TON, there’s no need to register. On a site or in an app, you can sign in with your TON Crypto Wallet — you won’t need to reveal your email address or create a different password for every new service.

### Hyperlinks

<div style={{textAlign:'center', margin: '0 auto'}}>
  <video width="300" style={{borderRadius:'10pt', margin:'15pt auto'}} muted={true} autoPlay={true} loop={true}>
    <source src="/docs/img/docs/hyperlinks.mp4" type="video/mp4" />
  </video>
</div>

The World Wide Web is made up of internet sites with web pages whose text can contain __hyperlinks__ which allows users to go from one resource to another seamlessly or to initiate some kind of action (e.g. open an email client).

TON Sites are similar to regular websites, but they’re accessible via the TON network. Their URLs also look similar to regular websites, but they end in “.ton” (e.g. [http://foundation.ton](http://foundation.ton/)).

TON has its own format for hyperlinks to initiate actions:
```bash
ton://domain/<method>?<field1>=<value1>&<field2>=..
```
For example:
```bash
ton://EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N/transfer?amount=1&text=hello
```
Clicking on this link will open the TON Crypto Wallet with the recipient’s address, the crypto amount and any other relevant data.

Web page developers can also use scripts that interact with your TON Wallet or TON Browser Extension.



Everything mentioned above is what creates TON WWW: the collection of web pages and services on TON, which link to one another and are accessible via a TON Crypto Wallet and a web browser.

## TON Proxy

To gain access to the TON Network, first, users must connect to a special entry point. In technical terms, this is called an "entry proxy".

Currently, you can use __[public entry points](/participate/web3/setting-proxy#public-entry-ton-proxies)__ launched by TON Foundation.

__|__ _Use public entry points along with HTTP for trial purposes only, as in this case, traffic outside the TON Network is not encrypted_

Tech-savvy users can already __[launch entry proxies](/participate/web3/sites-and-proxy#running-entry-proxy-on-remote-computer)__ directly on their devices — in the near future, this will become available to all users in the form of a simple application.

### In a browser
![image](/img/docs/in_a_browser.jpg)

Because TON Proxy is compatible with HTTP Proxy, you can simply open the settings in your browser or system settings and enter the address of a public TON Entry Proxy as a proxy server.

You’ll then be able to open “.ton” sites directly in your browser, just like regular websites.

Here’s a __[guide](/participate/web3/setting-proxy)__ on setting up TON Proxy for various browsers.

### Wallets

<div style={{textAlign:'center', margin: '0 auto'}}>
  <video width="600" style={{borderRadius:'10pt', margin:'15pt auto'}} muted={true} autoPlay={true} loop={true}>
    <source src="/docs/img/docs/wallets.mp4" type="video/mp4" />
  </video>
</div>

Things can always be simpler. Various TON Wallets have said that they wish to implement TON Proxy directly in the wallet’s app to avoid downloading extra apps.

At the moment, this is possible through a __[MyTonWallet](https://mytonwallet.io)__ Google Chrome extension: Click to switch to TON Proxy and your browser will be able to open TON sites.

This functionality will soon be available in the standard TON Chrome Extenstion,  Tonkeeper and other TON Wallet Apps.

## The next steps
We’re awaiting two monumental updates dedicated to privacy and decentralized finance.

### TON Proxy 2.0 — Privacy

In our opinion, the main red flag of the Internet is that a user’s IP Address and the site’s IP Address are both open and visible to everyone.

In the TON Proxy 2.0 update, a new functionality will allow people to launch intermediary proxy nodes on the TON Network; meanwhile, data between users and sites or services will travel through a swarm of intermediary nodes via __[garlic routing](https://en.wikipedia.org/wiki/Garlic_routing)__.

This will mask the IP Addresses of users and sites completely.

Anyone will be able to run intermediary nodes. At that point, they’ll be free like TOR or I2P. This will allow a large number of users to try the technology.

### Site security

Most websites, if it’s not a home page, use services such as CloudFlare or Akamai to mask the true IP address of a site and protect against DDoS attacks and hacks.

These kinds of services are good; however, they are centralized commercial companies. As it stands, these companies host a large slice of the internet and when one of them experiences a __[critical emergency](https://t.me/tonblockchain/136)__ it goes offline, turning off access to half the internet.

We see more stable and better solutions when the security of a site’s IP Address is provided through the system of decentralized nodes belonging to TON Proxy.

### Privacy for users

A user’s IP Address is exposed by default. Not only can this be a vector through which hackers could gain access to someone’s device but corporations use these same means to glean massive amounts of data on users. By juxtaposing IP Addresses, corporations can learn what sites you visit even if you haven’t created an account on it.

With TON Proxy, internet traffic will be rerouted through one of many intermediary proxies so that the end site or service will never know your real IP Address.

:::info
Starting with the TON Proxy 2.0 version, full anonymity will be available in the TON Network.
:::

### TON Proxy 3.0 — Decentralized finance

For the third stage, decentralized Toncoin economy will launch for the use of intermediary TON Proxies, which provide privacy to users and security to sites.

The payment will occur through the Payment Network technology, a network of payment channels __[developed](/learn/services/payments)__ in Q2 2022. An intermediary proxy node is going to receive micropayments for internet traffic packages (e.g. for 128 KiB) that run through it. These micropayments will be charged and deducted from users’ crypto wallets.

Thanks to this decentralized payments system, independent administrators will be able to run intermediary proxy nodes in various parts of the world, which will increase the effectiveness and speed of the network and make it more scalable and stable.

We believe that one of the main reasons why networks such as I2P or TOR haven’t been able to scale for 20 years is because of the absence of financial incentives for those who labor to support the network.

## Conclusion
The modern Internet has been operating on protocols developed in the __[1990s](https://www.rfc-editor.org/rfc/rfc1945)__, and some are even from the __[80s](https://www.rfc-editor.org/rfc/rfc791)__.

We have to pay our respects to the first developers whose many creations have stood the test of time: The Internet was able to adapt to billions of users and establish new means to consume content.

However, privacy and security of that same modern Internet have no response to the growing needs of the current day.

The Internet managed to integrate deeply into our lives and will only go deeper. Video cameras on every street corner, fitness bracelets, self-checkouts in stores — all of these electronic devices monitor everything we do in our day-to-day lives.

As soon as this information falls into the hands of bad actors or thieves, it becomes a threat not only to our image or assets.

Already, detailed personal information can become a threat to our lives and the lives of people close to us. But soon, when electronic heart valves become connected to networks, it will become life-threatening — literally.

Another glaring issue is how large corporations have monopolized the internet. Infrastructure companies create narrow spaces, making the internet __[fragile](https://t.me/tonblockchain/46)__. Corporations glean a huge amount of user data, which is sold to third parties or leaks in hacker attacks.



Today, we’re taking the first step toward solving this problem by opening the TON Network to users and launching TON Proxy and TON Sites with TON DNS integration, all of which are decentralized, secure, and reliable services that surpass the familiar WWW in terms of usability.


