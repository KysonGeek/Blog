+++
title = "将夸克网盘挂载到vps"
date = 2025-12-02
weight = 20251202
description = "使用夸克网盘的webdav服务可以将百度夸克网盘挂载到本地电脑上，就像操作本地电脑硬盘一样操作网盘，非常方便。"

[taxonomies]
tags = ["vps", "工具"]

[extra]
+++
## 使用开源工具开始夸克网盘的[WebDAV](https://zh.wikipedia.org/wiki/WebDAV)服务

1. 下载工具

   ```bash
   wget https://github.com/chenqimiao/quarkdrive-webdav/releases/download/v1.3.3/quarkdrive-webdav-x86_64-unknown-linux-gnu.tar.gz
   tar -zxvf quarkdrive-webdav-x86_64-unknown-linux-gnu.tar.gz
   ```

2. 运行工具

   ```bash
   quarkdrive-webdav --quark-cookie '你的cookie' -U '用户名' -W '密码' -p 8080
   ```

   cookie可以在夸克网页登录后通过控制台获取

3. 设置开机启动

   ```bash
   cat <<EOF > /etc/systemd/system/quark.service
   [Unit]
   Description=Quark Service
   After=network.target
   
   [Service]
   Type=simple
   ExecStart=/root/quark/start-quark.sh
   Restart=always
   User=root
   
   [Install]
   WantedBy=multi-user.target
   EOF
   systemctl daemon-reload
   systemctl enable quark
   
   ```
   ```
   #!/bin/bash
   /root/quark/quarkdrive-webdav --quark-cookie "$(cat /root/quark/cookie.txt)" -U kyson -W liugeliu -p 8082
   ```
   cookie比较长，可以放在`/root/quark/cookie.txt`中

## 将WebDAV挂载到vps

1. 安装工具

```bash
apt install davfs2
```

2. 创建挂载目录

```bash
mkdir /path/webdav
```

3. 挂载 WebDAV

```bash
mount -t davfs https://webdav.drive.com/dav  /path/webdav
```

4. 输入账号密码

使用以上挂载命令后就会让输入账号密码，填入第一步设置的账号密码

5. 配置开机启动

```bash
vi /etc/davfs2/davfs2.conf
```

修改打开use_locks参数，将value从原来的**1**，改为**0**

5.1 修改davfs2的secrets文件，添加认证信息

将webdav的地址以及用户名密码输入到最底部。

```bash
cat <<EOF >> /etc/davfs2/secrets
https://webdav.drive.com/dav  用户名  密码
EOF
```

5.2 配置systemd文件

⚠️注意：通常情况下，挂载单元文件（mount unit）的命名是按照要**挂载的路径**来命名的。这种命名约定是由systemd规定的，以便于自动识别和处理挂载点。如挂载点 `/mnt/data` 的挂载单元文件应命名为 `mnt-data.mount`

```bash
cat <<EOF >> /etc/systemd/system/path-webdav.mount
[Unit]
Description=Mount WebDAV Share
After=network-online.target
Wants=network-online.target

[Mount]
What=https://webdav.drive.com/dav  #修改为自己的webdav地址
Where=/path/webdav                 #修改为自己的挂载路径
Type=davfs 
Options=_netdev,users,rw

[Install]
WantedBy=multi-user.target
EOF
```

保存后重新加载systemd配置并启动

```bash
systemctl daemon-reload
systemctl enable path-webdav.mount
```

最后可以使用`df -h`查看一下是否生效

## 引用
- [Linux使用davfs2挂载webdav作为本地磁盘并实现自动挂载](https://www.yunieebk.com/davfs2/)

