#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动Git操作脚本 - 绕过VS Code提示，自动完成Git操作
"""

import os
import subprocess
import sys
from pathlib import Path


def run_git_command(command, check=True):
    """
    运行Git命令
    
    Args:
        command: Git命令
        check: 是否检查错误
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode


def setup_git_repository():
    """初始化Git仓库（如果需要）"""
    stdout, stderr, code = run_git_command("git status", check=False)
    
    if "not a git repository" in stderr.lower():
        print("正在初始化Git仓库...")
        run_git_command("git init")
        run_git_command('git config user.name "御定全唐詩项目"')
        run_git_command('git config user.email "project@tangpoetry.com"')


def auto_add_files():
    """自动添加文件到暂存区"""
    print("🔍 正在检查文件变更...")
    
    # 检查Git状态
    stdout, stderr, code = run_git_command("git status --porcelain", check=False)
    
    if not stdout.strip():
        print("✅ 没有文件变更")
        return False
    
    # 添加所有变更
    print("📁 正在添加文件到暂存区...")
    
    # 添加配置文件
    run_git_command("git add .gitignore", check=False)
    run_git_command("git add push_list.txt", check=False)
    run_git_command("git add exclude_list.txt", check=False)
    
    # 添加Python脚本
    run_git_command("git add *.py", check=False)
    
    # 添加文档
    run_git_command("git add *.md", check=False)
    
    # 添加批处理文件
    run_git_command("git add *.bat", check=False)
    
    # 显示状态
    status_out, _, _ = run_git_command("git status --short")
    print("📊 暂存区状态:")
    print(status_out)
    
    return True


def auto_commit_changes(commit_message=None):
    """自动提交变更"""
    if not commit_message:
        commit_message = "添加《御定全唐詩》Git文件管理解决方案"
    
    print(f"💾 正在提交变更: {commit_message}")
    
    # 检查是否有暂存的变更
    stdout, stderr, code = run_git_command("git diff --cached --quiet", check=False)
    
    if code != 0:
        run_git_command(f'git commit -m "{commit_message}"')
        print("✅ 提交完成")
        return True
    else:
        print("⚠️  没有暂存的变更")
        return False


def push_to_remote():
    """推送到远程仓库（如果配置了）"""
    stdout, stderr, code = run_git_command("git remote -v", check=False)
    
    if not stdout.strip():
        print("⚠️  没有配置远程仓库")
        return False
    
    print("🚀 正在推送到远程仓库...")
    run_git_command("git push -u origin main")
    print("✅ 推送完成")
    return True


def main():
    """主函数"""
    print("=" * 60)
    print("《御定全唐詩》自动Git操作")
    print("=" * 60)
    
    # 检查是否在Git目录中
    if not Path(".git").exists():
        setup_git_repository()
    
    # 解析命令行参数
    commit_message = None
    auto_push = False
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--push":
            auto_push = True
        else:
            commit_message = " ".join(sys.argv[1:])
    
    # 执行Git操作
    if auto_add_files():
        if auto_commit_changes(commit_message):
            if auto_push:
                push_to_remote()
        else:
            print("❌ 提交失败")
            return 1
    else:
        print("ℹ️  操作完成，无需提交")
    
    print("=" * 60)
    print("✅ 自动Git操作完成")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())