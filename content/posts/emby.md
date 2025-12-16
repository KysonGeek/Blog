+++
title = "使用夸克网盘搭建emby"
date = 2025-12-16
weight = 20251216
description = "夸克+webdav+CloudDrive2+AutoSymlink+Emby自建影视库"

[taxonomies]
tags = ["技术", "emby"]

[extra]
+++

## 使用开源工具挂载夸克网盘的[WebDAV](https://zh.wikipedia.org/wiki/WebDAV)服务

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
   /root/quark/quarkdrive-webdav --quark-cookie "$(cat /root/quark/cookie.txt)" -U admin -W password -p 8082
   ```
   cookie比较长，可以放在`/root/quark/cookie.txt`中

## 将WebDAV挂载到vps

1. 脚本

    ```bash
    cat <<EOF >> /etc/systemd/system/clouddrive.service
    [Unit]
    Description=Clouddrive Service
    Documentation=https://github.com/cloud-fs/clouddrive
    After=network.target network-online.target
    Wants=network-online.target

    [Service]
    Type=simple
    # 这里的 User 和 Group 可以指定特定用户运行，
    # 如果需要挂载 FUSE 文件系统且不涉及权限问题，root (默认) 最为方便。
    # User=root
    # Group=root

    # 重要：指定工作目录，否则 Clouddrive 可能找不到配置文件
    WorkingDirectory=/root/cd2

    # 指定启动命令的完整路径
    ExecStart=/root/cd2/clouddrive

    MountFlags=shared

    # 停止时的操作（可选，Systemd 默认会发送信号终止）
    ExecStop=/bin/kill -s SIGTERM $MAINPID

    # 崩溃或退出后自动重启
    Restart=always
    RestartSec=5

    # 环境变量（如果需要）
    # Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

    [Install]
    WantedBy=multi-user.target
    EOF
    systemctl daemon-reload
    systemctl enable clouddrive
    systemctl start clouddrive
    ```
## 生成strm

```yaml
  auto_symlink:
    image: shenxianmq/auto_symlink:latest
    container_name: auto_symlink
    restart: unless-stopped
    ports:
      - "8095:8095" # 管理后台端口
    volumes:
      # 映射配置目录
      - /var/www/config/auto_symlink:/app/config
      # 映射您的 davfs2 挂载源 (必须加 :rslave 否则容器内看不到内容)
      - /var/www/quark:/var/www/quark:rslave
      # 映射 strm 输出目录
      - /var/www/emby_strm:/var/www/emby_strm
    environment:
      - TZ=Asia/Shanghai
    user: "0:0" # 使用 root 权限以确保能读取挂载点
```

## 配置Emby

```yml
  emby:
    image: emby/embyserver:latest
    container_name: emby
    restart: unless-stopped
    ports:
      - "8096:8096"
    environment:
      - UID=0 # 建议使用 root 避免挂载点权限问题
      - GID=0
      - GIDLIST=0
      - TZ=Asia/Shanghai
    volumes:
      # Emby 配置
      - /var/www/config/emby:/config
      # 关键：Emby 必须能访问 strm 指向的真实路径
      - /var/www/quark:/var/www/quark:rslave
      # 挂载生成的 strm 目录作为媒体库
      - /var/www/emby_strm:/media
```

## 备注
- cd2挂载时设置允许其他用户访问权限
- echo "user_allow_other" > /etc/fuse.conf

> Linux 的 FUSE 挂载默认只允许执行挂载命令的用户（通常是 root）访问
