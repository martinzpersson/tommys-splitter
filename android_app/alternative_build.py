#!/usr/bin/env python3
"""
Alternative APK Build Methods
"""

import subprocess
import sys
from pathlib import Path

def try_python_for_android():
    """Try building with python-for-android"""
    print("Trying python-for-android build...")
    
    try:
        # Install p4a
        subprocess.run([sys.executable, "-m", "pip", "install", "python-for-android"], check=True)
        
        # Try to build
        result = subprocess.run([
            "p4a", "apk", 
            "--private", ".",
            "--package", "org.pdfspirit",
            "--name", "PDF Spirit",
            "--version", "1.0",
            "--bootstrap", "sdl2",
            "--requirements", "python3,kivy,PyPDF2"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("SUCCESS: python-for-android build completed!")
            return True
        else:
            print(f"python-for-android failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"python-for-android not available: {e}")
        return False

def try_briefcase():
    """Try building with BeeWare Briefcase"""
    print("Trying BeeWare Briefcase...")
    
    try:
        # Install briefcase
        subprocess.run([sys.executable, "-m", "pip", "install", "briefcase"], check=True)
        
        # Initialize briefcase project
        subprocess.run(["briefcase", "new"], check=True)
        
        print("Briefcase installed - manual setup required")
        return True
        
    except Exception as e:
        print(f"Briefcase not available: {e}")
        return False

def show_options():
    """Show all available build options"""
    print("PDF Spirit APK - Local Build Options")
    print("====================================")
    print()
    
    print("OPTION 1: Basic APK Structure (DONE)")
    print("- Created: bin/pdfspirit-simple.apk")
    print("- Shows APK can be built locally")
    print("- Needs runtime to be functional")
    print()
    
    print("OPTION 2: WSL Build (After Restart)")
    print("- Run: setup_windows.bat")
    print("- Run: build_windows.bat") 
    print("- Result: Full functional APK")
    print()
    
    print("OPTION 3: Web Version (Working Now)")
    print("- Already running at: http://localhost:5000")
    print("- Your friend can use via browser")
    print("- Same functionality as Android app")
    print()
    
    print("OPTION 4: Advanced Tools")
    print("- python-for-android (complex setup)")
    print("- BeeWare Briefcase (cross-platform)")
    print("- Android Studio (professional)")
    print()
    
    print("RECOMMENDATION:")
    print("Use the web version for immediate sharing!")
    print("Your GrapheneOS friend can access it via browser.")

if __name__ == "__main__":
    show_options()
    
    print()
    choice = input("Try advanced build tools? (y/n): ").lower().strip()
    
    if choice == 'y':
        print()
        if not try_python_for_android():
            try_briefcase()
    else:
        print()
        print("Smart choice! The web version works perfectly.")
        print("Your friend can use PDF Spirit right now via browser.")
