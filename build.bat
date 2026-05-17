@echo off
chcp 65001 >nul
echo ========================================
echo   视频解析工具打包脚本（终端版）
echo ========================================
echo.

echo [1/3] 清理旧的打包文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist lookingVideo.spec del /q lookingVideo.spec
echo 清理完成！
echo.

echo [2/3] 开始打包...
pyinstaller ^
    --name="视频解析工具" ^
    --onedir ^
    --console ^
    --icon=logo.ico ^
    --add-data "logo.ico;." ^
    --hidden-import=requests ^
    --hidden-import=bs4 ^
    --hidden-import=DrissionPage ^
    --hidden-import=rich ^
    --collect-submodules rich ^
    --collect-all DrissionPage ^
    lookingVideo.py

echo.
echo [3/3] 打包完成！
echo.
echo 可执行文件位置: dist\视频解析工具\视频解析工具.exe
echo.
pause
