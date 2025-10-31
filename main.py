#!/usr/bin/env python3
"""
Tommy's Splitter Android App
Native Android app for GrapheneOS using Kivy
"""

import os
import sys
from pathlib import Path
import threading
import tempfile

# Kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import platform

# PDF processing
try:
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:
    # Will be handled in the app
    pass

class PDFProcessor:
    """PDF processing logic"""
    
    def __init__(self):
        self.setup_paths()
    
    def setup_paths(self):
        """Setup Android-friendly paths"""
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            from android.storage import primary_external_storage_path
            
            # Request permissions
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
            
            # Android paths
            storage_path = primary_external_storage_path()
            self.input_dir = Path(storage_path) / "Download"
            self.output_dir = Path(storage_path) / "Documents" / "PDFSpirit"
        else:
            # Desktop paths for testing
            self.input_dir = Path.home() / "Downloads"
            self.output_dir = Path.home() / "Documents" / "PDFSpirit"
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def process_pdf(self, input_path: str, callback=None) -> tuple:
        """Process PDF with progress callback"""
        try:
            input_path = Path(input_path)
            
            if callback:
                callback("Reading PDF...", 0.1)
            
            with open(input_path, 'rb') as file:
                reader = PdfReader(file)
                writer = PdfWriter()
                
                if len(reader.pages) == 0:
                    return False, "PDF has no pages"
                
                total_pages = len(reader.pages)
                
                for page_num in range(total_pages):
                    if callback:
                        progress = 0.2 + (page_num / total_pages) * 0.6
                        callback(f"Processing page {page_num + 1}/{total_pages}...", progress)
                    
                    try:
                        page = reader.pages[page_num]
                        
                        # Get page dimensions
                        mediabox = page.mediabox
                        width = float(mediabox.width)
                        height = float(mediabox.height)
                        left = float(mediabox.lower_left[0])
                        bottom = float(mediabox.lower_left[1])
                        
                        # Crop to right half
                        middle_x = left + (width / 2)
                        page.mediabox.lower_left = (middle_x, bottom)
                        page.mediabox.upper_right = (left + width, bottom + height)
                        
                        writer.add_page(page)
                        
                    except Exception as e:
                        # Fallback: copy original page
                        writer.add_page(reader.pages[page_num])
                
                if callback:
                    callback("Saving PDF...", 0.9)
                
                # Create output filename
                output_name = f"{input_path.stem}_edited.pdf"
                output_path = self.output_dir / output_name
                
                # Save processed PDF
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                
                if callback:
                    callback("Complete!", 1.0)
                
                return True, str(output_path)
                
        except Exception as e:
            return False, f"Error: {str(e)}"

