# Kyson's Blog

基于 Zola 构建的个人博客，使用归档在仓库内的 `archie-zola` 主题。支持中文导航、代码高亮和 KaTeX 数学公式。

## 在线地址

- 站点：`https://blog.qixin.ch/`
- 标题：`Kyson's blog`

## 技术栈

- `Zola`：Rust 编写的静态站点生成器
- 主题：`themes/archie-zola`
- 内容目录：`content/`（文章、页面）
- 静态资源：`static/`（图片、图标、JS、CSS）
- 模板：`templates/`（首页、列表页、宏）
- 站点配置：`config.toml`

## 本地运行

- 安装 Zola（macOS）：`brew install zola`
- 启动本地预览：`zola serve`
- 预览地址：`http://127.0.0.1:1111`

## 构建与发布

- 构建静态文件：`zola build`
- 构建输出目录：`public/`
- GitHub Pages 简易发布（手动）：
  - 执行 `zola build`
  - 将 `public/` 内容推送到 `gh-pages` 分支并启用 Pages

## 目录结构

- `content/`：
  - `posts/` 文章列表，例如 `content/posts/as.md`
  - `about.md` 等页面
- `static/`：公共静态资源（如 `static/icon/favicon.png`、`static/imgs/...`）
- `templates/`：页面模板与宏（如 `templates/index.html`、`templates/posts.html`）
- `themes/archie-zola/`：主题源码（可直接二次定制）
- `config.toml`：站点与主题配置

## 写作指南

- 新建文章：在 `content/posts/` 下创建 `YYYY-mm-dd-标题.md`（文件名自定）
- 使用 TOML Front Matter：以 `+++` 包裹头部元数据，例如：

```
+++
title = "示例文章标题"
date = 2025-12-05
weight = 20251205
description = "文章简介"

[taxonomies]
tags = ["示例", "标签"]

[extra]
+++

正文从这里开始...
```

- 标签：通过 `[taxonomies]` 的 `tags` 字段管理
- 数学公式：在 `config.toml` 中已开启 `katex_enable = true`
- 代码高亮：`[markdown] highlight_code = true`

## 配置要点（`config.toml`）

- `base_url`：站点基础 URL（当前为 `//blog.qixin.ch/`）
- `default_language`：默认语言（当前 `zh-CN`）
- `taxonomies`：标签等分类配置
- `theme`：主题名称（`archie-zola`）
- `[extra]`：主题扩展配置，如：
  - `subtitle`、`mode`（深色/自动/切换）、`katex_enable`
  - `menus` 导航菜单
  - `social` 页脚社交链接（如 GitHub）

## 主题定制

- 样式：`themes/archie-zola/static/css/`（如 `main.css`、`dark.css`）
- 模板：`themes/archie-zola/templates/`（页头、页脚、文章等）
- 资源：`themes/archie-zola/static/`（图标、脚本、字体等）

## 许可与致谢

- 主题遵循其自带的 `LICENSE`
- 构建工具：Zola（感谢开源社区）

