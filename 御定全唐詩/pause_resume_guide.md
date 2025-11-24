# 暂停和续传功能使用指南

## 🎯 功能概述

现在系统支持**暂停和续传功能**，您可以在处理过程中随时暂停，并在之后继续处理，无需从头开始。

## 🔧 主要功能

### 1. 暂停处理
- **Ctrl+C**: 在终端中按 `Ctrl+C` 即可暂停当前处理
- **自动保存**: 系统会自动保存处理进度到 `processing_progress.json` 文件

### 2. 恢复处理
- **恢复命令**: `python folder_batch_poem_processor.py --resume`
- **智能续传**: 系统会自动检测未完成的文件并继续处理

### 3. 进度查看
- **查看进度**: `python folder_batch_poem_processor.py --show-progress`
- **实时更新**: 处理过程中会显示详细的进度信息

### 4. 进度管理
- **清理进度**: `python folder_batch_poem_processor.py --cleanup`
- **重新开始**: 清理进度文件后可以重新开始处理

## 📋 使用示例

### 开始新的处理
```bash
# 处理所有文件
python folder_batch_poem_processor.py

# 处理部分文件（例如前10个文件）
python folder_batch_poem_processor.py --end-file 10

# 处理指定范围的文件
python folder_batch_poem_processor.py --start-file 5 --end-file 15
```

### 暂停处理
```bash
# 运行处理命令
python folder_batch_poem_processor.py

# 在终端中按 Ctrl+C 暂停
# 系统会显示：⏸️ 收到暂停信号，正在保存进度...
```

### 恢复处理
```bash
# 恢复之前的处理
python folder_batch_poem_processor.py --resume

# 系统会显示：🔄 检测到未完成的处理任务，正在恢复...
```

### 查看进度
```bash
# 查看当前处理进度
python folder_batch_poem_processor.py --show-progress

# 输出示例：
# 📊 处理进度摘要
# 📈 状态: ▶️ in_progress
# 📁 文件进度: 5/20 (25.0%)
# 📊 剩余文件: 15
# ❌ 失败文件: 0
# 📄 当前文件: 006.json
# 📝 当前进度: 12/16
```

### 清理进度
```bash
# 清理进度文件（重新开始）
python folder_batch_poem_processor.py --cleanup

# 系统会显示：✅ 进度文件已清理
```

## 🎪 进度显示说明

### 进度摘要包含的信息
- **状态**: 处理状态（未开始、进行中、暂停、完成、失败）
- **文件进度**: 已处理文件数/总文件数 (完成百分比)
- **剩余文件**: 还需要处理的文件数量
- **失败文件**: 处理失败的文件数量
- **当前文件**: 正在处理的文件名称
- **当前进度**: 当前文件已处理诗歌数/总诗歌数
- **统计信息**: 总诗歌数、成功分析数、失败分析数
- **时间信息**: 开始时间和最后更新时间

### 状态图标说明
- `▶️`: 处理进行中
- `⏸️`: 处理已暂停
- `✅`: 处理已完成
- `❌`: 处理失败
- `❓`: 未知状态

## 🔄 处理流程示例

### 场景1: 完整处理流程
```bash
# 1. 开始处理
python folder_batch_poem_processor.py

# 2. 处理过程中按 Ctrl+C 暂停
# 3. 查看进度
python folder_batch_poem_processor.py --show-progress

# 4. 恢复处理
python folder_batch_poem_processor.py --resume

# 5. 处理完成后查看最终统计
```

### 场景2: 分批次处理
```bash
# 1. 处理前10个文件
python folder_batch_poem_processor.py --end-file 10

# 2. 暂停后继续处理11-20个文件
python folder_batch_poem_processor.py --start-file 11 --end-file 20 --resume
```

### 场景3: 处理失败后重新开始
```bash
# 1. 清理进度文件
python folder_batch_poem_processor.py --cleanup

# 2. 重新开始处理
python folder_batch_poem_processor.py
```

## ⚠️ 注意事项

1. **进度文件**: 系统会自动创建 `processing_progress.json` 文件保存进度，请不要手动修改此文件
2. **文件完整性**: 暂停时已完成的文件会正常保存，不会丢失数据
3. **网络中断**: 如果因网络问题中断，可以使用 `--resume` 参数恢复
4. **磁盘空间**: 确保有足够的磁盘空间保存处理结果
5. **API限制**: 注意API调用频率限制，系统会自动控制请求间隔

## 🛠️ 故障排除

### 问题1: 进度文件损坏
```bash
# 清理损坏的进度文件
python folder_batch_poem_processor.py --cleanup

# 重新开始处理
python folder_batch_poem_processor.py
```

### 问题2: 恢复失败
```bash
# 查看当前进度状态
python folder_batch_poem_processor.py --show-progress

# 如果状态异常，清理后重新开始
python folder_batch_poem_processor.py --cleanup
```

### 问题3: 处理卡住
```bash
# 按 Ctrl+C 暂停
# 查看进度确认状态
python folder_batch_poem_processor.py --show-progress

# 恢复处理
python folder_batch_poem_processor.py --resume
```

## 📊 进度文件结构

`processing_progress.json` 文件结构：
```json
{
  "status": "in_progress",
  "start_time": "2025-11-24T09:30:00",
  "last_update": "2025-11-24T09:35:00",
  "total_files": 20,
  "processed_files": ["001.json", "002.json", "003.json"],
  "current_file": "004.json",
  "current_file_poems": 16,
  "current_file_processed": 8,
  "failed_files": [],
  "statistics": {
    "total_poems": 48,
    "successful_analysis": 45,
    "failed_analysis": 3
  }
}
```

## 🎉 总结

新的暂停和续传功能让您可以：
- ✅ 随时暂停处理，不会丢失进度
- ✅ 在任意时间恢复处理
- ✅ 实时查看处理进度
- ✅ 灵活管理处理任务
- ✅ 处理大量数据时更加方便

现在您可以放心地处理大量诗歌数据，无需担心中断问题！