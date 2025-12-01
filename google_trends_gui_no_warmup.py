#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Trends GUI 下载器 v1.4.2 - 无预热版本

功能：
- 图形界面操作
- 可修改关键词列表
- 可设置输出目录
- 实时显示下载进度
- 保存配置，下次自动加载

v1.4.2 更新：
- 优化界面布局：左右分栏（配置区 | 日志区）
- 修复输出目录初始化：始终使用当前工作目录，不暴露其他用户路径
- 优化控件布局和间距

v1.4.1 更新：
- 修复重试计数问题（第一次尝试不算重试）
- 现在：1次尝试 + N次重试（而非N次尝试）

v1.4 更新（最终修复）：
- 移除预热流程
- 每个关键词使用独立的新会话
- 确保数据准确性（经测试验证）
- 推荐等待时间：30-60秒（成功率95%+）
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import json
import os
from datetime import datetime
import sys

# 导入下载核心
import pandas as pd
from pytrends.request import TrendReq
import time
import random


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file='trends_config.json'):
        self.config_file = config_file
        self.default_config = {
            'keywords': ['MOLLY', 'CRYBABY', 'LABUBU', 'SKULLPANDA', 
                        'HIRONO', 'Peach Riot', 'TWINKLE', 'DIMOO'],
            'output_dir': os.getcwd(),
            'wait_min': 30,
            'wait_max': 60,
            'max_retries': 3
        }
    
    def load(self):
        """加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 合并默认配置，但始终使用当前工作目录作为输出目录
                    merged_config = {**self.default_config, **config}
                    # 输出目录始终初始化为当前工作目录，避免暴露其他用户的路径
                    merged_config['output_dir'] = os.getcwd()
                    return merged_config
            except:
                pass
        return self.default_config.copy()
    
    def save(self, config):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False


class TrendsDownloader:
    """核心下载器 - 无预热版本"""
    
    def __init__(self, log_callback=None):
        self.log_callback = log_callback
        self.stop_flag = False
        
    def log(self, message, level='info'):
        """输出日志"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_msg = f"[{timestamp}] {message}"
        
        if self.log_callback:
            self.log_callback(log_msg, level)
        else:
            print(log_msg)
    
    def download_keyword(self, keyword, max_retries=3):
        """下载单个关键词 - 使用独立会话，不预热"""
        if self.stop_flag:
            return pd.DataFrame()
        
        # 第一次尝试 + max_retries次重试
        for attempt in range(max_retries + 1):
            if self.stop_flag:
                return pd.DataFrame()
            
            try:
                if attempt > 0:
                    self.log(f"    🔄 第 {attempt} 次重试 (共 {max_retries} 次重试机会): {keyword}", 'warning')
                    # 指数退避（从第1次重试开始）
                    delay = 30 * (2 ** (attempt - 1))
                    jitter = delay * 0.2 * random.uniform(-1, 1)
                    total_delay = delay + jitter
                    self.log(f"    ⏳ 指数退避等待: {total_delay:.1f} 秒")
                    time.sleep(total_delay)
                
                self.log(f"    📥 正在下载: {keyword}")
                
                # 每次都创建全新会话（关键！）
                pytrends = TrendReq(hl='en-US', tz=360)
                
                # 直接查询，不预热
                pytrends.build_payload(
                    kw_list=[keyword],
                    cat=0,
                    timeframe='today 5-y',
                    geo='',
                    gprop=''
                )
                
                # 获取数据
                data = pytrends.interest_over_time()
                
                if not data.empty:
                    if 'isPartial' in data.columns:
                        data = data.drop('isPartial', axis=1)
                    
                    self.log(f"    ✅ {keyword} 下载成功 (shape: {data.shape})")
                    return data
                else:
                    self.log(f"    ⚠️ {keyword} 返回空数据", 'warning')
                    return pd.DataFrame()
                    
            except Exception as e:
                error_msg = str(e)
                
                if "429" in error_msg:
                    if attempt == 0:
                        self.log(f"    🚫 遇到限速 (429): {keyword} (首次尝试失败)", 'error')
                    else:
                        self.log(f"    🚫 遇到限速 (429): {keyword} (第 {attempt} 次重试失败)", 'error')
                    
                    if attempt == max_retries:
                        self.log(f"    ❌ {keyword} 失败 (已用完所有重试机会)", 'error')
                        return pd.DataFrame()
                    else:
                        self.log(f"    💡 将使用指数退避重试...")
                        continue
                else:
                    self.log(f"    ❌ {keyword} 下载出错: {error_msg}", 'error')
                    return pd.DataFrame()
        
        return pd.DataFrame()
    
    def download_all(self, keywords, wait_min=30, wait_max=60, 
                    max_retries=3, progress_callback=None):
        """下载所有关键词 - 无预热版本"""
        self.stop_flag = False
        
        all_data = pd.DataFrame()
        successful = []
        failed = []
        total = len(keywords)
        
        self.log(f"\n{'='*50}")
        self.log(f"📊 开始下载 {total} 个关键词")
        self.log(f"⚠️ 无预热模式 - 每个关键词使用独立会话")
        self.log(f"{'='*50}")
        
        for i, keyword in enumerate(keywords):
            if self.stop_flag:
                self.log("⏹️ 用户中断下载", 'warning')
                break
            
            self.log(f"\n📊 [{i+1}/{total}] {keyword}")
            
            # 更新进度
            if progress_callback:
                progress_callback(i + 1, total)
            
            # 下载
            data = self.download_keyword(keyword, max_retries)
            
            if not data.empty:
                if all_data.empty:
                    all_data = data
                else:
                    all_data = all_data.join(data, how='outer')
                successful.append(keyword)
            else:
                failed.append(keyword)
            
            # 等待
            if i < total - 1 and not self.stop_flag:
                wait_time = random.uniform(wait_min, wait_max)
                self.log(f"    ⏳ 等待 {wait_time:.1f} 秒...")
                time.sleep(wait_time)
        
        # 总结
        self.log(f"\n{'='*50}")
        self.log(f"📊 下载完成")
        self.log(f"✅ 成功: {len(successful)}/{total}")
        if successful:
            self.log(f"   {successful}")
        if failed:
            self.log(f"❌ 失败: {len(failed)}")
            self.log(f"   {failed}")
        self.log(f"{'='*50}")
        
        return all_data if not all_data.empty else None
    
    def stop(self):
        """停止下载"""
        self.stop_flag = True


