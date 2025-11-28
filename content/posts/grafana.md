+++
title = "使用komari的延迟数据 + grafana自定义延迟看板"
date = 2025-11-25
weight = 20251125
description = "使用高度自由定制的grafana看板搭建属于自己的延迟看板"

[taxonomies]
tags = ["vps","工具"]

[extra]
+++

## 1. 安装grafana
1.1 安装依赖
```
sudo apt-get update
sudo apt-get install -y apt-transport-https software-properties-common wget gnupg
```
1.2 添加 Grafana 官方 GPG key
```
wget -q -O - https://packages.grafana.com/gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/grafana.gpg
```
1.3 添加 Grafana APT 源
```
echo "deb [signed-by=/usr/share/keyrings/grafana.gpg] https://packages.grafana.com/oss/deb stable main" \
  | sudo tee /etc/apt/sources.list.d/grafana.list
```
1.4 安装 Grafana
```
sudo apt-get update
sudo apt-get install -y grafana
```
1.5 启动 Grafana
```
sudo systemctl daemon-reload
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```
1.6 确认 Grafana 状态
```
systemctl status grafana-server
```

## 2. 处理数据
2.1 安装sqlite3
```
sudo apt install sqlite3
```
2.2 进入komari数据库
```
sqlite3 /opt/komari/data/komari.db
```
2.3 创建视图
```
CREATE VIEW v_ping_stats AS
SELECT
    pr.time AS time,
    pr.value AS value,
    c.uuid AS client_uuid,
    c.name AS client_name,
    t.id AS task_id,
    t.name AS task_name,
    t.target AS target
FROM ping_records pr
JOIN clients c ON pr.client = c.uuid
JOIN ping_tasks t ON pr.task_id = t.id;
```
## 3. 创建图表
3.1 安装Grafana插件
```
grafana-cli plugins install frser-sqlite-datasource
systemctl restart grafana-server
```
3.2 登录Grafana后台
http://服务器IP:3000 账号密码默认都是admin
3.3 创建dashboard，选择sqlite数据库，填上地址/opt/komari/data/komari.db
3.4 显示延迟的sql
- 查看某台vps的延迟
```
SELECT
  (strftime('%s', time)) AS time,  -- 转换为毫秒,
  value,
  task_name
FROM v_ping_stats
WHERE client_name = 'xx' -- komari后台设置的vps名称
ORDER BY time;
```
- 查看某台vps的丢包率
丢包率的算法不唯一，下面是按照5分钟聚合，结果还受到你上报的频率影响
```
SELECT
  (strftime('%s', time) / 300) * 300 AS time,  -- 按5分钟对齐
  task_name,
  SUM(CASE WHEN value = -1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS loss_rate -- komari中延迟-1代表丢包
FROM v_ping_stats
WHERE client_name = 'xx' -- komari后台设置的vps名称
GROUP BY 
  strftime('%s', time) / 300,
  task_name
ORDER BY time;
```
## 4. 开放给游客访问
4.1 修改/etc/grafana/grafana.ini文件
```
[auth.anonymous]
# 启用匿名访问
enabled = true

# 指定匿名用户的组织(通常是 1)
org_name = Main Org.

# 指定匿名用户的角色 (Viewer, Editor, Admin)
org_role = Viewer

# 可选: 隐藏版本信息
hide_version = false
```
4.2 重启 Grafana
```
sudo systemctl restart grafana-server
```
Grafana配置相对灵活，大家可以高度自定义
最后放一下草稿

https://grafana.qixin.ch
