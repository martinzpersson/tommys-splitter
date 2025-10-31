#!/bin/bash
# PDF Spirit Android Build Environment Setup
# Run this script to set up everything needed to build the APK

set -e  # Exit on any error

echo "🚀 PDF Spirit Android Build Setup"
echo "=================================="
echo

# Check if running on WSL/Linux
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ -n "$WSL_DISTRO_NAME" ]]; then
    echo "✅ Linux/WSL environment detected"
else
    echo "❌ This script requires Linux or WSL"
    echo "Please install WSL on Windows or run on Linux"
    exit 1
fi

# Update system packages
echo "📦 Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install required system packages
echo "🔧 Installing build dependencies..."
sudo apt install -y \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    python3 \
    python3-pip \
    python3-venv \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    build-essential \
    ccache \
    m4 \
    libc6-dev \
    libgmp-dev \
    libmpc-dev \
    libmpfr-dev \
    libltdl-dev

# Set JAVA_HOME
echo "☕ Setting up Java environment..."
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
echo "export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64" >> ~/.bashrc

# Create Python virtual environment
echo "🐍 Setting up Python environment..."
python3 -m venv pdf_spirit_build_env
source pdf_spirit_build_env/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install Python build tools
echo "🛠️ Installing Python build tools..."
pip install \
    buildozer \
    cython \
    kivy \
    PyPDF2

# Create buildozer directory
echo "📁 Setting up buildozer cache..."
mkdir -p ~/.buildozer

# Download Android SDK/NDK (this will happen automatically on first build)
echo "📱 Preparing Android build tools..."
echo "Note: Android SDK and NDK will be downloaded automatically on first build"

# Set up environment variables
echo "🌍 Setting up environment variables..."
cat >> ~/.bashrc << 'EOF'

# PDF Spirit Build Environment
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin
export ANDROID_HOME=$HOME/.buildozer/android/platform/android-sdk
export ANDROID_SDK_ROOT=$ANDROID_HOME
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
EOF

# Create build script
echo "📝 Creating build script..."
cat > build_apk.sh << 'EOF'
#!/bin/bash
# PDF Spirit APK Build Script

set -e

echo "🏗️ Building PDF Spirit APK..."
echo "============================="
echo

# Activate virtual environment
source pdf_spirit_build_env/bin/activate

# Set environment variables
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin

# Clean previous builds (optional)
if [ "$1" == "clean" ]; then
    echo "🧹 Cleaning previous builds..."
    buildozer android clean
fi

# Build debug APK
echo "🔨 Building debug APK..."
buildozer android debug

# Check if build was successful
if [ -f "bin/pdfspirit-1.0-debug.apk" ]; then
    echo
    echo "✅ Build successful!"
    echo "📱 APK location: bin/pdfspirit-1.0-debug.apk"
    echo "📊 APK size: $(du -h bin/pdfspirit-1.0-debug.apk | cut -f1)"
    echo
    echo "🚀 To install on your phone:"
    echo "   1. Enable 'Install unknown apps' in Android settings"
    echo "   2. Copy APK to your phone"
    echo "   3. Tap the APK file to install"
    echo
    echo "📋 Or use ADB:"
    echo "   adb install bin/pdfspirit-1.0-debug.apk"
else
    echo "❌ Build failed! Check the output above for errors."
    exit 1
fi
EOF

chmod +x build_apk.sh

# Create release build script
echo "📝 Creating release build script..."
cat > build_release.sh << 'EOF'
#!/bin/bash
# PDF Spirit Release APK Build Script

set -e

echo "🏗️ Building PDF Spirit Release APK..."
echo "===================================="
echo

# Activate virtual environment
source pdf_spirit_build_env/bin/activate

# Set environment variables
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin

# Build release APK
echo "🔨 Building release APK..."
buildozer android release

# Check if build was successful
if [ -f "bin/pdfspirit-1.0-release-unsigned.apk" ]; then
    echo
    echo "✅ Release build successful!"
    echo "📱 APK location: bin/pdfspirit-1.0-release-unsigned.apk"
    echo "📊 APK size: $(du -h bin/pdfspirit-1.0-release-unsigned.apk | cut -f1)"
    echo
    echo "⚠️  Note: This APK is unsigned and needs to be signed for distribution"
    echo "🔐 To sign the APK, run: ./sign_apk.sh"
else
    echo "❌ Build failed! Check the output above for errors."
    exit 1
fi
EOF

chmod +x build_release.sh

