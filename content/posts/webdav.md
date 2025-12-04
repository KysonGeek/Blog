+++
title = "将夸克网盘挂载到vps搭建图片墙"
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

## 将挂载数据同步到本地
由于webdav速度太慢，严重影响网页加载速度，因此可以将挂载数据同步到本地。
1. 安装rclone
```bash
# 示例：Debian/Ubuntu
sudo apt update
sudo apt install rclone

# 示例：CentOS/RHEL
sudo dnf install rclone
```
2. 使用 rclone sync 进行定时同步
2.1 基本的同步命令
```bash
rclone sync /var/www/quark/pictures /var/www/pictures --ignore-times --delete-during
```
2.2 设置定时任务
打开 crontab 配置
```bash
crontab -e
```
在文件末尾添加一行，例如设置为每 5 分钟 同步一次（将 /path/to/rclone 替换为实际的 rclone 路径，通常是 /usr/bin/rclone）：
```bash
*/5 * * * * /usr/bin/rclone sync /var/www/quark/pictures /var/www/pictures --ignore-times --delete-during --log-file=/var/log/rclone_sync.log
```
## 使用[files.gallery](https://files.gallery/)搭建图片墙
可以使用破解版本[Smooth-Files-Gallery](https://github.com/yanranxiaoxi/Smooth-Files-Gallery)
1. 将下载的index.php文件上传到vps的/var/www/Photos目录下
2. 配置caddy（也可以使用nginx）
```bash
cat <<EOF > /etc/caddy/photo.xx.xx.service #自行修改
photo.xx.xx { ##自行修改
    # 设置网站根目录
    root * /var/www/Photos

    # 开启 gzip 压缩，加快图片加载
    encode gzip

    # 处理 PHP 文件 (关键步骤)
    # 注意：unix 路径可能因系统不同而不同，下面是常见的 Ubuntu/Debian 路径
    # 如果找不到该文件，请查看下文的“检查 PHP”部分
    php_fastcgi unix//run/php/php8.2-fpm.sock

    # 静态文件服务（用于直接展示图片）
    file_server
    request_body {
        max_size 200MB
    }
}
EOF
重启caddy
```
systemctl restart caddy
```
3. 配置文件权限
```bash
chmod -R 777 /var/www/Photos
```
4. 配置Files.Gallery
4.1 先放问一下`http://photo.xx.xx`，在index.php所在的文件夹下会生成_files，里面有个config.php, 将里面的root目录改为`/var/www/pictures`

5. 设置上传文件的大小
5.1 caddy上面已经配置了200M
5.2 PHP 上传大小限制（必须设置，否则 Caddy 放开也没用）
- /etc/php/8.2/fpm/php.ini
- /etc/php/8.2/cli/php.ini
修改：
```
upload_max_filesize = 200M
post_max_size = 200M
max_file_uploads = 100
```
重启PHP-FPM：
```
systemctl restart php8.2-fpm
```
验证生效
```bash
php -i | grep upload_max_filesize
php -i | grep post_max_size
```

## 备注
解释一下上面各个文件的作用

| 路径 | 作用 |
|------|------|
| /var/www/Photos/index.php | Files.Gallery 的入口文件，用于展示图片墙。因 files.gallery 会在该目录下创建 `_files` 等文件，需赋予写权限。 |
| /var/www/Photos/_files/config.php | Files.Gallery 的配置文件，用于设置图片墙参数，如根目录、缓存时间等。 |
| /var/www/quark/pictures | 挂载的 WebDAV 目录，用于存储图片。 |
| /var/www/pictures | 从挂载点同步到本地的目录，Files.Gallery 从此处读取图片。因文件会被覆盖，index.php 需放在其他文件夹。 |
| /var/log/rclone_sync.log | rclone 同步日志文件，记录同步过程中的信息。 |
| /etc/caddy/photo.xx.xx.service | Caddy 配置文件，用于配置图片墙域名、根目录、上传文件大小等。 |

## 引用
- [Linux使用davfs2挂载webdav作为本地磁盘并实现自动挂载](https://www.yunieebk.com/davfs2/)

