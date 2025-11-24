# AI诗歌标签处理工具使用指南

## 工具概述

本系统提供两种数据处理方式：

1. **单文件批量处理** - 处理合并后的单个JSON文件
2. **文件夹批量处理** - 按原始文件夹结构处理多个JSON文件

## 数据源说明

### 原始数据结构
- 诗歌数据分布在 `json/` 文件夹中的多个JSON文件
- 每个文件包含多首诗歌，按卷号组织
- 文件命名：`001.json`, `002.json`, ..., `456.json`

### 合并数据结构
- `website_data/poems_data.json` - 所有诗歌合并后的文件
- 包含所有诗歌的完整数据

## 工具选择指南

### 1. 单文件批量处理器 (`batch_ai_poem_processor.py`)

**适用场景：**
- 处理已合并的完整数据集
- 需要快速处理所有诗歌
- 不需要按原始文件结构保存结果

**使用方法：**
```bash
# 处理所有诗歌
python batch_ai_poem_processor.py

# 处理指定范围的诗歌
python batch_ai_poem_processor.py --start 0 --end 100

# 测试模式（只处理前10首）
python batch_ai_poem_processor.py --sample 10

# 自定义参数
python batch_ai_poem_processor.py --batch-size 10 --delay 2.0
```

**输出结果：**
- `website_data/ai_enhanced_poems.json` - 完整的增强数据
- `website_data/ai_analysis_statistics.json` - 统计信息

### 2. 文件夹批量处理器 (`folder_batch_poem_processor.py`)

**适用场景：**
- 按原始文件结构处理数据
- 需要保持文件级别的组织
- 分批次处理大量数据
- 需要文件级别的统计信息

**使用方法：**
```bash
# 处理所有JSON文件
python folder_batch_poem_processor.py

# 处理指定文件范围
python folder_batch_poem_processor.py --start-file 1 --end-file 10

# 自定义输出文件夹
python folder_batch_poem_processor.py --output-folder my_output

# 测试模式（只处理前3个文件）
python folder_batch_poem_processor.py --sample-files 3
```

**输出结果：**
- `website_data/ai_enhanced_001.json` - 每个文件的增强版本
- `website_data/ai_enhanced_poems_merged.json` - 合并的完整数据
- `website_data/folder_ai_analysis_statistics.json` - 详细统计信息

## 参数说明

### 通用参数
- `--api-key` - DeepSeek API密钥（可选，优先使用环境变量）
- `--batch-size` - 批次大小（默认20）
- `--delay` - 请求间隔秒数（默认1.0）

### 单文件处理器特有参数
- `--input` - 输入文件路径（默认：website_data/poems_data.json）
- `--output` - 输出文件路径
- `--start` - 开始索引
- `--end` - 结束索引
- `--sample` - 样本大小（测试用）

### 文件夹处理器特有参数
- `--folder` - 输入文件夹路径（默认：json）
- `--output-folder` - 输出文件夹路径
- `--start-file` - 开始文件编号
- `--end-file` - 结束文件编号
- `--sample-files` - 样本文件数量（测试用）

## 环境配置

### 1. 设置API密钥
```bash
# 方法1：创建.env文件
echo "DEEPSEEK_API_KEY=your_api_key_here" > .env

# 方法2：设置系统环境变量
set DEEPSEEK_API_KEY=your_api_key_here

# 方法3：命令行参数
python batch_ai_poem_processor.py --api-key your_api_key_here
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

## 处理策略建议

### 小规模测试
```bash
# 单文件测试
python batch_ai_poem_processor.py --sample 5

# 文件夹测试
python folder_batch_poem_processor.py --sample-files 2
```

### 大规模处理
```bash
# 分批处理单文件
python batch_ai_poem_processor.py --start 0 --end 1000
python batch_ai_poem_processor.py --start 1000 --end 2000

# 分批处理文件夹
python folder_batch_poem_processor.py --start-file 1 --end-file 50
python folder_batch_poem_processor.py --start-file 51 --end-file 100
```

### 优化性能
```bash
# 增加批次大小，减少API调用次数
python batch_ai_poem_processor.py --batch-size 50

# 增加延迟，避免API限制
python batch_ai_poem_processor.py --delay 2.0
```

## 输出数据结构

处理后的诗歌数据包含原始字段和新增的AI分析字段：

```json
{
  "id": "卷一-1",
  "title": "帝京篇十首",
  "author": "李世民",
  "volume": "卷一",
  "number": 1,
  "paragraphs": [...],
  "keywords": [...],
  "dynasty": "初唐",
  "ai_tags": {
    "styles": ["豪放", "宫廷"],
    "scenes": ["宫廷", "宴会"],
    "emotions": ["豪迈", "欢愉"],
    "themes": ["帝王生活", "国家治理"],
    "rhetoric": ["对仗", "比喻"]
  },
  "ai_analysis": {
    "summary": "诗歌内容摘要...",
    "key_phrases": ["关键词1", "关键词2"]
  },
  "source_file": "001.json"  // 仅文件夹处理器有此字段
}
```

## 故障排除

### 常见问题

1. **API密钥错误**
   - 检查.env文件格式
   - 确认API密钥有效性

2. **网络连接问题**
   - 增加请求延迟
   - 检查网络连接

3. **内存不足**
   - 减小批次大小
   - 分批处理数据

4. **文件不存在**
   - 检查文件路径
   - 确认数据文件存在

### 日志查看
```bash
# 查看处理日志
tail -f ai_poem_processing.log
tail -f folder_ai_poem_processing.log
```

## 最佳实践

1. **先测试后生产**：先用小样本测试，确认无误后再处理完整数据
2. **分批处理**：对于大量数据，建议分批处理避免超时
3. **备份数据**：处理前备份原始数据
4. **监控进度**：通过日志文件监控处理进度
5. **错误恢复**：如果中途失败，可以从断点继续处理

选择适合您需求的工具，开始为您的诗歌数据添加智能标签吧！