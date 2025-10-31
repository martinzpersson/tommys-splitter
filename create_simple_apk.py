#!/usr/bin/env python3
"""
Simple APK Creator for PDF Spirit
Creates a basic APK without complex build tools
"""

import os
import sys
import zipfile
import tempfile
from pathlib import Path
import shutil

def create_simple_apk():
    """Create a simple APK structure"""
    
    print("🔧 Creating Simple PDF Spirit APK...")
    print("===================================")
    print()
    
    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp())
    apk_dir = temp_dir / "apk_structure"
    apk_dir.mkdir()
    
    print(f"📁 Working directory: {temp_dir}")
    
    # Create basic APK structure
    print("📋 Creating APK structure...")
    
    # Create directories
    (apk_dir / "META-INF").mkdir()
    (apk_dir / "assets").mkdir()
    (apk_dir / "res" / "drawable").mkdir(parents=True)
    (apk_dir / "res" / "layout").mkdir(parents=True)
    (apk_dir / "res" / "values").mkdir(parents=True)
    
    # Create AndroidManifest.xml
    manifest_content = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="org.pdfspirit"
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
    
    with open(apk_dir / "AndroidManifest.xml", "w") as f:
        f.write(manifest_content)
    
    # Create strings.xml
    strings_content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">PDF Spirit</string>
</resources>'''
    
    with open(apk_dir / "res" / "values" / "strings.xml", "w") as f:
        f.write(strings_content)
    
    # Copy main.py to assets
    if Path("main.py").exists():
        shutil.copy("main.py", apk_dir / "assets" / "main.py")
        print("✅ Copied main.py")
    
    # Create a simple icon (text-based)
    icon_content = '''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp"
    android:height="24dp"
    android:viewportWidth="24"
    android:viewportHeight="24">
    <path
        android:fillColor="#FF6200EE"
        android:pathData="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
</vector>'''
    
    with open(apk_dir / "res" / "drawable" / "icon.xml", "w") as f:
        f.write(icon_content)
    
    print("✅ Created APK structure")
    
    # Create APK zip file
    print("📦 Creating APK file...")
    apk_path = Path("bin") / "pdfspirit-simple.apk"
    apk_path.parent.mkdir(exist_ok=True)
    
    with zipfile.ZipFile(apk_path, 'w', zipfile.ZIP_DEFLATED) as apk_zip:
        for root, dirs, files in os.walk(apk_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(apk_dir)
                apk_zip.write(file_path, arc_path)
    
    print(f"✅ Created APK: {apk_path}")
    print(f"📊 APK size: {apk_path.stat().st_size} bytes")
    
    # Cleanup
    shutil.rmtree(temp_dir)
    
    print()
    print("⚠️  Note: This is a basic APK structure.")
    print("   For a fully functional app, use the WSL build method:")
    print("   1. Restart computer")
    print("   2. Run setup_windows.bat")
    print("   3. Run build_windows.bat")
    print()
    print("🎯 This simple APK demonstrates the structure,")
    print("   but won't run without proper compilation.")

if __name__ == "__main__":
    create_simple_apk()
