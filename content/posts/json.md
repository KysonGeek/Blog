+++
title = "一个支持格式化残缺json的工具"
date = 2025-12-02
weight = 20251202

description = "平常工作中，经常使用json格式化，例如格式化日志，但打印日志时为了减少损耗，会对打印json进行截断，截断后网上的json格式工具就失效了提示json异常，但平常使用vscode时就可以对残缺的json以及log中间包含的json进行格式化。"

[taxonomies]
tags = ["研发", "工具"]

[extra]
+++

用ai结合vscode原生的格式化能力搭建了一个json格式化工具
[json tool](https://json.qixin.ch)
[github](https://github.com/KysonGeek/json_format)

示例：
input1

```
{"xxa":{"ak":"a","sk":"a"},"xxb":{"ak":"a","sk":"a"},"xxc":{"ak":"a","sk":"a"},"xxd":{"ak":"a","sk":"a"
```
output1
```json
{
    "xxa": {
        "ak": "a",
        "sk": "a"
    },
    "xxb": {
        "ak": "a",
        "sk": "a"
    },
    "xxc": {
        "ak": "a",
        "sk": "a"
    },
    "xxd": {
        "ak": "a",
        "sk": "a"
```

input2
```
Info 2025-12-02 14:05:30.949 sxx logid  request body ={"bizId":"xx","curMessage":{"messageId":null,"content":"xx","type":"TEXT","role":"USER","shortCutToolId":null,"userCurTime":null,"toolCalls":null},"type":"CHAT","userId":"xx","chatHistory":[{"messageId":"xx","content":"xx","type
```
output2
```json
Info 2025-12-02 14: 05: 30.949 sxx logid  request body ={
    "bizId": "xx",
    "curMessage": {
        "messageId": null,
        "content": "xx",
        "type": "TEXT",
        "role": "USER",
        "shortCutToolId": null,
        "userCurTime": null,
        "toolCalls": null
    },
    "type": "CHAT",
    "userId": "xx",
    "chatHistory": [
        {
            "messageId": "xx",
            "content": "xx","type
```
