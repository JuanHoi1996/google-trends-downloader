# Google Trends 下载器（图形界面版）

[English](README.md) | 简体中文

一个简单易用的 Google Trends 数据批量下载工具，带图形界面。

## ✨ 特色功能

- 🖥️ **图形界面** - 无需命令行，点击即用
- 📊 **批量下载** - 一次下载多个关键词
- 💾 **自动保存** - 配置自动保存，下次打开自动加载
- 📈 **实时反馈** - 下载进度实时显示
- 🔄 **智能重试** - 遇到限速自动重试
- 🚀 **独立运行** - 可打包成 exe，无需安装 Python

## 🚀 快速开始

### 方法一：下载可执行文件（推荐）

1. 下载 `GoogleTrendsDownloader.exe`
2. 双击运行
3. 设置关键词
4. 点击"开始下载"

### 方法二：运行 Python 脚本

```bash
# 安装依赖
pip install -r requirements.txt

# 运行程序
python google_trends_gui_no_warmup.py
```

## 📖 使用说明

详细使用说明请查看 [USAGE.md](USAGE.md)

### 基本步骤

1. **设置关键词**（左侧，每行一个）
   ```
   MOLLY
   CRYBABY
   LABUBU
   ```

2. **选择输出目录**（点击"浏览"按钮）

3. **调整参数**
   - 等待时间：30-60 秒（推荐）
   - 重试次数：3 次（推荐）

4. **开始下载**（点击"开始下载"按钮）

5. **查看结果**（CSV 文件保存在输出目录）

## 📊 数据说明

- **时间范围**：过去 5 年
- **更新频率**：每周一个数据点
- **数值范围**：0-100（相对热度）
- **输出格式**：CSV

## 🛠️ 打包成 exe

```bash
# 方法一：一键打包（Windows）
.\一键打包.bat

# 方法二：手动打包
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name GoogleTrendsDownloader google_trends_gui_no_warmup.py
```

打包后的文件在 `dist/GoogleTrendsDownloader.exe`

## 📝 版本历史

- **v1.4.2** (2024-11-24) - 优化界面布局，修复输出目录初始化
- **v1.4.1** (2024-11-19) - 修复重试计数显示
- **v1.4.0** (2024-11-10) - 移除预热，确保数据准确性
- **v1.3.0** (2024-10-27) - 添加图形界面

## ❓ 常见问题

### 下载失败，提示 429 错误？

增加等待时间到 40-80 秒，或稍后再试。

### 数据与官网不一致？

确保使用 v1.4.2 版本（无预热模式）。

### SSL 连接错误？

检查网络连接，或尝试使用 VPN。

更多问题请查看 [USAGE.md](USAGE.md)

## 📄 许可证

MIT License

## 🙏 致谢

- [pytrends](https://github.com/GeneralMills/pytrends)
- [pandas](https://pandas.pydata.org/)
- [tkinter](https://docs.python.org/3/library/tkinter.html)

---

**⭐ 如果觉得有用，请给个 Star！**

