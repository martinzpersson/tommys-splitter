#!/bin/bash
# Tommy's Splitter - Quick Build Script

echo "🚀 Building Tommy's Splitter APK"
echo "================================="
echo

# Wait for package installation to complete
echo "⏳ Waiting for system packages to install..."
while ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; do
    echo "   Waiting for Python and pip..."
    sleep 5
done

echo "✅ Python found!"

# Install buildozer
echo "📦 Installing buildozer..."
pip3 install --user buildozer cython kivy PyPDF2

# Add user bin to PATH
export PATH=$PATH:~/.local/bin

# Build APK
echo "🔨 Building Tommy's Splitter APK..."
buildozer android debug

if [ -f "bin/tommyssplitter-1.0-debug.apk" ]; then
    echo
    echo "✅ Tommy's Splitter APK built successfully!"
    echo "📱 APK: bin/tommyssplitter-1.0-debug.apk"
    ls -lh bin/tommyssplitter-1.0-debug.apk
else
    echo "❌ Build failed. Checking for errors..."
    ls -la bin/
fi
