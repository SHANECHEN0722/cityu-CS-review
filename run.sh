#!/bin/bash
# 一键更新并部署课程资料
# 使用方法: ./run.sh
#你要先记得git add remote repo 还要给权限chmod +x run.sh

echo "🔄 步骤 1/3: 扫描课程文件夹..."
python3 tool/generate_courses_data.py

echo ""
echo "📝 步骤 2/3: 提交到 Git..."
git add -A
git commit -m "Update: Refresh course materials $(date '+%Y-%m-%d %H:%M')"

echo ""
echo "🚀 步骤 3/3: 推送到 GitHub..."
git push origin main

echo ""
echo "✅ 完成！等待 1-2 分钟后刷新 GitHub Pages 查看更新。"
