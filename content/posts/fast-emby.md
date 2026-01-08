+++
title = "提升302emby起播速度"
date = 2026-01-06
weight = 20260106
description = "302emby服务由于使用了302跳转，需要多次与emby服务端交互，导致起播速度较慢，本文介绍如何提升302emby起播速度。"

[taxonomies]
tags = ["vps", "网络"]

[extra]
+++

> 我是用[qmediasync](https://github.com/qicfan/qmediasync/wiki)搭建的，这是以下文档的前提，如果你不是用这个工具搭建的，可能会有差异。

## 1. 问题描述

最近搭建了一个115+strm+302emby服务（115网盘+STRM播放列表文件+302重定向的Emby服务），发现起播速度较慢，经测试发现是因为302多次跳转（Emby服务器每次都需要向115服务器请求直链），以及emby服务端的响应时间导致的。
抓包效果，以及详情如下

<img src="/imgs/emby/1.jpeg" alt="Emby请求抓包图1" width="30%">
<img src="/imgs/emby/3.jpeg" alt="Emby请求抓包图2" width="30%">
<img src="/imgs/emby/2.jpeg" alt="Emby请求抓包图3" width="30%">
由于手机屏幕比较小只筛选了115的请求记录，具体流程如下

![Emby请求流程图](/imgs/emby/emby_puml.jpg)

加上其他的请求，起播速度约7秒

每次请求的作用不一样（Range请求是HTTP协议中用于断点续传或部分内容请求的机制）：
1. 第一次请求header中包含`Range: bytes=0-`，主要是获取视频的基本信息（码率、格式等），响应头中包含`Content-Length: 750112694`
2. 第二次请求header中包含`bytes=855081591-`，寻找文件尾部，检查文件完整性或读取位于末尾的索引信息
3. 第三次请求header中包含`bytes=855029833-`，回退一点点位置来读取特定的数据块（如某些 MKV 格式的 Cluster 数据段或特定的 Metadata 元数据段）
4. 第四次请求header中包含`bytes=11768-`，此时播放器已经完全了解了视频结构，知道前面的 0 到 11767 字节只是些描述信息，真正的视频内容（Data Ocean）是从 11768 字节开始的

由于我的emby服务器在国外，所以响应时间比较长，导致起播速度较慢。从上面的分析可以看出，第一次请求时已经拿到了115的直链，后续的三次我们可以跳过emby服务器直接客户端请求115，这样可以显著提升起播速度

## 2. 解决方案：动态捕获与 302 重定向

可以保存第一次请求响应头中的115直链，后续的三次请求直接本地请求115，而不是通过emby服务器。

现在很多代理工具都支持请求/响应改写脚本，我主要在手机上观看，使用[Quantumult X](https://apps.apple.com/us/app/quantumult-x/id1443988620?l=zh-Hans-CN)（一款iOS平台的网络调试工具）来实现这个优化方案。

### 1. 拦截emby部分请求
```conf
# 1. 匹配响应：捕获第一轮请求返回的Location（115直链）
# 当客户端发起视频流请求时，该规则会拦截响应头并调用emby_save_link.js脚本
^https?:\/\/emby\.xx\.com(:443)?\/emby\/videos\/\d+\/stream url script-response-header emby_save_link.js

# 2. 匹配请求：拦截后续轮次的Range请求
# 当客户端发起带有Range头的请求时，该规则会拦截请求头并调用emby_redirect_logic.js脚本
^https?:\/\/emby\.xx\.com(:443)?\/emby\/videos\/\d+\/stream url script-request-header emby_redirect_logic.js
```

### 2. 保存115直链

```js
let url = $request.url;
let headers = $request.headers;
let respHeaders = $response.headers;
let status = $response.statusCode || $response.status;

// 获取请求时的 Range
let range = headers["Range"] || headers["range"] || "";
// 获取响应中的 Location (115 直链)
let location = respHeaders["Location"] || respHeaders["location"];

let videoIdMatch = url.match(/\/videos\/(\d+)\/stream/);
let videoKey = videoIdMatch ? videoIdMatch[1] : null;

// 日志记录调试信息
console.log(`ID: ${videoKey} range:${range} status:${status} location:${location}`);

// 只有在以下条件满足时才保存直链：
// 1. 成功提取到视频ID
// 2. Range请求是从0开始的（第一轮请求）
// 3. 响应状态码是307（临时重定向）
// 4. 响应中包含Location头信息（115直链）
if (videoKey && range === "bytes=0-" && (status == 307) && location) {
    // 将直链保存到本地存储中，键名为"emby_115_" + 视频ID
    $prefs.setValueForKey(location, "emby_115_" + videoKey);
    console.log(`[Emby优化] 成功捕获直链 ID: ${videoKey}, Location: ${location}`);
}

$done({});
```

### 3. 本地拦截emby请求转发到115

```js
let url = $request.url;
let headers = $request.headers;
let range = headers["Range"] || headers["range"] || "";

// 从URL中提取视频ID作为缓存键
let videoIdMatch = url.match(/\/videos\/(\d+)\/stream/);
let videoKey = videoIdMatch ? videoIdMatch[1] : null;

// 核心逻辑：
// 1. 如果是后续的Range请求（不是从0开始）
// 2. 且在本地存储中找到了对应的115直链
// 则直接将请求重定向到115直链，绕过emby服务器
if (videoKey && range && range !== "bytes=0-") {
    // 从本地存储中获取保存的115直链
    let savedLocation = $prefs.valueForKey("emby_115_" + videoKey);
    
    if (savedLocation) {
        console.log(`[Emby优化] 命中缓存，ID: ${videoKey}, Range: ${range}, 转发至直链`);
        // 返回302重定向响应，将客户端直接引导到115直链
        $done({
            status: "HTTP/1.1 302 Found",
            headers: {
                "Location": savedLocation,
                "Access-Control-Allow-Origin": "*",
                "Cache-Control": "no-cache"
            },
            body: ""
        });
    } else {
        console.log(`[Emby优化] 未命中缓存，放行由VPS处理`);
        $done({});
    }
} else {
    // 第一轮请求（Range: bytes=0-）或无Range请求，直接放行给emby服务器处理
    $done({});
}
```

## 3. 测试效果

### 优化目标流程
优化后的请求流程将跳过后续请求的Emby服务器环节，直接从客户端请求115直链：
![优化后Emby请求流程图](/imgs/emby/4.png)

### 实际测试结果

<img src="/imgs/emby/5.jpeg" alt="实际优化效果测试图" width="40%">

### 性能对比
- **优化前**：起播速度约7秒（受Emby服务器网络延迟影响）
- **优化后**：起播速度约3秒
- **提升幅度**：约57%的起播速度提升

测试条件：
- 客户端：iOS设备
- 网络环境：家庭Wi-Fi（50Mbps下载速度）
- Emby服务器：国外VPS（延迟约200ms）
- 测试视频：1080P MKV格式（约8GB）

## 备注
- 本方案主要解决公网302emby服务的起播速度问题，对于局域网内的Emby服务，由于网络延迟较低，优化效果可能不明显。
- 视频的基本信息（如码率、格式等）仍需通过第一次请求获取，这是Emby播放器正常工作的必要步骤。
- 该方案依赖于代理工具的脚本功能，不同工具的实现方式可能略有差异。
