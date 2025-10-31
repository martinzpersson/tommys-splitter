@echo off
title PDF Spirit Android Build Setup - Windows

echo.
echo 🚀 PDF Spirit Android Build Setup for Windows
echo ===============================================
echo.

REM Check if WSL is available
echo 📋 Checking for WSL (Windows Subsystem for Linux)...
wsl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ WSL not found. Installing WSL...
    echo.
    echo 🔧 Installing WSL Ubuntu...
    wsl --install -d Ubuntu
    echo.
    echo ✅ WSL installed! Please restart your computer and run this script again.
    echo.
    pause
    exit /b 1
)

echo ✅ WSL found!
echo.

REM Check if Ubuntu is installed
echo 📋 Checking Ubuntu distribution...
wsl -l -v | findstr Ubuntu >nul
if %errorlevel% neq 0 (
    echo.
    echo 🔧 Installing Ubuntu distribution...
    wsl --install -d Ubuntu
    echo.
    echo ✅ Ubuntu installed! Please set up your Ubuntu user account.
    echo.
    pause
)

echo.
echo 🐧 Setting up build environment in WSL Ubuntu...
echo.

REM Copy files to WSL
echo 📁 Copying files to WSL...
wsl mkdir -p /home/%USERNAME%/pdf_spirit_build
wsl cp -r . /home/%USERNAME%/pdf_spirit_build/ 2>nul || (
    echo Copying files manually...
    for %%f in (*.py *.spec *.md *.txt *.sh) do (
        wsl cp "%%f" /home/%USERNAME%/pdf_spirit_build/ 2>nul
    )
)

REM Run setup in WSL
echo.
echo 🛠️ Running setup in WSL Ubuntu...
echo This may take 10-15 minutes for first-time setup...
echo.

wsl cd /home/%USERNAME%/pdf_spirit_build && chmod +x setup_build_environment.sh && ./setup_build_environment.sh

if %errorlevel% neq 0 (
    echo.
    echo ❌ Setup failed. Please check the output above.
    echo.
    echo 💡 Manual setup option:
    echo    1. Open WSL Ubuntu terminal
    echo    2. cd /home/%USERNAME%/pdf_spirit_build
    echo    3. chmod +x setup_build_environment.sh
    echo    4. ./setup_build_environment.sh
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Setup complete!
echo.
echo 🎯 Next steps:
echo 1. Run: build_windows.bat (to build APK)
echo 2. Find your APK in: bin\pdfspirit-1.0-debug.apk
echo 3. Install on your GrapheneOS phone
echo.
pause