class TrendsGUI:
    """主GUI窗口"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Google Trends 下载器 v1.4.2 (无预热版)")
        self.root.geometry("1000x650")
        
        # 配置管理
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load()
        
        # 下载器
        self.downloader = None
        self.download_thread = None
        
        # 创建界面
        self.create_widgets()
        
        # 加载配置
        self.load_config()
    
    def create_widgets(self):
        """创建界面组件 - 左右分栏布局"""
        # 标题
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            title_frame, 
            text="Google Trends 数据下载器 v1.4.2",
            font=('Arial', 16, 'bold')
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="无预热版本 - 每个关键词使用独立会话 - 推荐等待30-60秒",
            font=('Arial', 10),
            foreground='blue'
        )
        subtitle_label.pack()
        
        # 主容器：左右分栏
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # ===== 左侧：配置区域 =====
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 5))
        
        # 关键词设置
        keywords_frame = ttk.LabelFrame(left_frame, text="关键词设置", padding="10")
        keywords_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        ttk.Label(keywords_frame, text="关键词列表（每行一个）:").pack(anchor=tk.W)
        
        self.keywords_text = scrolledtext.ScrolledText(
            keywords_frame, 
            width=35,
            height=12,
            font=('Consolas', 10)
        )
        self.keywords_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 输出设置
        output_frame = ttk.LabelFrame(left_frame, text="输出设置", padding="10")
        output_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(output_frame, text="输出目录:").pack(anchor=tk.W, pady=(0, 5))
        
        dir_frame = ttk.Frame(output_frame)
        dir_frame.pack(fill=tk.X)
        
        self.output_dir_var = tk.StringVar()
        ttk.Entry(
            dir_frame, 
            textvariable=self.output_dir_var,
            width=25
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(
            dir_frame,
            text="浏览",
            command=self.browse_directory,
            width=8
        ).pack(side=tk.LEFT)
        
        # 下载参数
        params_frame = ttk.LabelFrame(left_frame, text="下载参数", padding="10")
        params_frame.pack(fill=tk.X, pady=(0, 5))
        
        # 等待时间
        ttk.Label(params_frame, text="关键词间等待时间:").pack(anchor=tk.W, pady=(0, 5))
        
        wait_frame = ttk.Frame(params_frame)
        wait_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.wait_min_var = tk.IntVar(value=30)
        ttk.Spinbox(
            wait_frame,
            from_=10,
            to=120,
            textvariable=self.wait_min_var,
            width=8
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Label(wait_frame, text="到").pack(side=tk.LEFT, padx=(0, 5))
        
        self.wait_max_var = tk.IntVar(value=60)
        ttk.Spinbox(
            wait_frame,
            from_=10,
            to=120,
            textvariable=self.wait_max_var,
            width=8
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Label(wait_frame, text="秒").pack(side=tk.LEFT)
        
        # 最大重试次数
        ttk.Label(params_frame, text="最大重试次数:").pack(anchor=tk.W, pady=(0, 5))
        
        retry_frame = ttk.Frame(params_frame)
        retry_frame.pack(fill=tk.X)
        
        self.max_retries_var = tk.IntVar(value=3)
        ttk.Spinbox(
            retry_frame,
            from_=1,
            to=10,
            textvariable=self.max_retries_var,
            width=8
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Label(retry_frame, text="次").pack(side=tk.LEFT)
        
        # 控制按钮
        control_frame = ttk.Frame(left_frame, padding="10")
        control_frame.pack(fill=tk.X)
        
        self.start_button = ttk.Button(
            control_frame,
            text="开始下载",
            command=self.start_download
        )
        self.start_button.pack(fill=tk.X, pady=(0, 5))
        
        self.stop_button = ttk.Button(
            control_frame,
            text="停止",
            command=self.stop_download,
            state=tk.DISABLED
        )
        self.stop_button.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(
            control_frame,
            text="保存配置",
            command=self.save_config
        ).pack(fill=tk.X)
        
        # ===== 右侧：日志区域 =====
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # 进度条
        progress_frame = ttk.Frame(right_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(progress_frame, text="下载进度:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 日志输出
        log_frame = ttk.LabelFrame(right_frame, text="下载日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def browse_directory(self):
        """浏览目录"""
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)
    
    def load_config(self):
        """加载配置"""
        # 关键词
        keywords_text = '\n'.join(self.config['keywords'])
        self.keywords_text.delete('1.0', tk.END)
        self.keywords_text.insert('1.0', keywords_text)
        
        # 输出目录
        self.output_dir_var.set(self.config['output_dir'])
        
        # 参数
        self.wait_min_var.set(self.config['wait_min'])
        self.wait_max_var.set(self.config['wait_max'])
        self.max_retries_var.set(self.config['max_retries'])
    
    def save_config(self):
        """保存配置"""
        # 获取关键词
        keywords_text = self.keywords_text.get('1.0', tk.END).strip()
        keywords = [k.strip() for k in keywords_text.split('\n') if k.strip()]
        
        # 更新配置
        self.config['keywords'] = keywords
        self.config['output_dir'] = self.output_dir_var.get()
        self.config['wait_min'] = self.wait_min_var.get()
        self.config['wait_max'] = self.wait_max_var.get()
        self.config['max_retries'] = self.max_retries_var.get()
        
        # 保存
        if self.config_manager.save(self.config):
            messagebox.showinfo("成功", "配置已保存")
        else:
            messagebox.showerror("错误", "配置保存失败")
    
    def log_message(self, message, level='info'):
        """记录日志"""
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        
        # 根据级别设置颜色
        if level == 'error':
            # 可以添加颜色标记
            pass
    
    def update_progress(self, current, total):
        """更新进度"""
        progress = (current / total) * 100
        self.progress_var.set(progress)
    
    def start_download(self):
        """开始下载"""
        # 获取关键词
        keywords_text = self.keywords_text.get('1.0', tk.END).strip()
        keywords = [k.strip() for k in keywords_text.split('\n') if k.strip()]
        
        if not keywords:
            messagebox.showwarning("警告", "请输入至少一个关键词")
            return
        
        # 获取参数
        output_dir = self.output_dir_var.get()
        wait_min = self.wait_min_var.get()
        wait_max = self.wait_max_var.get()
        max_retries = self.max_retries_var.get()
        
        if wait_min > wait_max:
            messagebox.showwarning("警告", "最小等待时间不能大于最大等待时间")
            return
        
        # 禁用开始按钮
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # 清空日志
        self.log_text.delete('1.0', tk.END)
        self.progress_var.set(0)
        
        # 创建下载器
        self.downloader = TrendsDownloader(log_callback=self.log_message)
        
        # 在新线程中下载
        self.download_thread = threading.Thread(
            target=self._download_worker,
            args=(keywords, output_dir, wait_min, wait_max, max_retries)
        )
        self.download_thread.start()
    
    def _download_worker(self, keywords, output_dir, wait_min, wait_max, max_retries):
        """下载工作线程"""
        try:
            # 下载数据
            data = self.downloader.download_all(
                keywords=keywords,
                wait_min=wait_min,
                wait_max=wait_max,
                max_retries=max_retries,
                progress_callback=self.update_progress
            )
            
            # 保存数据
            if data is not None and not data.empty:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'google_trends_{timestamp}.csv'
                filepath = os.path.join(output_dir, filename)
                
                data.to_csv(filepath, encoding='utf-8-sig')
                
                self.log_message(f"\n💾 数据已保存: {filepath}")
                self.log_message(f"📊 数据形状: {data.shape}")
                
                messagebox.showinfo("成功", f"数据已保存到:\n{filepath}")
            else:
                self.log_message("\n❌ 未获取到任何数据", 'error')
                messagebox.showwarning("警告", "未获取到任何数据")
                
        except Exception as e:
            self.log_message(f"\n❌ 错误: {e}", 'error')
            messagebox.showerror("错误", f"下载过程中出错:\n{e}")
        
        finally:
            # 恢复按钮状态
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def stop_download(self):
        """停止下载"""
        if self.downloader:
            self.downloader.stop()
            self.log_message("\n⏹️ 正在停止下载...", 'warning')


def main():
    root = tk.Tk()
    app = TrendsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

