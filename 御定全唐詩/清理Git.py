#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Git提示清除工具"""

import subprocess
import sys
from pathlib import Path


def clear_git_changes():
    """清除所有Git变更"""
    print("🧹 清除Git提示中...")
    
    # 1. 添加所有变更
    subprocess.run(['git', 'add', '.'], capture_output=True)
    
    # 2. 创建提交
    result = subprocess.run([
        'git', 'commit', '-m', '清理Git状态 - 消除VS Code提示'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Git状态已清理")
        return True
    else:
        if "nothing to commit" in result.stderr:
            print("✅ Git状态已干净")
            return True
        else:
            print(f"⚠️  {result.stderr}")
            return False


def main():
    """主函数"""
    print("=" * 50)
    print("Git提示清除工具")
    print("=" * 50)
    
    if not Path('.git').exists():
        print("❌ 不是Git仓库")
        return 1
    
    clear_git_changes()
    
    # 验证结果
    result = subprocess.run(['git', 'status', '--porcelain'], 
                          capture_output=True, text=True)
    
    if not result.stdout.strip():
        print("🎉 完成！所有Git提示已清除")
    else:
        print("⚠️  仍有未处理内容:")
        print(result.stdout)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())