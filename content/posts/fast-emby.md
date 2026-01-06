+++
title = "提升302emby起播速度"
date = 2026-01-06
weight = 20260106
description = "302emby服务由于使用了302跳转，需要多次与emby服务端交互，导致起播速度较慢，本文介绍如何提升302emby起播速度。"

[taxonomies]
tags = ["vps", "网络"]

[extra]
+++

> 我是用[qmediasync](https://github.com/qicfan/qmediasync/wiki)搭建的，这是一下文档的前提，如果你不是用这个工具搭建的，可能会有差异。

## 1. 问题描述

最近搭建了一个115+strm+302emby服务，发现起播速度较慢，经测试发现是因为302多次跳转，以及emby服务端的响应时间导致的。
抓包效果，以及详情如下

<img src="/imgs/emby/1.jpeg" width="30%">
<img src="/imgs/emby/3.jpeg" width="30%">
<img src="/imgs/emby/2.jpeg" width="30%">
由于手机屏幕比较小只筛选了115的请求记录，具体流程如下

![](/imgs/emby/emby_puml.png)

加上其他的请求，起播速度约7秒

每次请求的左右不一样：
1. 第一次请求header中包含`Range: bytes=0-`，主要是获取视频的基本信息（码率、格式等），响应头中包含`Content-Length: 750112694`
2. 第二次请求header中包含`bytes=855081591-`，寻找文件尾部,检查文件完整性或读取位于末尾的索引
3. 第三次请求header中包含`bytes=855029833-`，回退一点点位置来读取特定的数据块（如某些 MKV 的 Cluster 或特定的 Metadata 段）
4. 第四次请求header中包含`bytes=11768-`，此时播放器已经完全了解了视频结构，知道前面的 0 到 11767 字节只是些描述信息，真正的视频内容（Data Ocean）是从 11768 开始的

由于我的emby服务器在国外，所以响应时间比较长，导致起播速度较慢。从上面的分析可以看出，第一次请求时已经拿到了115的直链，后续的三次我们可以跳过emby服务器直接客户端请求115，这样可以显著提升起播速度

## 2. 解决方案：动态捕获与 302 重定向

可以保存第一次请求响应头中的115直链，后续的三次请求直接本地请求115，而不是通过emby服务器。
现在很多代理工具都支持改写脚本，我主要在手机上看，使用圈x实现

### 1. 拦截emby部分请求
```conf
# 1. 匹配响应：捕获第一轮产生的 Location
^https?:\/\/emby\.xx\.com(:443)?\/emby\/videos\/\d+\/stream url script-response-header emby_save_link.js

# 2. 匹配请求：拦截后续轮次的 Range 请求
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

// 只有在 Range 是 0- 且 VPS 成功返回 307 时才记录
console.log(`ID: ${videoKey} range:${range} status:${status} location:${location}`);
if (videoKey && range === "bytes=0-" && (status == 307) && location) {
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

// 提取视频 ID (例如 4464) 作为缓存键
let videoIdMatch = url.match(/\/videos\/(\d+)\/stream/);
let videoKey = videoIdMatch ? videoIdMatch[1] : null;

// 逻辑：如果 Range 不是 0- 且缓存中有直链，则直接 302
if (videoKey && range && range !== "bytes=0-") {
    let savedLocation = $prefs.valueForKey("emby_115_" + videoKey);
    
    if (savedLocation) {
        console.log(`[Emby优化] 命中缓存，ID: ${videoKey}, Range: ${range}, 转发至直链`);
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
    // 第一轮 0- 或者无 Range 请求，直接放行给 VPS
    $done({});
}
```

## 3. 测试效果

目标流程：
![](/imgs/emby/4.png)

实际情况：

<img src="/imgs/emby/5.jpeg" width="40%">

起播速度约3秒

## 备注：
- 如果该文档只解决了公网302emby问题，如果是局域网不具备参考。
- 视频的基本信息还是需要提前获取，否则也会导致起播速度较慢。（未实验）
