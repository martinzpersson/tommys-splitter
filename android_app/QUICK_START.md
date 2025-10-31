# 🚀 PDF Spirit Android - Quick Start

## ⚡ Super Quick Build (5 Commands)

```bash
# 1. Make setup script executable
chmod +x setup_build_environment.sh

# 2. Run setup (installs everything)
./setup_build_environment.sh

# 3. Restart terminal or reload environment
source ~/.bashrc

# 4. Build the APK
./build_apk.sh

# 5. Install on phone (optional)
./install_apk.sh
```

**That's it! Your APK is ready!** 📱

## 📁 What You Get

After building, you'll find:
- `bin/pdfspirit-1.0-debug.apk` - Ready to install APK (~15-20 MB)
- Complete Android app with native UI
- Works offline, no internet required
- Perfect for GrapheneOS privacy

## 🎯 Installation Options

### Option 1: Manual Install
1. Copy `bin/pdfspirit-1.0-debug.apk` to your phone
2. Enable "Install unknown apps" in Android settings
3. Tap the APK file to install

### Option 2: ADB Install
```bash
# Connect phone via USB with USB debugging enabled
adb install bin/pdfspirit-1.0-debug.apk
```

### Option 3: Automatic Install
```bash
# Builds and installs in one command
./build_and_install.sh
```

## 🎨 App Features

- **📄 Scan Downloads** - Automatically finds PDF files
- **👆 One-tap processing** - Simple touch interface  
- **📊 Progress bars** - Visual feedback during processing
- **✅ Success notifications** - Shows where files are saved
- **📱 Native Android UI** - Feels like a real Android app
- **🔒 Privacy focused** - No internet, no tracking

## 🛠 Build Scripts Included

- `build_apk.sh` - Build debug APK
- `build_release.sh` - Build release APK  
- `sign_apk.sh` - Sign APK for distribution
- `install_apk.sh` - Install APK via ADB
- `build_and_install.sh` - Build and install in one command

## 🐛 Troubleshooting

### Build fails?
```bash
# Clean and rebuild
./build_apk.sh clean
```

### Java issues?
```bash
# Check Java version (should be 17+)
java -version
```

### Permission errors?
```bash
# Make scripts executable
chmod +x *.sh
```

## 🎉 Result

You'll have a **professional Android app** that:
- ✅ Installs like any Android app
- ✅ Works completely offline  
- ✅ Has native Android UI/UX
- ✅ Processes PDFs in seconds
- ✅ Respects GrapheneOS privacy
- ✅ No ads, no tracking, no internet

**The PDF Spirit has achieved its final evolution - a true Android native!** 📱✨
