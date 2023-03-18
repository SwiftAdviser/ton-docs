# Compile TON on a low-memory machines

:::caution
This section describes instructions and manuals for interacting with TON at a low level.
:::

Creating a swap partitions to compile TON on a computer with low memory (less than 1GB).

## Prerequisites

During C++ compilation in the Linux system the following errors occur, resulting in a compilation abort:

```
C++: fatal error: Killed signal terminated program cc1plus compilation terminated.
```

## Solution

This occurs due to a lack of memory and is solved by creating a swap partitions.

```bash
# Create the partition path
sudo mkdir -p /var/cache/swap/
# Set the size of the partition
# bs=64M is the block size, count=64 is the number of blocks, so the swap space size is bs*count=4096MB=4GB
sudo dd if=/dev/zero of=/var/cache/swap/swap0 bs=64M count=64
# Set permissions for this directory
sudo chmod 0600 /var/cache/swap/swap0
# Create the SWAP file
sudo mkswap /var/cache/swap/swap0
# Activate the SWAP file
sudo swapon /var/cache/swap/swap0
# Check if SWAP information is correct
sudo swapon -s
```

Command to delete swap partition:

```bash
sudo swapoff /var/cache/swap/swap0
sudo rm /var/cache/swap/swap0
```

Free space command:

```bash
sudo swapoff -a
#Detailed usage: swapoff --help
#View current memory usage: --swapoff: free -m
```