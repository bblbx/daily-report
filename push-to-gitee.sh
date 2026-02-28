#!/bin/bash
# 推送到 Gitee 脚本

echo "🚀 推送到 Gitee..."
echo ""
echo "请在下方输入你的 Gitee 账号和密码（密码不会显示）"
echo ""

git remote set-url origin https://gitee.com/bblbx/daily-report.git
git push -u origin main

echo ""
echo "✅ 推送完成！"
echo ""
echo "接下来去 Gitee 操作："
echo "1. 进入仓库 → 管理 → Pages"
echo "2. 源分支选择 main，点击「启动 Pages」"
echo "3. 等待 1-2 分钟后访问：https://bblbx.gitee.io/daily-report/"
