#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进度管理器 - 支持暂停和续传功能
"""

import os
import json
import time
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ProgressManager:
    """进度管理器 - 支持暂停和续传功能"""
    
    def __init__(self, progress_file: str = "processing_progress.json"):
        """
        初始化进度管理器
        
        Args:
            progress_file: 进度文件路径
        """
        self.progress_file = progress_file
        self.progress_data = self._load_progress()
    
    def _load_progress(self) -> Dict[str, Any]:
        """加载进度数据"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"加载进度文件失败: {e}，创建新的进度文件")
        
        # 默认进度数据
        return {
            "status": "not_started",  # not_started, in_progress, paused, completed, failed
            "start_time": None,
            "last_update": None,
            "total_files": 0,
            "processed_files": [],
            "current_file": None,
            "current_file_poems": 0,
            "current_file_processed": 0,
            "failed_files": [],
            "statistics": {
                "total_poems": 0,
                "successful_analysis": 0,
                "failed_analysis": 0
            }
        }
    
    def save_progress(self):
        """保存进度数据"""
        self.progress_data["last_update"] = datetime.now().isoformat()
        
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.progress_data, f, ensure_ascii=False, indent=2)
            logger.debug(f"进度已保存到: {self.progress_file}")
        except Exception as e:
            logger.error(f"保存进度失败: {e}")
    
    def start_processing(self, total_files: int):
        """开始处理"""
        self.progress_data.update({
            "status": "in_progress",
            "start_time": datetime.now().isoformat(),
            "total_files": total_files,
            "processed_files": [],
            "current_file": None,
            "current_file_poems": 0,
            "current_file_processed": 0,
            "failed_files": [],
            "statistics": {
                "total_poems": 0,
                "successful_analysis": 0,
                "failed_analysis": 0
            }
        })
        self.save_progress()
        logger.info(f"开始处理 {total_files} 个文件")
    
    def set_current_file(self, file_path: str, total_poems: int):
        """设置当前处理文件"""
        file_name = os.path.basename(file_path)
        self.progress_data.update({
            "current_file": file_name,
            "current_file_poems": total_poems,
            "current_file_processed": 0
        })
        self.save_progress()
        logger.info(f"开始处理文件: {file_name} (共 {total_poems} 首诗歌)")
    
    def update_file_progress(self, processed_count: int, successful_count: int = None):
        """更新文件处理进度"""
        self.progress_data["current_file_processed"] = processed_count
        
        if successful_count is not None:
            self.progress_data["statistics"]["successful_analysis"] = successful_count
        
        self.save_progress()
    
    def complete_file(self, file_path: str, successful_poems: int, total_poems: int):
        """完成文件处理"""
        file_name = os.path.basename(file_path)
        
        # 添加到已处理文件列表
        if file_name not in self.progress_data["processed_files"]:
            self.progress_data["processed_files"].append(file_name)
        
        # 更新统计
        self.progress_data["statistics"]["total_poems"] += total_poems
        self.progress_data["statistics"]["successful_analysis"] += successful_poems
        self.progress_data["statistics"]["failed_analysis"] += (total_poems - successful_poems)
        
        # 重置当前文件状态
        self.progress_data["current_file"] = None
        self.progress_data["current_file_poems"] = 0
        self.progress_data["current_file_processed"] = 0
        
        self.save_progress()
        logger.info(f"完成文件: {file_name} (成功: {successful_poems}/{total_poems})")
    
    def mark_file_failed(self, file_path: str, error_message: str):
        """标记文件处理失败"""
        file_name = os.path.basename(file_path)
        
        self.progress_data["failed_files"].append({
            "file": file_name,
            "error": error_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # 重置当前文件状态
        self.progress_data["current_file"] = None
        self.progress_data["current_file_poems"] = 0
        self.progress_data["current_file_processed"] = 0
        
        self.save_progress()
        logger.error(f"文件处理失败: {file_name} - {error_message}")
    
    def pause_processing(self):
        """暂停处理"""
        self.progress_data["status"] = "paused"
        self.save_progress()
        logger.info("处理已暂停")
    
    def resume_processing(self):
        """恢复处理"""
        self.progress_data["status"] = "in_progress"
        self.save_progress()
        logger.info("处理已恢复")
    
    def complete_processing(self):
        """完成处理"""
        self.progress_data["status"] = "completed"
        self.save_progress()
        logger.info("处理已完成")
    
    def get_remaining_files(self, all_files: List[str]) -> List[str]:
        """获取剩余需要处理的文件"""
        processed_files = set(self.progress_data["processed_files"])
        failed_files = set([f["file"] for f in self.progress_data["failed_files"]])
        
        # 当前正在处理的文件
        current_file = self.progress_data["current_file"]
        if current_file and current_file not in processed_files:
            processed_files.add(current_file)
        
        remaining_files = [f for f in all_files if os.path.basename(f) not in processed_files and os.path.basename(f) not in failed_files]
        
        return remaining_files
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """获取进度摘要"""
        total_files = self.progress_data["total_files"]
        processed_files = len(self.progress_data["processed_files"])
        failed_files = len(self.progress_data["failed_files"])
        remaining_files = total_files - processed_files - failed_files
        
        stats = self.progress_data["statistics"]
        
        return {
            "status": self.progress_data["status"],
            "total_files": total_files,
            "processed_files": processed_files,
            "failed_files": failed_files,
            "remaining_files": remaining_files,
            "progress_percentage": (processed_files / total_files * 100) if total_files > 0 else 0,
            "current_file": self.progress_data["current_file"],
            "current_file_progress": f"{self.progress_data['current_file_processed']}/{self.progress_data['current_file_poems']}",
            "statistics": stats,
            "start_time": self.progress_data["start_time"],
            "last_update": self.progress_data["last_update"]
        }
    
    def print_progress_summary(self):
        """打印进度摘要"""
        summary = self.get_progress_summary()
        
        print("\n" + "="*60)
        print("📊 处理进度摘要")
        print("="*60)
        
        status_icons = {
            "not_started": "⏸️",
            "in_progress": "▶️", 
            "paused": "⏸️",
            "completed": "✅",
            "failed": "❌"
        }
        
        print(f"📈 状态: {status_icons.get(summary['status'], '❓')} {summary['status']}")
        print(f"📁 文件进度: {summary['processed_files']}/{summary['total_files']} ({summary['progress_percentage']:.1f}%)")
        print(f"📊 剩余文件: {summary['remaining_files']}")
        print(f"❌ 失败文件: {summary['failed_files']}")
        
        if summary['current_file']:
            print(f"📄 当前文件: {summary['current_file']}")
            print(f"📝 当前进度: {summary['current_file_progress']}")
        
        stats = summary['statistics']
        print(f"\n📚 诗歌统计:")
        print(f"  总诗歌数: {stats['total_poems']}")
        print(f"  成功分析: {stats['successful_analysis']}")
        print(f"  失败分析: {stats['failed_analysis']}")
        
        if stats['total_poems'] > 0:
            success_rate = stats['successful_analysis'] / stats['total_poems'] * 100
            print(f"  成功率: {success_rate:.1f}%")
        
        if summary['start_time']:
            start_time = datetime.fromisoformat(summary['start_time'])
            print(f"⏰ 开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if summary['last_update']:
            last_update = datetime.fromisoformat(summary['last_update'])
            print(f"🔄 最后更新: {last_update.strftime('%Y-%m-%d %H:%M:%S')}")

def check_resume_processing() -> bool:
    """检查是否可以恢复处理"""
    progress_file = "processing_progress.json"
    
    if not os.path.exists(progress_file):
        return False
    
    try:
        with open(progress_file, 'r', encoding='utf-8') as f:
            progress_data = json.load(f)
        
        return progress_data.get("status") in ["paused", "in_progress"]
    except:
        return False

def cleanup_progress_file():
    """清理进度文件"""
    progress_file = "processing_progress.json"
    if os.path.exists(progress_file):
        os.remove(progress_file)
        logger.info("进度文件已清理")