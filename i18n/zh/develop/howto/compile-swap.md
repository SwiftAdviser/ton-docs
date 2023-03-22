# 在記憶體較低的機器上編譯 TON

:::caution
本節提供與 TON 進行低層級互動的指令和手冊。
:::

在記憶體較低（少於1GB）的電腦上編譯 TON，可以創建交換分區。

## 先決條件

在 Linux 系統中進行 C++ 編譯時，會發生以下錯誤，導致編譯中止：


```
C++: fatal error: Killed signal terminated program cc1plus compilation terminated.
```

## 解決方案

這個問題是由於記憶體不足引起的，可以透過建立交換分區來解決。

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

刪除交換分區的指令如下：

```bash
sudo swapoff /var/cache/swap/swap0
sudo rm /var/cache/swap/swap0
```

查看可用空間的指令如下：

```bash
sudo swapoff -a
#Detailed usage: swapoff --help
#View current memory usage: --swapoff: free -m
```