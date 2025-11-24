# 文件夹批量处理使用指南

## 概述
文件夹批量处理器 (`folder_batch_poem_processor.py`) 专门用于处理包含多个JSON文件的文件夹，每个文件包含多首诗歌数据。

## 使用方法

### 1. 通过交互式菜单
```bash
python start_here_windows.py
```
然后选择 "3. 文件夹批量处理"

### 2. 直接命令行使用
```bash
# 基本用法 - 处理 json/ 文件夹中的所有文件
python folder_batch_poem_processor.py --folder json

# 指定输出文件夹
python folder_batch_poem_processor.py --folder json --output-folder processed_data

# 只处理部分文件（测试用）
python folder_batch_poem_processor.py --folder json --sample-files 5

# 自定义批次大小和延迟
python folder_batch_poem_processor.py --folder json --batch-size 10 --delay 2.0
```

### 3. 文件夹结构要求
```
项目根目录/
├── json/                    # 输入文件夹
│   ├── 001.json            # 诗歌数据文件1
│   ├── 002.json            # 诗歌数据文件2
│   ├── 003.json            # 诗歌数据文件3
│   └── ...                 # 更多文件
├── processed_data/          # 输出文件夹（自动创建）
│   ├── 001_enhanced.json   # 增强数据文件1
│   ├── 002_enhanced.json   # 增强数据文件2
│   └── ...                 # 更多增强文件
└── folder_ai_analysis_statistics.json  # 整体统计信息
```

## 参数说明

### 必需参数
- `--folder`: 输入文件夹路径（包含JSON文件的文件夹）

### 可选参数
- `--output-folder`: 输出文件夹路径（默认：`processed_data`）
- `--sample-files`: 样本文件数量（只处理前N个文件，用于测试）
- `--batch-size`: 批次大小（默认：20）
- `--delay`: 请求间隔秒数（默认：1.0）
- `--api-key`: DeepSeek API密钥（可选，优先使用环境变量）
- `--start-file`: 开始文件编号
- `--end-file`: 结束文件编号

## 示例

### 示例1：处理整个json文件夹
```bash
python folder_batch_poem_processor.py --folder json
```

### 示例2：处理指定文件夹并自定义参数
```bash
python folder_batch_poem_processor.py --folder D:\诗歌数据 --output-folder D:\处理结果 --batch-size 15 --delay 1.5
```

### 示例3：测试处理前5个文件
```bash
python folder_batch_poem_processor.py --folder json --sample-files 5
```

### 示例4：处理指定范围的文件
```bash
python folder_batch_poem_processor.py --folder json --start-file 10 --end-file 20
```

## 路径格式

### Windows路径格式
```bash
# 绝对路径
python folder_batch_poem_processor.py --folder "D:\Soft\MyCode\test-demo\御定全唐詩\json"

# 相对路径（推荐）
python folder_batch_poem_processor.py --folder json
python folder_batch_poem_processor.py --folder ./json
python folder_batch_poem_processor.py --folder ../其他文件夹
```

### Linux/Mac路径格式
```bash
python folder_batch_poem_processor.py --folder /home/user/诗歌数据/json
python folder_batch_poem_processor.py --folder ./json
```

## 处理流程

1. **扫描文件夹** - 自动查找所有 `.json` 文件
2. **逐个处理** - 按文件名顺序处理每个文件
3. **生成增强数据** - 为每首诗歌添加AI标签
4. **保存结果** - 每个输入文件生成对应的增强文件
5. **生成统计** - 创建整体处理统计报告

## 输出文件

- `processed_data/` - 包含所有增强后的JSON文件
- `folder_ai_analysis_statistics.json` - 整体统计信息
- `folder_ai_poem_processing.log` - 详细处理日志

## 注意事项

1. **文件命名**：输入文件应按顺序命名（如001.json, 002.json等）
2. **数据格式**：每个JSON文件应包含诗歌数据数组
3. **API限制**：建议设置合理的批次大小和延迟时间
4. **进度显示**：处理过程中会显示当前进度和剩余时间