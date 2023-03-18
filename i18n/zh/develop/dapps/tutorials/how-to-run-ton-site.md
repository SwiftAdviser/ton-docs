# How to run TON Site

## 👋 Introduction

[TON Sites](/learn/services/sites-www-proxy) work almost like regular sites except for their installation. A number of additional actions are required to launch them. In this tutorial I will show you how to do it.

## 🖥 Running TON Site

There are two ways to do this. The first is to use a docker. This method is easier because docker will do all the complex actions for you.

The second method is Installing from sources manually. This method is longer and may cause difficulties for not experienced users.

### 📦 Running with Docker

There is an easy-to-use docker container for [TON Proxy](/participate/web3/sites-and-proxy) with which you can run TON Site:
https://github.com/kdimentionaltree/ton-proxy-docker

Before you start, make sure that you already have a regular website running on port 80. We will consider installing on a Linux machine, but the same steps can be performed on other operating systems.

1.  Download Docker container:
```bash
git clone https://github.com/kdimentionaltree/ton-proxy-docker.git
```

2.  Build TON Proxy with docker:
```bash
cd ton-proxy-docker
docker-compose build
```

3.  Generate a persistent [ADNL](/learn/networking/adnl) address for your server:
```bash
./init.sh
```
You see something like
```
45061C1D4EC44A937D0318589E13C73D151D1CEF5D3C0E53AFBCF56A6C2FE2BD vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3
```
This is your newly-generated persistent ADNL address, in hexadecimal and user-friendly form.

4.  Run proxy in reverse mode:
```bash
docker-compose up -d
```

### ⚙️ Installing from sources

Otherwise, if you don't want to use [Docker](#-running-with-docker), you can download the sources and install it manually.

Before you start, make sure that you already have a regular website running on port 80. We will consider installing on a Linux machine, but the same steps can be performed on other operating systems.

1.  Download the newest version of the TON blockchain sources, available at GitHub repository https://github.com/ton-blockchain/ton/:
```bash
git clone --recurse-submodules https://github.com/ton-blockchain/ton.git
```

2.  Install the newest versions of `make`, `cmake`, `clang`, `OpenSSL` and some other packets:
```bash
apt update
apt install build-essential cmake clang-6.0 openssl libssl-dev zlib1g-dev
```

3.  Suppose that you have fetched the source tree to directory `~/ton`, where `~` is your home directory, then create an empty directory `~/ton-build` and open it:
```bash
mkdir ton-build
cd ton-build
```

4.  Compile with `cmake`:
```bash
cmake ../ton
```

5.  Download Global Config:
```bash
wget https://ton-blockchain.github.io/global.config.json
```

6.  Compile `RLDP-HTTP-Proxy` and `generate-random-id`:

You can read more about RLDP [here](/learn/networking/rldp)

```bash
cmake --build . --target rldp-http-proxy
cmake --build . --target generate-random-id
```

7.  Generate a persistent ADNL address for your server:
```bash
mkdir keyring
utils/generate-random-id -m adnlid
```
You see something like
```
45061C1D4EC44A937D0318589E13C73D151D1CEF5D3C0E53AFBCF56A6C2FE2BD vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3
```
This is your newly-generated persistent ADNL address, in hexadecimal and user-friendly form. The corresponding private key is saved into file `45061...2DB` in the current directory. Move it into the `keyring` directory:
```bash
mv 45061C1* keyring/
```

8. Run proxy in reverse mode:
```bash
rldp-http-proxy/rldp-http-proxy -a <your-server-ip>:3333 -L '*' -C global.config.json -A <your-adnl-address> -d -l <log-file>
```
where <your_public_ip> is your server public IPv4 address and <your_adnl_address> is ADNL address generated in the previous step.
Example:
```bash
rldp-http-proxy/rldp-http-proxy -a 10.132.46.154:3333 -L '*' -C global.config.json -A vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3 -d -l tonsite.log
```

## 👀 Further steps

### 🔍 Сhecking availability of the site

After completing all the steps of the method you selected, the TON Proxy should have started. If everything was successful, your site will be available at the ADNL address received at the corresponding step. 

You can check the availability of the site by opening this address with the domain `.adnl`. Also note that in order for the site to open, you must have a TON Proxy running in your browser, for example through an extension [MyTonWallet](https://mytonwallet.io/).

### 📎 Linking TON DNS domain

To link a [TON DNS domain](/participate/web3/dns) domain to your site, follow these steps:

1.  Open the domain page on [dns.ton.org](https://dns.ton.org)

2.  Click the `Edit` button

3.  Enter your site's ADNL address in `TON site` field and click `set`

In a few minutes you will be able to access your website using the chosen domain if you have TON Proxy enabled.

## 📌 References

 * [TON Sites, TON WWW and TON Proxy](/learn/services/sites-www-proxy/)
 * [TON DNS](/learn/services/dns/)
 * [TON Web3 Overview](/participate/web3/overview/)
 * [Site & Domain Management](/participate/web3/site-management)
 * Author: [Andrew Burnosov](https://github.com/AndreyBur) (TG: [@AndrewBurnosov](https://t.me/AndreyBurnosov))