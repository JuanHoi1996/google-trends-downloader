# 项目结构说明

```
google-trends-downloader/
│
├── google_trends_gui_no_warmup.py  # 主程序（GUI版本）
├── requirements.txt                # Python 依赖列表
├── 一键打包.bat                    # Windows 打包脚本
│
├── README.md                       # 项目说明（英文）
├── README_CN.md                    # 项目说明（中文）
├── USAGE.md                        # 详细使用指南
├── LICENSE                         # MIT 许可证
│
├── 上传到GitHub.md                 # GitHub 上传教程
├── 一键上传GitHub.ps1              # 一键上传脚本
└── .gitignore                      # Git 忽略文件配置
```

## 📄 文件说明

### 核心文件

#### `google_trends_gui_no_warmup.py`
- **作用**：主程序文件
- **功能**：图形界面的 Google Trends 数据下载器
- **版本**：v1.4.2
- **特点**：无预热模式，确保数据准确性

#### `requirements.txt`
- **作用**：Python 依赖包列表
- **内容**：
  ```
  pytrends>=4.9.0
  pandas>=1.3.0
  ```
- **用法**：`pip install -r requirements.txt`

### 文档文件

#### `README.md` / `README_CN.md`
- **作用**：项目首页说明
- **内容**：
  - 项目简介
  - 主要特性
  - 快速开始
  - 基本使用方法
  - 常见问题

#### `USAGE.md`
- **作用**：详细使用指南
- **内容**：
  - 界面布局说明
  - 完整操作步骤
  - 参数详细说明
  - 高级技巧
  - 故障排除

#### `LICENSE`
- **作用**：开源许可证
- **类型**：MIT License
- **说明**：允许自由使用、修改和分发

### 工具脚本

#### `一键打包.bat`
- **作用**：Windows 平台一键打包脚本
- **功能**：将 Python 脚本打包成 exe 文件
- **依赖**：PyInstaller
- **输出**：`dist/GoogleTrendsDownloader.exe`

#### `一键上传GitHub.ps1`
- **作用**：自动化 GitHub 上传流程
- **功能**：
  - 配置 Git
  - 初始化仓库
  - 提交代码
  - 推送到 GitHub
- **用法**：右键 → "使用 PowerShell 运行"

#### `上传到GitHub.md`
- **作用**：GitHub 上传详细教程
- **内容**：
  - 三种上传方法
  - Personal Access Token 获取方法
  - 常见问题解决

### 配置文件

#### `.gitignore`
- **作用**：Git 忽略文件配置
- **排除内容**：
  - Python 缓存文件（`__pycache__/`, `*.pyc`）
  - 虚拟环境（`venv/`, `env/`）
  - IDE 配置（`.vscode/`, `.idea/`）
  - 个人数据（`*.csv`, `*.xlsx`, `trends_config.json`）
  - 构建产物（`build/`, `dist/`, `*.exe`）

## 🔒 隐私保护

### 不会上传的文件

以下文件类型已在 `.gitignore` 中配置，**不会**上传到 GitHub：

```
❌ trends_config.json    # 个人配置（可能包含路径）
❌ *.csv                 # 下载的数据文件
❌ *.xlsx, *.xls         # Excel 文件
❌ *.pptx                # PowerPoint 文件
❌ *.pdf                 # PDF 文件
❌ *.exe                 # 可执行文件
❌ build/, dist/         # 构建目录
❌ __pycache__/          # Python 缓存
```

### 安全的文件

以下文件**可以安全上传**：

```
✅ google_trends_gui_no_warmup.py  # 不包含个人信息
✅ requirements.txt                # 只有依赖包名称
✅ README.md                       # 项目说明
✅ LICENSE                         # 开源许可证
✅ .gitignore                      # Git 配置
✅ 所有 .md 文档                   # 纯文本文档
```

## 📦 打包后的文件

运行 `一键打包.bat` 后会生成：

```
dist/
└── GoogleTrendsDownloader.exe  # 独立可执行文件（约 30-40 MB）

build/
└── GoogleTrendsDownloader/     # 临时构建文件（可删除）
```

**注意**：
- `dist/` 和 `build/` 目录不会上传到 GitHub
- 可以手动将 `.exe` 文件上传到 GitHub Release

## 🚀 使用流程

### 开发者流程

1. **克隆项目**
   ```bash
   git clone https://github.com/username/google-trends-downloader.git
   cd google-trends-downloader
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行程序**
   ```bash
   python google_trends_gui_no_warmup.py
   ```

4. **打包（可选）**
   ```bash
   .\一键打包.bat
   ```

### 普通用户流程

1. **下载 Release**
   - 访问 GitHub Releases 页面
   - 下载 `GoogleTrendsDownloader.exe`

2. **运行程序**
   - 双击 `GoogleTrendsDownloader.exe`
   - 无需安装 Python

## 📊 版本管理

### 当前版本：v1.4.2

**版本号规则**：`主版本.次版本.修订版本`

- **主版本**：重大功能变更（如 v1 → v2）
- **次版本**：新功能添加（如 v1.3 → v1.4）
- **修订版本**：Bug 修复（如 v1.4.1 → v1.4.2）

### 版本历史

- **v1.4.2** (2024-11-24) - 界面优化，输出目录修复
- **v1.4.1** (2024-11-19) - 重试计数修复
- **v1.4.0** (2024-11-10) - 移除预热，数据准确性修复
- **v1.3.0** (2024-10-27) - 添加 GUI
- **v1.2.0** - 智能重试机制
- **v1.1.0** - 批量下载功能
- **v1.0.0** - 初始版本

## 🤝 贡献指南

如果您想改进这个项目：

1. Fork 这个仓库
2. 创建您的特性分支（`git checkout -b feature/AmazingFeature`）
3. 提交您的修改（`git commit -m 'Add some AmazingFeature'`）
4. 推送到分支（`git push origin feature/AmazingFeature`）
5. 开启一个 Pull Request

## 📞 获取帮助

- 📖 查看 [USAGE.md](USAGE.md) 了解详细使用方法
- 🐛 在 GitHub Issues 报告问题
- 💡 在 GitHub Discussions 提出建议

---

**感谢使用 Google Trends Downloader！** 🎉

