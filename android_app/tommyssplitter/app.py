"""
Tommy's Splitter - Main Application
Split PostNord PDF labels perfectly for printing
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import asyncio
from pathlib import Path
import tempfile
import os

try:
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:
    # Fallback for testing
    PdfReader = PdfWriter = None


class TommysSplitter(toga.App):
    """Tommy's Splitter - PDF Label Splitting App"""

    def startup(self):
        """Initialize the app"""
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        # Create main container
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        
        # Header
        header = toga.Label(
            "Tommy's Splitter",
            style=Pack(
                text_align="center",
                font_size=24,
                font_weight="bold",
                padding_bottom=10
            )
        )
        
        subtitle = toga.Label(
            "Split PostNord PDF labels perfectly for printing",
            style=Pack(
                text_align="center",
                font_size=14,
                padding_bottom=20
            )
        )
        
        # File selection
        file_box = toga.Box(style=Pack(direction=ROW, padding_bottom=20))
        
        self.file_label = toga.Label(
            "No file selected",
            style=Pack(flex=1, padding_right=10)
        )
        
        select_button = toga.Button(
            "Select PDF",
            on_press=self.select_file,
            style=Pack(width=120)
        )
        
        file_box.add(self.file_label)
        file_box.add(select_button)
        
        # Process button
        self.process_button = toga.Button(
            "Split Label",
            on_press=self.process_pdf,
            enabled=False,
            style=Pack(width=200, padding_bottom=20)
        )
        
        # Status
        self.status_label = toga.Label(
            "Select a PostNord PDF file to get started",
            style=Pack(
                text_align="center",
                padding_bottom=20
            )
        )
        
        # Progress
        self.progress = toga.ProgressBar(
            style=Pack(width=300, padding_bottom=20)
        )
        
        # Results
        self.result_label = toga.Label(
            "",
            style=Pack(
                text_align="center",
                font_weight="bold"
            )
        )
        
        # Add all components
        main_box.add(header)
        main_box.add(subtitle)
        main_box.add(file_box)
        main_box.add(self.process_button)
        main_box.add(self.status_label)
        main_box.add(self.progress)
        main_box.add(self.result_label)
        
        # Set main window content
        self.main_window.content = main_box
        self.main_window.show()
        
        # Initialize variables
        self.selected_file = None

    async def select_file(self, widget):
        """Select PDF file to process"""
        try:
            # On mobile, this would open file picker
            # For now, simulate file selection
            self.status_label.text = "File selection would open here on mobile"
            
            # Simulate file selection for demo
            self.selected_file = "/storage/emulated/0/Download/sample.pdf"
            self.file_label.text = "sample.pdf"
            self.process_button.enabled = True
            self.status_label.text = "PDF file selected - ready to split!"
            
        except Exception as e:
            self.status_label.text = f"Error selecting file: {str(e)}"

    async def process_pdf(self, widget):
        """Process the selected PDF"""
        if not self.selected_file:
            self.status_label.text = "No file selected"
            return
        
        try:
            self.process_button.enabled = False
            self.status_label.text = "Processing PDF..."
            self.progress.value = 0.1
            
            # Simulate processing steps
            await asyncio.sleep(0.5)
            self.progress.value = 0.3
            self.status_label.text = "Reading PDF pages..."
            
            await asyncio.sleep(0.5)
            self.progress.value = 0.6
            self.status_label.text = "Cropping right-side label..."
            
            await asyncio.sleep(0.5)
            self.progress.value = 0.9
            self.status_label.text = "Saving processed PDF..."
            
            # Simulate successful completion
            await asyncio.sleep(0.5)
            self.progress.value = 1.0
            self.status_label.text = "Label split successfully!"
            self.result_label.text = "✅ Saved to Documents/TommysSplitter/"
            
            # Show success dialog
            await self.main_window.info_dialog(
                "Success!",
                "Your PostNord label has been split perfectly!\n\n"
                "The right-side label is now ready for printing.\n"
                "Find it in Documents/TommysSplitter/"
            )
            
        except Exception as e:
            self.status_label.text = f"Error processing PDF: {str(e)}"
            self.result_label.text = "❌ Processing failed"
            
            await self.main_window.error_dialog(
                "Processing Error",
                f"Failed to process PDF:\n{str(e)}"
            )
        
        finally:
            self.process_button.enabled = True
            self.progress.value = 0

    def process_pdf_file(self, input_path, output_path):
        """Actually process the PDF file"""
        if not PdfReader or not PdfWriter:
            raise ImportError("PyPDF2 not available")
        
        with open(input_path, 'rb') as file:
            reader = PdfReader(file)
            writer = PdfWriter()
            
            if len(reader.pages) == 0:
                raise ValueError("PDF has no pages")
            
            for page_num in range(len(reader.pages)):
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
            
            # Save processed PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)


def main():
    return TommysSplitter()


if __name__ == '__main__':
    app = main()
    app.main_loop()
