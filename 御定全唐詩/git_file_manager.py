#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git文件管理器 - 管理《御定全唐詩》项目中的推送文件
用于识别和管理"暂时不推送"的文件
"""

import os
import json
import argparse
import shutil
from typing import List, Dict, Set
from pathlib import Path


class GitFileManager:
    """Git文件管理器"""
    
    def __init__(self, project_dir: str = "."):
        """
        初始化文件管理器
        
        Args:
            project_dir: 项目根目录
        """
        self.project_dir = Path(project_dir)
        self.exclude_patterns = {
            # 大文件和生成文件
            'large_files': [
                'website_data/*.json',
                'json/*.json',
                '*.log',
                '*.tmp',
                '*.cache'
            ],
            
            # 环境配置文件
            'environment_files': [
                '.env',
                '.env.local',
                '*.config',
                'config.json'
            ],
            
            # 编译和缓存文件
            'build_files': [
                '__pycache__',
                '*.pyc',
                '*.pyo',
                '.pytest_cache',
                'node_modules',
                'dist',
                'build'
            ],
            
            # IDE和编辑器文件
            'ide_files': [
                '.vscode',
                '.idea',
                '*.swp',
                '*.swo',
                '*.bak'
            ],
            
            # 系统文件
            'system_files': [
                '.DS_Store',
                'Thumbs.db',
                'desktop.ini'
            ]
        }
        
        self.push_list_file = self.project_dir / 'push_list.txt'
        self.exclude_list_file = self.project_dir / 'exclude_list.txt'
    
    def scan_project_files(self) -> Dict[str, List[str]]:
        """
        扫描项目文件并分类
        
        Returns:
            按类型分类的文件字典
        """
        files_by_type = {
            'json_data': [],
            'python_scripts': [],
            'web_files': [],
            'documents': [],
            'config_files': [],
            'logs': [],
            'other': []
        }
        
        for file_path in self.project_dir.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                relative_path = str(file_path.relative_to(self.project_dir))
                suffix = file_path.suffix.lower()
                
                if suffix == '.json':
                    files_by_type['json_data'].append(relative_path)
                elif suffix == '.py':
                    files_by_type['python_scripts'].append(relative_path)
                elif suffix in ['.html', '.js', '.css']:
                    files_by_type['web_files'].append(relative_path)
                elif suffix == '.md':
                    files_by_type['documents'].append(relative_path)
                elif suffix in ['.txt', '.env', '.yml', '.yaml', '.cfg']:
                    files_by_type['config_files'].append(relative_path)
                elif suffix == '.log':
                    files_by_type['logs'].append(relative_path)
                else:
                    files_by_type['other'].append(relative_path)
        
        return files_by_type
    
    def get_file_size(self, file_path: str) -> int:
        """
        获取文件大小（字节）
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件大小
        """
        try:
            return (self.project_dir / file_path).stat().st_size
        except:
            return 0
    
    def should_exclude_file(self, file_path: str) -> tuple[bool, str]:
        """
        判断文件是否应该排除
        
        Args:
            file_path: 文件相对路径
            
        Returns:
            (是否排除, 排除原因)
        """
        # 检查文件大小（超过1MB的文件）
        size = self.get_file_size(file_path)
        if size > 1024 * 1024:  # 1MB
            return True, f"大文件 ({size/1024/1024:.1f}MB)"
        
        # 检查文件名模式
        for category, patterns in self.exclude_patterns.items():
            for pattern in patterns:
                if self._match_pattern(file_path, pattern):
                    return True, f"匹配排除模式: {category}"
        
        # 检查特定文件
        exclude_files = {
            '.env': '环境配置文件',
            '*.log': '日志文件',
            'website_data/*.json': '生成的网站数据',
            'folder_ai_poem_processing.log': '处理日志',
            'ai_poem_processing.log': 'AI处理日志'
        }
        
        for pattern, reason in exclude_files.items():
            if self._match_pattern(file_path, pattern):
                return True, reason
        
        return False, ""
    
    def _match_pattern(self, file_path: str, pattern: str) -> bool:
        """
        简单的模式匹配
        
        Args:
            file_path: 文件路径
            pattern: 匹配模式
            
        Returns:
            是否匹配
        """
        # 处理通配符
        if '*' in pattern:
            parts = pattern.split('*')
            if len(parts) == 2:
                prefix, suffix = parts
                return file_path.startswith(prefix) and file_path.endswith(suffix)
            elif pattern.startswith('*'):
                return file_path.endswith(pattern[1:])
            elif pattern.endswith('*'):
                return file_path.startswith(pattern[:-1])
        
        return file_path == pattern
    
    def generate_file_lists(self, output_dir: str = None):
        """
        生成文件列表
        
        Args:
            output_dir: 输出目录
        """
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            push_list = output_path / 'push_list.txt'
            exclude_list = output_path / 'exclude_list.txt'
        else:
            push_list = self.push_list_file
            exclude_list = self.exclude_list_file
        
        # 扫描文件
        files_by_type = self.scan_project_files()
        
        push_files = []
        exclude_files = []
        
        # 分析每个文件
        all_files = []
        for file_type, files in files_by_type.items():
            all_files.extend(files)
        
        for file_path in all_files:
            should_exclude, reason = self.should_exclude_file(file_path)
            if should_exclude:
                exclude_files.append(f"{file_path} # {reason}")
            else:
                push_files.append(file_path)
        
        # 排序
        push_files.sort()
        exclude_files.sort()
        
        # 保存推送文件列表
        with open(push_list, 'w', encoding='utf-8') as f:
            f.write("# 应该推送的文件列表\n")
            f.write(f"# 生成时间: {Path().cwd()}\n\n")
            f.write("# Python脚本\n")
            for file in sorted(files_by_type['python_scripts']):
                if file not in exclude_files:
                    f.write(f"{file}\n")
            
            f.write("\n# 文档文件\n")
            for file in sorted(files_by_type['documents']):
                if file not in exclude_files:
                    f.write(f"{file}\n")
            
            f.write("\n# 网站文件\n")
            for file in sorted(files_by_type['web_files']):
                if file not in exclude_files:
                    f.write(f"{file}\n")
            
            f.write("\n# 配置文件\n")
            for file in sorted(files_by_type['config_files']):
                if file not in exclude_files:
                    f.write(f"{file}\n")
            
            f.write("\n# 其他重要文件\n")
            for file in sorted(files_by_type['other']):
                # 排除编译文件和缓存文件
                if (file not in exclude_files and
                    not self._is_generated_file(file) and
                    not file.endswith('.pyc') and
                    not 'pycache__' in file):
                    f.write(f"{file}\n")
            
            # 添加批处理文件
            if 'git_manager.bat' not in [f.split(' #')[0] for f in exclude_files]:
                f.write("git_manager.bat\n")
        
        # 保存排除文件列表
        with open(exclude_list, 'w', encoding='utf-8') as f:
            f.write("# 暂时不推送的文件列表\n")
            f.write(f"# 生成时间: {Path().cwd()}\n")
            f.write("# 原因包括：大文件、生成文件、环境配置等\n\n")
            
            for entry in exclude_files:
                f.write(f"{entry}\n")
        
        return push_files, exclude_files
    
    def _is_generated_file(self, file_path: str) -> bool:
        """
        判断是否为生成文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否为生成文件
        """
        generated_patterns = [
            'website_data/',
            'ai_enhanced_',
            'processed_',
            'combined_',
            '*.log'
        ]
        
        for pattern in generated_patterns:
            if self._match_pattern(file_path, pattern):
                return True
        return False
    
    def create_gitignore(self, output_file: str = None):
        """
        创建.gitignore文件
        
        Args:
            output_file: 输出文件路径
        """
        if not output_file:
            output_file = self.project_dir / '.gitignore'
        else:
            output_file = Path(output_file)
        
        gitignore_content = """# 《御定全唐詩》项目 .gitignore
