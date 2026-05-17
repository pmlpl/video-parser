@echo off
chcp 65001 >nul
echo ========================================
echo   视频解析工具 GUI 版打包脚本
echo ========================================
echo.

echo [1/3] 清理旧的打包文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist lookingVideo_gui.spec del /q lookingVideo_gui.spec
echo 清理完成！
echo.

echo [2/3] 开始打包 GUI 版本...
pyinstaller ^
    --name="视频解析工具" ^
    --onedir ^
    --windowed ^
    --icon=logo.ico ^
    --hidden-import=requests ^
    --hidden-import=bs4 ^
    --hidden-import=DrissionPage ^
    --hidden-import=tkinter ^
    --collect-all DrissionPage ^
    lookingVideo_gui.py

echo.
echo [3/3] 打包完成！
echo.
echo 可执行文件位置: dist\视频解析工具\视频解析工具.exe
echo.
pause
