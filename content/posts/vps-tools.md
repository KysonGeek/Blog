+++
title = "VPS 工具"
date = 2025-09-24
weight = 20250924

[taxonomies]
tags = ["vps", "工具"]

[extra]
+++

[全球延迟](https://tools.bunny.net/latency-test)
## realm转发
```
wget -qO- https://raw.githubusercontent.com/zywe03/realm-xwPF/main/xwPF.sh | sudo bash -s install
```
## 节点搭建
```
bash <(wget -qO- -o- https://github.com/233boy/sing-box/raw/main/install.sh)
```
## snell服务端多端口监听
```
wget https://raw.githubusercontent.com/KysonGeek/scripts/refs/heads/main/snell.sh
chmod +x snell.sh
./snell.sh
```

## tcping

```
sudo wget http://www.vdberg.org/~richard/tcpping -O /usr/bin/tcping
sudo chmod +x /usr/bin/tcping

```

## snell
```
wget -O snell.sh --no-check-certificate https://git.io/Snell.sh && chmod +x snell.sh && ./snell.sh
```
## 命令小抄
```
bash <(curl -sL https://sh.nodeseek.com)
```

## dd脚本
```
wget --no-check-certificate -qO InstallNET.sh 'https://raw.githubusercontent.com/leitbogioro/Tools/master/Linux_reinstall/InstallNET.sh' && chmod a+x InstallNET.sh && bash InstallNET.sh -debian 12 -pwd 'password'
```

## systemctl
```
systemctl list-units --type=service
``` 

## 关闭ipv6
```
sudo nano /etc/sysctl.conf
```
```
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
```
```
sudo sysctl -p
```
测试
```
getent ahosts google.com
// 检查
sysctl net.ipv6.conf.all.disable_ipv6
sysctl net.ipv6.conf.default.disable_ipv6
// 手动处理
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=0
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=0
```
