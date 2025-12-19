#!/bin/bash

# 
# 脚本名称: update_blog.sh
# 描述: 快速进入 /root/myblog 目录，执行 git pull 并运行 zola build。
# 

BLOG_DIR="/root/myblog"

echo "=== 开始更新博客 ==="

# 1. 切换到博客目录
echo "切换到目录: $BLOG_DIR"
if [ -d "$BLOG_DIR" ]; then
    cd "$BLOG_DIR"
else
    echo "错误: 目录 $BLOG_DIR 不存在。请检查路径。"
    exit 1
fi

# 2. 执行 git pull
echo "执行 git pull..."
git pull

# 检查 git pull 是否成功
if [ $? -ne 0 ]; then
    echo "错误: git pull 执行失败。请检查网络连接或权限。"
    exit 1
fi

# 3. 执行 zola build
echo "执行 zola build..."
zola build

# 检查 zola build 是否成功
if [ $? -ne 0 ]; then
    echo "错误: zola build 执行失败。请检查 Zola 是否安装或配置是否正确。"
    exit 1
fi

echo "=== 博客更新和构建完成 ==="

# 返回到脚本执行前的目录 (可选)
# cd - > /dev/null