# 自动生成文件

# 环境配置
.env
.env.local
.env.development
.env.production

# 日志文件
*.log
ai_poem_processing.log
folder_ai_poem_processing.log
*.tmp

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 处理后的数据文件
website_data/*.json
json/*.json
ai_enhanced_*.json
*.processed.json
*.combined.json

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.cache
desktop.ini

# 测试
.pytest_cache/
.coverage
htmlcov/

# 其他
*.cache
*.backup
node_modules/
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        return output_file
    
    def backup_large_files(self, backup_dir: str = "backup"):
        """
        备份大文件到本地目录
        
        Args:
            backup_dir: 备份目录
        """
        backup_path = self.project_dir / backup_dir
        backup_path.mkdir(exist_ok=True)
        
        files_by_type = self.scan_project_files()
        
        # 找出大文件
        large_files = []
        for file_type, files in files_by_type.items():
            for file_path in files:
                if self.get_file_size(file_path) > 1024 * 1024:  # 1MB
                    large_files.append(file_path)
        
        # 备份文件
        for file_path in large_files:
            src = self.project_dir / file_path
            dst = backup_path / file_path
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"备份: {file_path} -> {backup_dir}/{file_path}")
        
        print(f"\n备份完成! 备份目录: {backup_path}")
        return len(large_files)
    
    def clean_generated_files(self, dry_run: bool = True):
        """
        清理生成的文件
        
        Args:
            dry_run: 是否仅预览不实际删除
        """
        files_by_type = self.scan_project_files()
        
        # 生成的文件模式
        generated_patterns = [
            'website_data/*.json',
            '*.log',
            '*.tmp',
            '*.cache',
            'ai_enhanced_*.json'
        ]
        
        files_to_clean = []
        for file_path in files_by_type.get('json_data', []):
            for pattern in generated_patterns:
                if self._match_pattern(file_path, pattern):
                    files_to_clean.append(file_path)
                    break
        
        for file_path in files_by_type.get('logs', []):
            files_to_clean.append(file_path)
        
        if dry_run:
            print("预览将清理的文件:")
            for file_path in files_to_clean:
                print(f"  将删除: {file_path}")
            return len(files_to_clean)
        
        # 实际删除
        removed_count = 0
        for file_path in files_to_clean:
            try:
                (self.project_dir / file_path).unlink()
                print(f"已删除: {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"删除失败 {file_path}: {e}")
        
        return removed_count
    
    def print_summary(self):
        """打印项目文件摘要"""
        files_by_type = self.scan_project_files()
        
        print("\n" + "="*60)
        print("《御定全唐詩》项目文件摘要")
        print("="*60)
        
        total_files = 0
        total_size = 0
        
        for file_type, files in files_by_type.items():
            if files:
                type_size = sum(self.get_file_size(f) for f in files)
                total_size += type_size
                total_files += len(files)
                
                print(f"\n{file_type.upper()}: {len(files)} 个文件, {type_size/1024/1024:.1f} MB")
                for file_path in sorted(files)[:5]:  # 只显示前5个
                    size = self.get_file_size(file_path)
                    print(f"  {file_path} ({size/1024:.1f} KB)")
                if len(files) > 5:
                    print(f"  ... 还有 {len(files)-5} 个文件")
        
        print(f"\n总计: {total_files} 个文件, {total_size/1024/1024:.1f} MB")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Git文件管理器')
    parser.add_argument('--scan', action='store_true', help='扫描并分析项目文件')
    parser.add_argument('--generate-lists', action='store_true', help='生成推送和排除文件列表')
    parser.add_argument('--create-gitignore', action='store_true', help='创建.gitignore文件')
    parser.add_argument('--backup-large', action='store_true', help='备份大文件')
    parser.add_argument('--clean-generated', action='store_true', help='清理生成的文件')
    parser.add_argument('--dry-run', action='store_true', help='预览模式（不实际执行）')
    parser.add_argument('--output-dir', help='输出目录')
    parser.add_argument('--backup-dir', default='backup', help='备份目录')
    parser.add_argument('--quiet', action='store_true', help='静默模式，减少输出')
    
    args = parser.parse_args()
    
    # 创建管理器
    manager = GitFileManager()
    
    # 执行操作
    if args.scan:
        manager.print_summary()
    
    if args.generate_lists:
        push_files, exclude_files = manager.generate_file_lists(args.output_dir)
        if not args.quiet:
            print(f"\n文件列表生成完成:")
            print(f"  推送文件: {len(push_files)} 个")
            print(f"  排除文件: {len(exclude_files)} 个")
            print(f"  推送列表: push_list.txt")
            print(f"  排除列表: exclude_list.txt")
    
    if args.create_gitignore:
        gitignore_path = manager.create_gitignore()
        if not args.quiet:
            print(f".gitignore 文件已创建: {gitignore_path}")
    
    if args.backup_large:
        count = manager.backup_large_files(args.backup_dir)
        if not args.quiet:
            print(f"已备份 {count} 个大文件")
    
    if args.clean_generated:
        if args.dry_run:
            count = manager.clean_generated_files(dry_run=True)
            if not args.quiet:
                print(f"预览: 将清理 {count} 个文件")
        else:
            count = manager.clean_generated_files(dry_run=False)
            if not args.quiet:
                print(f"已清理 {count} 个文件")


if __name__ == "__main__":
    main()