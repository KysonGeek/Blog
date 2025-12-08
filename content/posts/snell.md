+++
title = "Snell 一键脚本开启多个端口监听"
date = 2025-12-08
weight = 20251208
description = "之前用的snell一键脚本只能创建一个端口，只能和朋友用一个端口不方便。今天用AI糊了个脚本可以开启多个端口监听。"

[taxonomies]
tags = ["vps", "网络"]
[extra]

+++
主要使用的systemctl service的变量功能，将端口当成变量传给service，每个端口启动一个service

将内容保存到snell.sh中，使用下面命令赋予执行权限

```bash
chmod +x snell.sh
```

```bash
./snell install #安装官方snell-service
./snell create 1234 #新增端口
./snell list #查看目前端口列表
```

脚本内容：

```bash
#!/usr/bin/env bash
set -e
snell_server="/etc/systemd/system/snell-server@.service"
snell_bin="/usr/local/bin/snell-server"
snell_dir="/etc/snell"

check_root() {
  [[ $EUID -ne 0 ]] && echo "请使用 root 运行" && exit 1
}

install_binary() {
  mkdir -p "$snell_dir"
  arch=$(uname -m)
  [[ "$arch" == "x86_64" ]] && arch="amd64"
  ver="5.0.0"
  url="https://dl.nssurge.com/snell/snell-server-v${ver}-linux-${arch}.zip"
  wget -qO snell.zip "$url"
  unzip -o snell.zip && mv snell-server "$snell_bin"
  chmod +x "$snell_bin"
  rm -f snell.zip
  cat >"$snell_server" <<EOF
[Unit]
Description=Snell Service
After=network-online.target
Wants=network-online.target systemd-networkd-wait-online.service
[Service]
LimitNOFILE=32767 
Type=simple
User=root
Restart=on-failure
RestartSec=5s
ExecStartPre=/bin/sh -c ulimit -n 51200
ExecStart=${snell_bin} -c ${snell_dir}/config-%i.conf
[Install]
WantedBy=multi-user.target
EOF
}

create_config() {
  port=$1
  [[ -z "$port" ]] && echo "用法: $0 create <port>" && exit 1
  conf="$snell_dir/config-$port.conf"
  [[ -f "$conf" ]] && echo "配置已存在: $conf" && exit 1
  read -p "PSK(留空随机): " psk
  [[ -z "$psk" ]] && psk=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 16)
  cat >"$conf" <<EOF
[snell-server]
listen = 0.0.0.0:${port}
psk = ${psk}
obfs = off
ipv6 = false
tfo = true
dns = 1.1.1.1,8.8.8.8
version = 5
EOF
  echo "已创建 $conf"
}

start_instance() {
  port=$1
  systemctl enable --now snell-server@"$port"
}

stop_instance() {
  port=$1
  systemctl stop snell-server@"$port"
}

list_instances() {
  systemctl list-units --type=service | grep snell-server@
}

case "$1" in
  install) install_binary ;;
  create) create_config "$2"
          start_instance "$2" ;;
  stop) stop_instance "$2" ;;
  list) list_instances ;;
  *) echo "用法: $0 {install|create <port>|stop <port>|list}" ;;
esac
```