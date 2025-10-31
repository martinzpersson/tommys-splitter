#!/usr/bin/env python3
"""
Simple APK Builder for PDF Spirit
Creates basic APK structure without emojis
"""

import os
import sys
import zipfile
import tempfile
from pathlib import Path
import shutil
import subprocess

def build_simple_apk():
    """Create a simple APK structure"""
    
    print("Building PDF Spirit APK Directly")
    print("=================================")
    print()
    
    # Install PyPDF2 if needed
    try:
        import PyPDF2
        print("PyPDF2 found")
    except ImportError:
        print("Installing PyPDF2...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PyPDF2"], check=True)
    
    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp())
    apk_dir = temp_dir / "apk"
    apk_dir.mkdir()
    
    print(f"Working directory: {temp_dir}")
    
    # Create Android APK structure
    print("Creating APK structure...")
    
    # Create directories
    (apk_dir / "META-INF").mkdir()
    (apk_dir / "assets").mkdir()
    (apk_dir / "res" / "drawable").mkdir(parents=True)
    (apk_dir / "res" / "values").mkdir(parents=True)
    
    # AndroidManifest.xml
    manifest_content = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="org.pdfspirit.app"
    android:versionCode="1"
    android:versionName="1.0">
    
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    
    <application
        android:label="PDF Spirit"
        android:icon="@drawable/icon">
        
        <activity
            android:name=".MainActivity"
            android:label="PDF Spirit"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>'''
    
    with open(apk_dir / "AndroidManifest.xml", "w", encoding='utf-8') as f:
        f.write(manifest_content)
    
    # strings.xml
    strings_content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">PDF Spirit</string>
</resources>'''
    
    with open(apk_dir / "res" / "values" / "strings.xml", "w", encoding='utf-8') as f:
        f.write(strings_content)
    
    # Simple icon (vector drawable)
    icon_content = '''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="48dp"
    android:height="48dp"
    android:viewportWidth="48"
    android:viewportHeight="48">
    <path
        android:fillColor="#4CAF50"
        android:pathData="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
</vector>'''
    
    with open(apk_dir / "res" / "drawable" / "icon.xml", "w", encoding='utf-8') as f:
        f.write(icon_content)
    
    # Copy main.py if it exists
    if Path("main.py").exists():
        shutil.copy("main.py", apk_dir / "assets" / "main.py")
        print("Copied main.py to assets")
    
    # Create MANIFEST.MF
    manifest_mf = '''Manifest-Version: 1.0
Created-By: PDF Spirit Builder

'''
    
    with open(apk_dir / "META-INF" / "MANIFEST.MF", "w", encoding='utf-8') as f:
        f.write(manifest_mf)
    
    # Create the APK zip file
    print("Creating APK file...")
    
    # Ensure bin directory exists
    bin_dir = Path("bin")
    bin_dir.mkdir(exist_ok=True)
    
    apk_path = bin_dir / "pdfspirit-simple.apk"
    
    # Create ZIP file (APK is just a ZIP with specific structure)
    with zipfile.ZipFile(apk_path, 'w', zipfile.ZIP_DEFLATED) as apk_zip:
        for root, dirs, files in os.walk(apk_dir):
            for file in files:
                file_path = Path(root) / file
                # Calculate relative path from apk_dir
                relative_path = file_path.relative_to(apk_dir)
                apk_zip.write(file_path, relative_path)
    
    # Clean up temporary directory
    shutil.rmtree(temp_dir)
    
    # Show results
    file_size = apk_path.stat().st_size
    print(f"APK created successfully: {apk_path}")
    print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    print()
    print("IMPORTANT NOTES:")
    print("- This is a basic APK structure demonstration")
    print("- It won't run as a functional app without:")
    print("  * Python runtime for Android")
    print("  * Compiled native libraries")
    print("  * Proper app signing")
    print()
    print("For a fully functional APK, use one of these methods:")
    print("1. WSL build (after restart): setup_windows.bat")
    print("2. GitHub Actions build (cloud-based)")
    print("3. Professional tools like Android Studio")
    print()
    print("This demonstrates that we CAN create APKs locally!")
    
    return apk_path

if __name__ == "__main__":
    try:
        build_simple_apk()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to continue...")
