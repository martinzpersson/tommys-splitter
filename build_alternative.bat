@echo off
title PDF Spirit - Alternative Build Method

echo.
echo 🚀 PDF Spirit APK - Alternative Build Method
echo ============================================
echo.

echo 📋 Since WSL needs a restart, let's try an alternative approach...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ from python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python found!

REM Check if we can install buildozer directly on Windows
echo.
echo 🔧 Attempting Windows-native build setup...
echo.

REM Install required packages
echo 📦 Installing build dependencies...
pip install --upgrade pip
pip install buildozer cython kivy PyPDF2

if %errorlevel% neq 0 (
    echo.
    echo ❌ Package installation failed.
    echo.
    echo 💡 Alternative options:
    echo.
    echo Option 1 - Restart and use WSL:
    echo   1. Restart your computer
    echo   2. Run: setup_windows.bat
    echo   3. Run: build_windows.bat
    echo.
    echo Option 2 - Use online build service:
    echo   1. Upload your code to GitHub
    echo   2. Use GitHub Actions to build APK
    echo   3. Download the built APK
    echo.
    echo Option 3 - Manual APK creation:
    echo   We can create a simpler APK using other tools
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Dependencies installed!
echo.

REM Try to build
echo 🔨 Attempting to build APK...
echo.

buildozer android debug

if exist "bin\pdfspirit-1.0-debug.apk" (
    echo.
    echo ✅ Build successful!
    echo 📱 APK: bin\pdfspirit-1.0-debug.apk
    echo.
) else (
    echo.
    echo ❌ Windows-native build not supported.
    echo.
    echo 🎯 Recommended next steps:
    echo.
    echo 1. RESTART your computer (to complete WSL installation)
    echo 2. Run: setup_windows.bat
    echo 3. Run: build_windows.bat
    echo.
    echo This will give you a working APK in about 20 minutes total.
    echo.
)

pause
