@echo off
chcp 65001 >nul
echo ========================================================
echo 《御定全唐詩》一键Git管理解决方案
echo 绕过VS Code提示，自动完成所有操作
echo ========================================================
echo.

cd /d "%~dp0"

echo 步骤 1/4: 生成文件列表...
python git_file_manager.py --generate-lists --quiet

echo 步骤 2/4: 创建 .gitignore...
python git_file_manager.py --create-gitignore --quiet

echo 步骤 3/4: 备份大文件...
python git_file_manager.py --backup-large --quiet

echo 步骤 4/4: 自动Git操作...
python auto_git.py "添加《御定全唐詩》Git文件管理解决方案"

echo.
echo ========================================================
echo ✅ 一键操作完成！
echo ========================================================
echo.
echo 操作结果：
echo • 文件列表已生成：push_list.txt, exclude_list.txt
echo • .gitignore文件已创建
echo • 大文件已备份到 backup/ 目录
echo • Git提交已完成
echo.
echo 接下来您可以：
echo • 直接推送：git push （如配置了远程仓库）
echo • 或者：git add --from-file=push_list.txt （手动模式）
echo ========================================================

pause