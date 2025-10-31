# 🪟 PDF Spirit Android - Windows Build Guide

## 🚀 Super Simple Windows Build (2 Commands)

```cmd
# 1. Setup build environment (one time only)
setup_windows.bat

# 2. Build your APK
build_windows.bat
```

**That's it! Your Android APK will be ready!** 📱

## 🎯 What Happens

### Step 1: `setup_windows.bat`
- ✅ **Installs WSL** (Windows Subsystem for Linux) if needed
- ✅ **Installs Ubuntu** distribution  
- ✅ **Sets up build environment** with all dependencies
- ✅ **Installs Android SDK/NDK** automatically
- ⏱️ **Takes 10-15 minutes** (one time only)

### Step 2: `build_windows.bat`  
- ✅ **Builds APK** using WSL Ubuntu
- ✅ **Copies APK** back to Windows
- ✅ **Shows install instructions**
- ⏱️ **Takes 5-10 minutes**

## 📁 Result

After building, you'll find:
- `bin\pdfspirit-1.0-debug.apk` - Your Android app (~15-20 MB)
- Ready to install on GrapheneOS
- Complete native Android app with touch UI

## 📱 Installation on GrapheneOS

### Option 1: Manual Install (Recommended)
1. **Copy** `bin\pdfspirit-1.0-debug.apk` to your phone
2. **Enable** "Install unknown apps" in Android Settings
3. **Tap** the APK file to install
4. **Done!** Look for "PDF Spirit" in your app drawer

### Option 2: ADB Install
```cmd
# Connect phone via USB with USB debugging enabled
adb install bin\pdfspirit-1.0-debug.apk
```

## 🎨 Your App Features

- **📄 Auto-scan Downloads** - Finds PDFs automatically
- **👆 One-tap processing** - Simple touch interface
- **📊 Progress indicators** - Visual feedback
- **✅ Success notifications** - Shows where files saved
- **📱 Native Android UI** - Feels like a real app
- **🔒 Completely offline** - Perfect for GrapheneOS privacy

## 🛠 Troubleshooting

### WSL Issues?
```cmd
# Check WSL status
wsl --status

# Update WSL
wsl --update

# Restart WSL
wsl --shutdown
```

### Build Fails?
```cmd
# Clean build and retry
wsl cd /home/%USERNAME%/pdf_spirit_build && ./build_apk.sh clean
build_windows.bat
```

### APK Not Found?
- Check `bin\` folder in the android_app directory
- Look for error messages in the build output
- Try running setup again if first build fails

## 🎯 Why WSL?

- **Android builds require Linux** - WSL provides this on Windows
- **Automatic setup** - No manual Linux configuration needed  
- **Integrated experience** - Build from Windows, get Windows APK
- **Best of both worlds** - Windows convenience + Linux build power

## 🔒 Privacy Benefits

Your PDF Spirit app:
- ✅ **No internet permissions** - Works completely offline
- ✅ **No tracking** - Zero data collection
- ✅ **Local processing** - Files never leave your device
- ✅ **Open source** - You can audit all code
- ✅ **GrapheneOS perfect** - Respects your privacy choices

## 🎉 Final Result

You'll have a **professional Android app** that:
- Installs like any Android app
- Has native touch interface
- Processes PDFs in seconds  
- Works completely offline
- Respects GrapheneOS privacy
- No ads, no tracking, no internet required

**The PDF Spirit has achieved Windows-to-Android transcendence!** 🪟➡️📱✨

## 🚀 Ready to Build?

Just double-click `setup_windows.bat` and let the magic happen!
