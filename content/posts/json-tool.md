+++
title = "查看一行json的大文件方法"
date = 2025-10-20
weight = 20251020

[taxonomies]
tags = ["研发","工具"]

[extra]
+++

使用vscode打开大文件时有一定概率卡死，可以采用jq格式化，将一行json解析成多行，然后使用less分页浏览
>jq 的主要特点
流式处理：可以处理任意大小的 JSON 数据
丰富的操作符：提供多种操作符来处理 JSON 数据结构
格式化输出：可以美化 JSON 输出，提高可读性
跨平台：可在 Linux、macOS 和 Windows（通过 WSL）上运行
```
jq . result.json | less
```
也可以只看指定的字段
    jq '.data' result.json | less