# Create APK signing script
echo "📝 Creating APK signing script..."
cat > sign_apk.sh << 'EOF'
#!/bin/bash
# PDF Spirit APK Signing Script

set -e

echo "🔐 Signing PDF Spirit APK..."
echo "============================"
echo

# Check if unsigned APK exists
if [ ! -f "bin/pdfspirit-1.0-release-unsigned.apk" ]; then
    echo "❌ Unsigned APK not found. Run ./build_release.sh first."
    exit 1
fi

# Check if keystore exists
if [ ! -f "pdfspirit.keystore" ]; then
    echo "🔑 Creating signing keystore..."
    keytool -genkey -v \
        -keystore pdfspirit.keystore \
        -alias pdfspirit \
        -keyalg RSA \
        -keysize 2048 \
        -validity 10000
fi

# Sign the APK
echo "✍️ Signing APK..."
jarsigner -verbose \
    -sigalg SHA1withRSA \
    -digestalg SHA1 \
    -keystore pdfspirit.keystore \
    bin/pdfspirit-1.0-release-unsigned.apk \
    pdfspirit

# Rename signed APK
mv bin/pdfspirit-1.0-release-unsigned.apk bin/pdfspirit-1.0-release-signed.apk

echo
echo "✅ APK signed successfully!"
echo "📱 Signed APK: bin/pdfspirit-1.0-release-signed.apk"
echo "📊 APK size: $(du -h bin/pdfspirit-1.0-release-signed.apk | cut -f1)"
EOF

chmod +x sign_apk.sh

# Create quick install script
echo "📝 Creating install script..."
cat > install_apk.sh << 'EOF'
#!/bin/bash
# PDF Spirit APK Install Script

set -e

echo "📱 Installing PDF Spirit APK..."
echo "==============================="
echo

# Find the APK to install
if [ -f "bin/pdfspirit-1.0-release-signed.apk" ]; then
    APK_FILE="bin/pdfspirit-1.0-release-signed.apk"
    echo "🔐 Installing signed release APK..."
elif [ -f "bin/pdfspirit-1.0-debug.apk" ]; then
    APK_FILE="bin/pdfspirit-1.0-debug.apk"
    echo "🐛 Installing debug APK..."
else
    echo "❌ No APK found. Build the app first with ./build_apk.sh"
    exit 1
fi

# Check if ADB is available
if ! command -v adb &> /dev/null; then
    echo "❌ ADB not found. Please install Android SDK platform-tools"
    echo "Or manually copy $APK_FILE to your phone and install"
    exit 1
fi

# Check if device is connected
if ! adb devices | grep -q "device$"; then
    echo "❌ No Android device connected via ADB"
    echo "📋 Manual installation:"
    echo "   1. Copy $APK_FILE to your phone"
    echo "   2. Enable 'Install unknown apps' in settings"
    echo "   3. Tap the APK file to install"
    exit 1
fi

# Install APK
echo "🚀 Installing APK via ADB..."
adb install -r "$APK_FILE"

echo
echo "✅ PDF Spirit installed successfully!"
echo "📱 Look for 'PDF Spirit' in your app drawer"
EOF

chmod +x install_apk.sh

# Create all-in-one script
echo "📝 Creating all-in-one build and install script..."
cat > build_and_install.sh << 'EOF'
#!/bin/bash
# PDF Spirit - Build and Install in One Command

set -e

echo "🚀 PDF Spirit - Build and Install"
echo "=================================="
echo

# Build APK
./build_apk.sh

echo
echo "⏳ Waiting 3 seconds before installation..."
sleep 3

# Install APK
./install_apk.sh

echo
echo "🎉 PDF Spirit is ready to use on your phone!"
EOF

chmod +x build_and_install.sh

echo
echo "✅ Build environment setup complete!"
echo
echo "🎯 Next Steps:"
echo "=============="
echo "1. Restart your terminal (or run: source ~/.bashrc)"
echo "2. Navigate to the android_app directory"
echo "3. Run one of these commands:"
echo
echo "   🔨 Build debug APK:"
echo "      ./build_apk.sh"
echo
echo "   🏗️ Build release APK:"
echo "      ./build_release.sh"
echo
echo "   📱 Build and install in one command:"
echo "      ./build_and_install.sh"
echo
echo "   🧹 Clean build (if needed):"
echo "      ./build_apk.sh clean"
echo
echo "📁 Your APK will be created in the 'bin/' directory"
echo
echo "🎉 The PDF Spirit Android app is ready to build!"
