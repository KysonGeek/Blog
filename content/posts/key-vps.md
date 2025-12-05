+++
title = "密钥登录vps"
date = 2025-10-20
weight = 20251020

[taxonomies]
tags = ["vps","工具"]

[extra]
+++

## 1. 生成密钥
```
ssh-keygen -t ed25519 -C "gen2" -f ~/.ssh/id_ed25519_gen2
```

## 2. 密钥上传到vps
```
mkdir -p ~/.ssh
chmod 700 ~/.ssh
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

//或者通过命令上传
ssh-copy-id -p 11017 -i id_ed25519_gen2.pub maxchan@ip
```

## 3. 测试密钥登录
```
ssh -i ~/.ssh/id_ed25519 root@你的VPSIP
```

## 4. 删除密码登录
```
vim /etc/ssh/sshd_config

PasswordAuthentication no
PubkeyAuthentication yes
```

## 5.重启ssh服务
```
sudo systemctl restart ssh
```
