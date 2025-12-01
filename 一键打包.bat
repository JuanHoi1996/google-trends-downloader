@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo   Google Trends 下载器 - 快速打包
echo ========================================
echo.
echo 正在打包...
echo.
python -m PyInstaller --clean GoogleTrendsDownloader.spec
echo.
if errorlevel 1 (
    echo ❌ 打包失败！
) else (
    echo ========================================
    echo   🎉 打包成功！
    echo ========================================
    echo.
    echo 📁 可执行文件位置: dist\GoogleTrendsDownloader.exe
)
echo.
pause

