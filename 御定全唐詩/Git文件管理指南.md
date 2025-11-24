# 《御定全唐詩》Git文件管理解决方案

## 问题背景

项目中包含大量文件，特别是JSON数据文件（json/*.json）和生成的数据文件（website_data/*.json），这些文件可能包含以下问题：

1. **文件过大** - JSON数据文件可能很大，推送会影响仓库大小
2. **生成内容** - AI处理后的数据文件可以重新生成，无需推送到Git
3. **环境配置** - .env等敏感配置文件不应该推送到公共仓库
4. **日志文件** - 处理日志等临时文件

## 解决方案

### 1. 自动文件管理工具

#### 快速使用（推荐）
```bash
# Windows
git_manager.bat all

# Linux/Mac
python git_file_manager.py --scan --generate-lists --create-gitignore --backup-large
```

#### 分步操作
```bash
# 1. 扫描项目文件
python git_file_manager.py --scan

# 2. 生成推送文件列表
python git_file_manager.py --generate-lists

# 3. 创建.gitignore
python git_file_manager.py --create-gitignore

# 4. 备份大文件（可选）
python git_file_manager.py --backup-large
```

### 2. Git选择性推送

#### 方法一：使用生成的列表文件
```bash
# 只推送核心文件
git add --from-file=push_list.txt
git commit -m "添加《御定全唐詩》核心文件"

# 查看暂存区状态
git status
```

#### 方法二：使用.gitignore
```bash
# 创建.gitignore后
git add .
git commit -m "添加项目文件（忽略生成文件）"
```

### 3. 文件分类说明

#### 应该推送的核心文件：
- ✅ **源代码**: *.py（处理脚本）
- ✅ **文档**: *.md（说明文档）
- ✅ **网站文件**: *.html, *.js, *.css（前端文件）
- ✅ **配置文件**: *.txt, requirements.txt（项目配置）
- ✅ **原始数据**: json/001.json - json/020.json（核心数据样本）

#### 暂时不推送的文件：
- ❌ **大文件**: json/021.json之后（数据完整版，文件较大）
- ❌ **生成数据**: website_data/*.json（可重新生成）
- ❌ **环境配置**: .env（包含API密钥）
- ❌ **日志文件**: *.log（处理过程记录）
- ❌ **缓存文件**: __pycache__/, *.pyc

### 4. 备份策略

#### 本地备份
```bash
# 运行备份命令
python git_file_manager.py --backup-large

# 备份文件将存储在 backup/ 目录中
```

#### 云端备份（可选）
```bash
# 压缩备份
zip -r tang_poetry_backup.zip backup/

# 上传到云端（根据您的云端方案）
```

## 使用流程

### 步骤1：初始设置
```bash
# 进入项目目录
cd 御定全唐詩

# 运行一键管理
git_manager.bat all
```

### 步骤2：查看结果
- 检查 `push_list.txt` - 确认需要推送的文件
- 检查 `exclude_list.txt` - 确认被排除的文件
- 检查 `.gitignore` - 确认忽略规则
- 检查 `backup/` 目录 - 确认大文件备份

### 步骤3：Git操作
```bash
# 添加.gitignore
git add .gitignore
git commit -m "添加.gitignore文件"

# 添加核心文件
git add --from-file=push_list.txt
git commit -m "添加《御定全唐詩》核心文件"

# 检查状态
git status
```

## 高级功能

### 1. 自定义排除规则
编辑 `git_file_manager.py` 中的 `exclude_patterns`：

```python
self.exclude_patterns = {
    # 添加您的自定义规则
    'custom_files': [
        'your_pattern/*',
        '*.custom'
    ]
}
```

### 2. 清理生成文件
```bash
# 预览清理操作
python git_file_manager.py --clean-generated --dry-run

# 执行清理
python git_file_manager.py --clean-generated
```

### 3. 恢复备份文件
```bash
# 手动从backup目录恢复
copy backup\website_data\*.json website_data\
```

## 常见问题

### Q: 为什么要排除JSON文件？
A: JSON数据文件，特别是完整的900卷数据文件，可能非常大。每个文件可能达到几MB，推送到Git会增加仓库大小，影响下载速度。

### Q: 如何处理缺失的数据文件？
A: 
1. 从备份目录恢复
2. 重新运行处理脚本生成
3. 提供单独的数据包下载

### Q: 如何选择性推送某些JSON文件？
A: 编辑 `push_list.txt` 文件，将需要的JSON文件路径添加到相应部分。

### Q: 如何更新生成的数据？
A: 在新环境中运行处理脚本：
```bash
python folder_batch_poem_processor.py
```

## 最佳实践

1. **分层推送**：
   - 第一层：核心代码和文档
   - 第二层：核心数据（json/001.json - json/020.json）
   - 第三层：完整数据（通过其他方式分发）

2. **版本管理**：
   - 使用语义化版本号
   - 为不同类型的文件设置不同的推送频率

3. **备份策略**：
   - 本地备份大文件
   - 云端备份重要数据
   - 定期清理临时文件

4. **团队协作**：
   - 在README中说明文件组织方式
   - 使用分支管理不同版本
   - 建立代码审查流程

---

通过这个解决方案，您可以有效地管理《御定全唐詩》项目中的文件推送，既保证核心功能的可用性，又避免大文件和生成文件对Git仓库的影响。