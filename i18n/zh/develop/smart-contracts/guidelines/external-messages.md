# External messages


External messages are `sent from the outside` to the smart contracts residing in the TON Blockchain to make them perform certain actions. 

For instance, a wallet smart contract expects to receive external messages containing orders (e.g., internal messages to be sent from the wallet smart contract) signed by the wallet's owner. When such an external message is received by the wallet smart contract, it first checks the signature, then accepts the message (by running the TVM primitive `ACCEPT`), and then performs whatever actions are required.

:::danger
Notice that all external messages `must be protected` against replay attacks. The validators normally remove an external message from the pool of suggested external messages (received from the network); however, in some situations `another validator` could process the same external message twice (thus creating a second transaction for the same external message, leading to the duplication of the original action). Even worse, a `malicious actor could extract` the external message from the block containing the processing transaction and re-send it later. This could force a wallet smart contract to repeat a payment, for example.
:::

export const Highlight = ({children, color}) => (
<span
style={{
backgroundColor: color,
borderRadius: '2px',
color: '#4a080b',
padding: '0.2rem',
}}>
{children}
</span>
);


The <Highlight color="#ffeced">simplest way to protect smart contracts from replay attacks</Highlight> related to external messages is to store a 32-bit counter `cur-seqno` in the persistent data of the smart contract, and to expect a `req-seqno` value in (the signed part of) any inbound external messages. Then an external message is accepted only if both the signature is valid and `req-seqno` equals `cur-seqno`. After successful processing, the `cur-seqno` value in the persistent data is increased by one, so the <Highlight color="#ffeced">same external message will never be accepted again</Highlight>.

And <Highlight color="#ffeced">One could also</Highlight> include an `expire-at` field in the external message, and accept an external message only if the current Unix time is less than the value of this field. This approach can be used in conjunction with `seqno`; alternatively, the receiving smart contract could store the set of (the hashes of) all recent (not expired) accepted external messages in its persistent data, and reject a new external message if it is a duplicate of one of the stored messages. Some garbage collection of expired messages in this set should also be performed to avoid bloating the persistent data.

:::note
In general, an external message begins with a 256-bit signature (if needed), a 32-bit `req-seqno` (if needed), a 32-bit `expire-at` (if needed), and possibly a 32-bit `op` and other required parameters depending on `op`. The layout of external messages does not need to be as standardized as that of internal messages because external messages are not used for interaction between different smart contracts (written by different developers and managed by different owners).
:::