class ProgressPopup(Popup):
    """Progress popup for PDF processing"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.title = "Processing PDF"
        self.size_hint = (0.8, 0.4)
        self.auto_dismiss = False
        
        # Layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Status label
        self.status_label = Label(
            text="Starting...",
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.status_label)
        
        # Progress bar
        self.progress_bar = ProgressBar(
            max=1.0,
            value=0,
            size_hint_y=None,
            height=30
        )
        layout.add_widget(self.progress_bar)
        
        # Cancel button
        self.cancel_btn = Button(
            text="Cancel",
            size_hint_y=None,
            height=50
        )
        self.cancel_btn.bind(on_press=self.dismiss)
        layout.add_widget(self.cancel_btn)
        
        self.content = layout
    
    def update_progress(self, status, progress):
        """Update progress display"""
        self.status_label.text = status
        self.progress_bar.value = progress
        
        if progress >= 1.0:
            self.cancel_btn.text = "Done"

class FileListItem(BoxLayout):
    """Custom file list item"""
    
    def __init__(self, filename, filepath, on_select_callback, **kwargs):
        super().__init__(**kwargs)
        
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 60
        self.padding = [10, 5]
        self.spacing = 10
        
        # File info
        file_size = Path(filepath).stat().st_size / (1024 * 1024)
        
        # File label
        file_label = Label(
            text=f"{filename}\n{file_size:.1f} MB",
            text_size=(None, None),
            halign='left',
            valign='center'
        )
        self.add_widget(file_label)
        
        # Process button
        process_btn = Button(
            text="Process",
            size_hint_x=None,
            width=100
        )
        process_btn.bind(on_press=lambda x: on_select_callback(filepath))
        self.add_widget(process_btn)

class TommysSplitterApp(App):
    """Main Tommy's Splitter Android App"""
    
    def build(self):
        self.title = "Tommy's Splitter"
        self.processor = PDFProcessor()
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text="📄 Tommy's Splitter\nCrop postal labels for printing",
            size_hint_y=None,
            height=80,
            font_size=20
        )
        main_layout.add_widget(header)
        
        # Buttons layout
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        
        # Scan button
        scan_btn = Button(text="🔍 Find PDFs")
        scan_btn.bind(on_press=self.scan_for_pdfs)
        button_layout.add_widget(scan_btn)
        
        # Choose file button
        choose_btn = Button(text="📁 Choose File")
        choose_btn.bind(on_press=self.choose_file)
        button_layout.add_widget(choose_btn)
        
        main_layout.add_widget(button_layout)
        
        # File list
        self.file_list_layout = BoxLayout(orientation='vertical')
        scroll = ScrollView()
        scroll.add_widget(self.file_list_layout)
        main_layout.add_widget(scroll)
        
        # Status label
        self.status_label = Label(
            text="Tap 'Scan for PDFs' to find files in Downloads",
            size_hint_y=None,
            height=40
        )
        main_layout.add_widget(self.status_label)
        
        # Initial scan
        Clock.schedule_once(lambda dt: self.scan_for_pdfs(None), 0.5)
        
        return main_layout
    
    def scan_for_pdfs(self, instance):
        """Scan for PDF files"""
        self.status_label.text = "Scanning for PDFs..."
        self.file_list_layout.clear_widgets()
        
        try:
            if not self.processor.input_dir.exists():
                self.status_label.text = f"Downloads folder not found: {self.processor.input_dir}"
                return
            
            pdf_files = list(self.processor.input_dir.glob("*.pdf"))
            pdf_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            if not pdf_files:
                self.status_label.text = "No PDF files found in Downloads"
                return
            
            self.status_label.text = f"Found {len(pdf_files)} PDF file(s)"
            
            for pdf_file in pdf_files:
                item = FileListItem(
                    pdf_file.name,
                    str(pdf_file),
                    self.process_selected_file
                )
                self.file_list_layout.add_widget(item)
                
        except Exception as e:
            self.status_label.text = f"Error scanning: {str(e)}"
    
    def choose_file(self, instance):
        """Open file chooser"""
        content = BoxLayout(orientation='vertical')
        
        # File chooser
        filechooser = FileChooserListView(
            path=str(self.processor.input_dir),
            filters=['*.pdf']
        )
        content.add_widget(filechooser)
        
        # Buttons
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        
        select_btn = Button(text="Select")
        cancel_btn = Button(text="Cancel")
        
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        # Popup
        popup = Popup(
            title="Choose PDF File",
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        def select_file(instance):
            if filechooser.selection:
                popup.dismiss()
                self.process_selected_file(filechooser.selection[0])
        
        select_btn.bind(on_press=select_file)
        cancel_btn.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def process_selected_file(self, filepath):
        """Process the selected PDF file"""
        # Show progress popup
        progress_popup = ProgressPopup()
        progress_popup.open()
        
        def update_progress(status, progress):
            Clock.schedule_once(lambda dt: progress_popup.update_progress(status, progress))
        
        def process_thread():
            success, result = self.processor.process_pdf(filepath, update_progress)
            
            def show_result(dt):
                if success:
                    self.show_success_popup(result)
                else:
                    self.show_error_popup(result)
                progress_popup.dismiss()
            
            Clock.schedule_once(show_result)
        
        # Start processing in background thread
        threading.Thread(target=process_thread, daemon=True).start()
    
    def show_success_popup(self, output_path):
        """Show success message"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        content.add_widget(Label(
            text="✅ Label split successfully!",
            size_hint_y=None,
            height=40
        ))
        
        content.add_widget(Label(
            text=f"Saved to:\n{output_path}",
            text_size=(300, None),
            halign='center'
        ))
        
        close_btn = Button(text="OK", size_hint_y=None, height=50)
        content.add_widget(close_btn)
        
        popup = Popup(
            title="Success",
            content=content,
            size_hint=(0.8, 0.6)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
        
        # Refresh file list
        self.scan_for_pdfs(None)
    
    def show_error_popup(self, error_message):
        """Show error message"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        content.add_widget(Label(
            text="❌ Splitting failed",
            size_hint_y=None,
            height=40
        ))
        
        content.add_widget(Label(
            text=error_message,
            text_size=(300, None),
            halign='center'
        ))
        
        close_btn = Button(text="OK", size_hint_y=None, height=50)
        content.add_widget(close_btn)
        
        popup = Popup(
            title="Error",
            content=content,
            size_hint=(0.8, 0.5)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

# Run the app
if __name__ == '__main__':
    TommysSplitterApp().run()
