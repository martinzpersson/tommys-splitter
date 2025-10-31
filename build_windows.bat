@echo off
title PDF Spirit Android Build - Windows

echo.
echo 🏗️ Building PDF Spirit Android APK
echo ===================================
echo.

REM Check if WSL is available
wsl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ WSL not found. Please run setup_windows.bat first.
    pause
    exit /b 1
)

echo 📋 Using WSL Ubuntu for build...
echo.

REM Build APK in WSL
echo 🔨 Building APK (this may take 5-10 minutes)...
echo.

wsl cd /home/%USERNAME%/pdf_spirit_build && source ~/.bashrc && ./build_apk.sh

if %errorlevel% neq 0 (
    echo.
    echo ❌ Build failed. Trying manual approach...
    echo.
    wsl cd /home/%USERNAME%/pdf_spirit_build && source pdf_spirit_build_env/bin/activate && buildozer android debug
)

REM Copy APK back to Windows
echo.
echo 📁 Copying APK to Windows...
if not exist "bin" mkdir bin
wsl cp /home/%USERNAME%/pdf_spirit_build/bin/pdfspirit-1.0-debug.apk ./bin/ 2>nul

REM Check if APK was created
if exist "bin\pdfspirit-1.0-debug.apk" (
    echo.
    echo ✅ Build successful!
    echo.
    echo 📱 APK location: bin\pdfspirit-1.0-debug.apk
    for %%A in ("bin\pdfspirit-1.0-debug.apk") do echo 📊 APK size: %%~zA bytes
    echo.
    echo 🚀 Installation options:
    echo.
    echo   Option 1 - Manual install:
    echo   1. Copy bin\pdfspirit-1.0-debug.apk to your phone
    echo   2. Enable "Install unknown apps" in Android settings  
    echo   3. Tap the APK file to install
    echo.
    echo   Option 2 - ADB install:
    echo   adb install bin\pdfspirit-1.0-debug.apk
    echo.
    echo 🎉 PDF Spirit Android app is ready!
) else (
    echo.
    echo ❌ APK not found. Build may have failed.
    echo.
    echo 💡 Troubleshooting:
    echo 1. Check WSL Ubuntu terminal for errors
    echo 2. Try running: wsl cd /home/%USERNAME%/pdf_spirit_build ^&^& ./build_apk.sh clean
    echo 3. Then run this script again
)

echo.
pause
