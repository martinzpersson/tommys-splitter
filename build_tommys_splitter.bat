@echo off
title Tommy's Splitter - Android APK Builder

echo.
echo 🚀 Tommy's Splitter - Android APK Builder
echo ==========================================
echo.

REM Check if WSL is ready
echo 📋 Checking WSL status...
wsl --status >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ WSL not ready yet. Please restart your computer first.
    echo.
    echo After restart:
    echo 1. Run this script again
    echo 2. WSL will be ready
    echo 3. Tommy's Splitter APK will be built automatically
    echo.
    pause
    exit /b 1
)

echo ✅ WSL is ready!
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
    echo Then run this script again.
    echo.
    pause
    exit /b 0
)

echo ✅ Ubuntu found!
echo.

REM Setup build environment in WSL
echo 🛠️ Setting up Tommy's Splitter build environment...
echo This may take 10-15 minutes for first-time setup...
echo.

REM Copy files to WSL
echo 📁 Copying files to WSL...
wsl mkdir -p /home/%USERNAME%/tommys_splitter_build
wsl cp -r . /home/%USERNAME%/tommys_splitter_build/ 2>nul || (
    echo Copying files manually...
    for %%f in (*.py *.spec *.md *.txt *.sh *.toml) do (
        wsl cp "%%f" /home/%USERNAME%/tommys_splitter_build/ 2>nul
    )
    wsl mkdir -p /home/%USERNAME%/tommys_splitter_build/tommyssplitter
    for %%f in (tommyssplitter\*.py) do (
        wsl cp "%%f" /home/%USERNAME%/tommys_splitter_build/tommyssplitter/ 2>nul
    )
)

REM Run setup and build in WSL
echo.
echo 🔨 Building Tommy's Splitter APK in WSL...
echo.

wsl cd /home/%USERNAME%/tommys_splitter_build && chmod +x setup_build_environment.sh && ./setup_build_environment.sh

if %errorlevel% neq 0 (
    echo.
    echo ❌ Setup failed. Trying manual build...
    echo.
    wsl cd /home/%USERNAME%/tommys_splitter_build && sudo apt update && sudo apt install -y python3-pip openjdk-17-jdk && pip3 install buildozer cython
)

REM Build the APK
echo.
echo 🏗️ Building Tommy's Splitter APK...
echo.

wsl cd /home/%USERNAME%/tommys_splitter_build && chmod +x build_apk.sh && ./build_apk.sh

if %errorlevel% neq 0 (
    echo.
    echo ❌ Build script failed. Trying direct buildozer...
    echo.
    wsl cd /home/%USERNAME%/tommys_splitter_build && buildozer android debug
)

REM Copy APK back to Windows
echo.
echo 📁 Copying Tommy's Splitter APK to Windows...
if not exist "bin" mkdir bin
wsl cp /home/%USERNAME%/tommys_splitter_build/bin/tommyssplitter-1.0-debug.apk ./bin/ 2>nul

REM Check if APK was created
if exist "bin\tommyssplitter-1.0-debug.apk" (
    echo.
    echo ✅ Tommy's Splitter APK built successfully!
    echo.
    echo 📱 APK location: bin\tommyssplitter-1.0-debug.apk
    for %%A in ("bin\tommyssplitter-1.0-debug.apk") do echo 📊 APK size: %%~zA bytes
    echo.
    echo 🎉 Tommy's Splitter is ready for your GrapheneOS friend!
    echo.
    echo 📋 Installation instructions:
    echo 1. Copy bin\tommyssplitter-1.0-debug.apk to their phone
    echo 2. Enable "Install unknown apps" in Android settings
    echo 3. Tap the APK file to install
    echo 4. Grant storage permissions when prompted
    echo 5. Enjoy perfect PostNord label splitting!
    echo.
    echo 🔒 Privacy features:
    echo - No internet permissions
    echo - No tracking or analytics
    echo - Local processing only
    echo - Perfect for GrapheneOS
    echo.
) else (
    echo.
    echo ❌ APK not found. Build may have failed.
    echo.
    echo 💡 Troubleshooting:
    echo 1. Check WSL Ubuntu terminal for errors
    echo 2. Try running: wsl cd /home/%USERNAME%/tommys_splitter_build ^&^& buildozer android clean
    echo 3. Then run this script again
    echo.
    echo 📧 If issues persist, the GitHub Actions method is available as backup.
)

echo.
pause
