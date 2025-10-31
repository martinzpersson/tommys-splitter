# 📱 PDF Spirit Android App - Build Instructions

## 🎯 What You're Building
A **native Android APK** that runs directly on GrapheneOS with:
- **Touch-friendly interface** with buttons and file lists
- **Native file access** to Downloads and Documents folders
- **Progress indicators** during PDF processing
- **No internet required** - completely offline
- **Material Design** inspired UI

## 🛠 Build Methods

### Method 1: Linux/WSL (Recommended)

#### Prerequisites
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Install buildozer
pip3 install --user buildozer cython
```

#### Build Process
```bash
# Navigate to android_app directory
cd PDFSpirit/android_app/

# Initialize buildozer (first time only)
buildozer init

# Build debug APK
buildozer android debug

# Build release APK (for distribution)
buildozer android release
```

#### Find Your APK
```bash
# Debug APK location
ls bin/pdfspirit-1.0-debug.apk

# Release APK location  
ls bin/pdfspirit-1.0-release-unsigned.apk
```

### Method 2: Docker (Cross-Platform)

#### Create Docker Build Environment
```dockerfile
# Dockerfile for PDF Spirit build
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    git zip unzip openjdk-17-jdk python3-pip autoconf libtool \
    pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev \
    libtinfo5 cmake libffi-dev libssl-dev

RUN pip3 install buildozer cython

WORKDIR /app
COPY . .

CMD ["buildozer", "android", "debug"]
```

#### Build with Docker
```bash
# Build the Docker image
docker build -t pdfspirit-builder .

# Run the build
docker run -v $(pwd):/app pdfspirit-builder

# Extract APK
docker cp container_id:/app/bin/pdfspirit-1.0-debug.apk ./
```

### Method 3: GitHub Actions (Automated)

Create `.github/workflows/build.yml`:
```yaml
name: Build Android APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y openjdk-17-jdk
        pip install buildozer cython
    
    - name: Build APK
      run: |
        cd android_app
        buildozer android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: pdfspirit-apk
        path: android_app/bin/*.apk
```

## 📱 Installation on GrapheneOS

### Method 1: Direct Install
```bash
# Enable "Install unknown apps" for your file manager
# Copy APK to phone
# Tap APK file to install
```

### Method 2: ADB Install
```bash
# Enable Developer Options and USB Debugging
adb install pdfspirit-1.0-debug.apk
```

### Method 3: F-Droid (Future)
- Could potentially submit to F-Droid repository
- Requires meeting F-Droid guidelines
- Provides automatic updates

## 🎨 App Features

### Main Screen
- **Header**: PDF Spirit logo and description
- **Scan Button**: Automatically finds PDFs in Downloads
- **Choose File Button**: Manual file picker
- **File List**: Shows found PDFs with file sizes
- **Process Buttons**: One-tap processing per file

### Processing Screen
- **Progress Bar**: Visual processing progress
- **Status Text**: Current processing step
- **Cancel Button**: Stop processing if needed

### Results
- **Success Popup**: Shows output file location
- **Error Popup**: Shows any processing errors
- **Auto-refresh**: Updates file list after processing

## 🔧 Customization Options

### Change App Icon
Replace `icon.png` with your custom icon (512x512 px recommended)

### Modify Colors/Theme
Edit the Kivy styling in `main.py`:
```python
# Custom colors
primary_color = [0.2, 0.6, 0.8, 1]  # Blue
success_color = [0.2, 0.8, 0.2, 1]  # Green
error_color = [0.8, 0.2, 0.2, 1]    # Red
```

### Add Features
- **Batch processing**: Process all PDFs at once
- **Settings screen**: Configure output folder, quality, etc.
- **File preview**: Show PDF thumbnails
- **Share integration**: Direct sharing to print apps

## 🐛 Troubleshooting

### Build Errors
```bash
# Clean build cache
buildozer android clean

# Update buildozer
pip install --upgrade buildozer

# Check Java version
java -version  # Should be 17+
```

### Runtime Errors
```bash
# Check Android logs
adb logcat | grep python

# Debug on device
buildozer android debug deploy run logcat
```

### Permissions Issues
The app requests:
- `READ_EXTERNAL_STORAGE`
- `WRITE_EXTERNAL_STORAGE`

Make sure these are granted in Android settings.

## 📦 Distribution

### Signing for Release
```bash
# Generate signing key
keytool -genkey -v -keystore pdfspirit.keystore -alias pdfspirit -keyalg RSA -keysize 2048 -validity 10000

# Build signed release
buildozer android release

# Sign APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore pdfspirit.keystore bin/pdfspirit-1.0-release-unsigned.apk pdfspirit
```

### File Size Optimization
- Final APK size: ~15-20 MB
- Includes Python runtime and PyPDF2
- No unnecessary dependencies

## 🎯 Result

You'll have a **native Android app** that:
- ✅ **Installs like any Android app**
- ✅ **Works completely offline**
- ✅ **Integrates with Android file system**
- ✅ **Respects GrapheneOS privacy**
- ✅ **Professional UI/UX**
- ✅ **Fast PDF processing**

**The PDF Spirit has achieved its final form - a true native Android citizen!** 📱✨
