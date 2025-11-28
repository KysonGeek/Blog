+++
title = "快速查看csv大文件"
date = 2025-10-28
weight = 20251028

[taxonomies]
tags = ["研发", "工具"]

[extra]
+++

安装：
```
brew install xsv    # macOS
sudo apt install xsv  # Debian/Ubuntu
```
使用：
```
xsv table -d, big.csv | less -S        # 美观对齐查看（流式输出）
xsv headers big.csv                    # 只看列名
xsv slice -i 0 -l 20 big.csv           # 取前 20 行
xsv select name,age big.csv | head     # 选列+快速预览
xsv stats big.csv                      # 各列统计（数值/非数值/缺失等）
```
过滤：
```
xsv search Kyson big.csv
```
→ 查找任意列中包含 “Kyson” 的行。
只在特定列中匹配：
```
xsv search -s name Kyson big.csv
xsv search -i -s city tokyo big.csv # 大小写不敏感
```
正则匹配：
```
xsv search -s email '.*@gmail\.com' big.csv
```
管道：
```
xsv search -s process_node_descp '问题识别' 1761016417085.csv | xsv table | less -S
```
