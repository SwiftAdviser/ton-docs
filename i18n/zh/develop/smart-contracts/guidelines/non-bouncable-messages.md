# Non-bounceable messages

export const Highlight = ({children, color}) => (
<span
style={{
backgroundColor: color,
borderRadius: '2px',
color: '#fff',
padding: '0.2rem',
}}>
{children}
</span>
);

Almost all internal messages sent between smart contracts should be bounceable, i.e., should have their "bounce" bit set. Then, if the destination smart contract does not exist, or if it throws an unhandled exception while processing this message, the message will be "bounced" back carrying the remainder of the original value (minus all message transfer and gas fees). The body of the bounced message will contain 32 bit `0xffffffff` followed by 256 bit from original message, but with the "bounce" flag cleared and the "bounced" flag set. Therefore, all smart contracts should check the "bounced" flag of all inbound messages and either silently accept them (by immediately terminating with a zero exit code) or perform some special processing to detect which outbound query has failed. The query contained in the body of a bounced message should never be executed.

:::info
The query contained in the body of a bounced message <Highlight color="#186E8A"> should never be executed</Highlight>.
:::

On some occasions, `non-bounceable internal messages` must be used. For instance, new accounts cannot be created without at least one non-bounceable internal message being sent to them. Unless this message contains a `StateInit` with the code and data of the new smart contract, it does not make sense to have a non-empty body in a non-bounceable internal message.

:::tip
It is a good idea `not to allow` the end user (e.g., of a wallet) to send unbounceable messages containing large amounts of value (e.g., more than five Toncoins) or to warn them if they do. It is a `better idea` to send a small amount first, then initialize the new smart contract, and then send a larger amount.
:::