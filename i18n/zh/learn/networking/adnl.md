# ADNL Protocol

Implementation:
* https://github.com/ton-blockchain/ton/tree/master/adnl

## Overview

The cornerstone of TON is the Abstract Datagram Network Layer (ADNL). 

This is an overlay, peer-to-peer, unreliable (small-size) datagram protocol running on top of a **UDP** in **IPv4** (in the future, IPv6), with an optional **TCP fallback** if UDP is not available.

## ADNL address

Each participant has a 256-bit ADNL Address.

The ADNL Protocol allows you to send (unreliable) and receive datagrams using only  ADNL Addresses. IP Addresses and Ports are hidden by the ADNL Protocol.

An ADNL Address is essentially equal to a 256-bit ECC public key. This public key can be arbitrarily generated, thus creating as many different network identities as the node needs.
However, one must know the corresponding private key in order to receive (and decrypt) messages intended for the recipient address.

In reality, the ADNL Address is not the public key itself; instead, it is a 256-bit SHA256 hash of a serialized TL-object that can describe several types of public keys and addresses depending on its constructor.

## Encryption & security

Normally each datagram sent is signed by the sender and encrypted so that only the recipient can decrypt the message and verify its integrity by the signature.

## Neighbor tables

Normally, a TON ADNL node will have some “neighbor table”, which contains information about other known nodes, such as their abstract addresses, public keys, IP Addresses and UDP Ports. Over time, it will gradually
extend this table using information gathered from these known nodes. This new information can be in the form of answers to special queries or sometimes the removal of obsolete records.

ADNL allows you to set up point-to-point channels and tunnels (a chain of proxies).

A TCP-like stream protocol can be built over ADNL.

## What's next?

* Read more about ADNL in the [Low-Level ADNL article](/learn/networking/low-level-adnl)
* Chapter 3.1 of the [TON Whitepaper](https://ton.org/docs/ton.pdf).
