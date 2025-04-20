import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QLabel, QMessageBox, QComboBox, QLineEdit,
    QProgressBar, QFrame, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette

class ModernFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setStyleSheet("""
            ModernFrame {
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)

class FileRenamer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Renamer")
        self.setGeometry(100, 100, 550, 500)
        self.setAcceptDrops(True)
        
        # Set application style
        self.set_application_style()
        
        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        header_label = QLabel("File Renamer")
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Description
        description = QLabel("Batch rename files with customizable options")
        description.setStyleSheet("font-size: 14px; color: #7f8c8d; margin-bottom: 10px;")
        description.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(description)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #e0e0e0;")
        main_layout.addWidget(separator)
        
        # Drop area
        self.drop_frame = ModernFrame()
        drop_layout = QVBoxLayout(self.drop_frame)
        drop_layout.setAlignment(Qt.AlignCenter)
        
        self.drop_icon = QLabel("📁")
        self.drop_icon.setStyleSheet("font-size: 48px; color: #3498db;")
        self.drop_icon.setAlignment(Qt.AlignCenter)
        
        self.drop_label = QLabel("Drag & drop a folder here\nor use the browse button below")
        self.drop_label.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        self.drop_label.setAlignment(Qt.AlignCenter)
        
        drop_layout.addWidget(self.drop_icon)
        drop_layout.addWidget(self.drop_label)
        main_layout.addWidget(self.drop_frame)
        
        # Options frame
        options_frame = ModernFrame()
        options_layout = QVBoxLayout(options_frame)
        options_layout.setSpacing(15)
        
        # Rename scheme
        scheme_label = QLabel("Renaming Scheme:")
        scheme_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        
        self.combo = QComboBox()
        self.combo.addItems(["Numbering (1, 2, 3...)", "Alphabet (A, B, C...)"])
        self.combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QComboBox::drop-down {
                border: 0px;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #bdc3c7;
                selection-background-color: #3498db;
            }
        """)
        
        # Prefix input
        prefix_label = QLabel("Custom Prefix:")
        prefix_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        
        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("Enter prefix (e.g. Image_)")
        self.prefix_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """)
        
        # File filter
        filter_label = QLabel("Filter by File Type:")
        filter_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            "All Files (*)",
            ".jpg", ".png", ".pdf", ".txt", ".mp3", ".mp4", ".docx", ".xlsx"
        ])
        self.filter_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QComboBox::drop-down {
                border: 0px;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #bdc3c7;
                selection-background-color: #3498db;
            }
        """)
        
        # Add options to layout
        options_layout.addWidget(scheme_label)
        options_layout.addWidget(self.combo)
        options_layout.addWidget(prefix_label)
        options_layout.addWidget(self.prefix_input)
        options_layout.addWidget(filter_label)
        options_layout.addWidget(self.filter_combo)
        
        main_layout.addWidget(options_frame)
        
        # Progress area
        progress_frame = ModernFrame()
        progress_layout = QVBoxLayout(progress_frame)
        
        progress_label = QLabel("Progress:")
        progress_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #2ecc71;
                border-radius: 4px;
            }
        """)
        self.progress_bar.setVisible(False)
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setVisible(False)
        
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.status_label)
        
        main_layout.addWidget(progress_frame)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.btn_browse = QPushButton("Browse Folder")
        self.btn_browse.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
        """)
        self.btn_browse.setMinimumHeight(40)
        self.btn_browse.setCursor(Qt.PointingHandCursor)
        self.btn_browse.clicked.connect(self.browse_folder)
        
        self.btn_rename = QPushButton("Start Renaming")
        self.btn_rename.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #219653;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.btn_rename.setMinimumHeight(40)
        self.btn_rename.setCursor(Qt.PointingHandCursor)
        self.btn_rename.setEnabled(False)
        self.btn_rename.clicked.connect(self.start_rename)
        
        button_layout.addWidget(self.btn_browse)
        button_layout.addWidget(self.btn_rename)
        
        main_layout.addLayout(button_layout)
        
        # Footer
        footer = QLabel("© 2025 File Renamer")
        footer.setStyleSheet("color: #95a5a6; font-size: 11px;")
        footer.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer)
        
        self.setLayout(main_layout)
        
        # Current folder path
        self.current_folder = None

    def set_application_style(self):
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 12px;
                background-color: #f5f8fa;
            }
            QToolTip {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 5px;
            }
        """)
        
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.current_folder = folder
            self.drop_icon.setText("✅")
            self.drop_label.setText(f"Selected: {os.path.basename(folder)}")
            self.btn_rename.setEnabled(True)
    
    def start_rename(self):
        if self.current_folder:
            self.rename_from_path(self.current_folder)
    
    def rename_from_path(self, folder):
        try:
            self.progress_bar.setVisible(True)
            self.status_label.setVisible(True)
            self.status_label.setText("Preparing files...")
            self.btn_rename.setEnabled(False)
            self.btn_browse.setEnabled(False)
            QApplication.processEvents()
            
            mode = self.combo.currentIndex()
            prefix = self.prefix_input.text().strip()
            selected_ext = self.filter_combo.currentText()
            
            renamed, skipped = self.auto_rename_files(folder, mode, prefix, selected_ext)
            
            self.status_label.setText("Complete!")
            self.btn_rename.setEnabled(True)
            self.btn_browse.setEnabled(True)
            
            QMessageBox.information(
                self,
                "Operation Complete",
                f"<h3>Renaming Complete</h3>"
                f"<p><b>✅ Successfully renamed:</b> {renamed} file(s)</p>"
                f"<p><b>⏭️ Skipped:</b> {skipped} file(s)</p>",
                QMessageBox.Ok
            )
            
        except Exception as e:
            self.progress_bar.setVisible(False)
            self.status_label.setVisible(False)
            self.btn_rename.setEnabled(True)
            self.btn_browse.setEnabled(True)
            
            QMessageBox.critical(
                self, 
                "Error",
                f"<h3>An error occurred</h3><p>{str(e)}</p>"
            )

    def auto_rename_files(self, folder, mode, prefix, filter_ext):
        all_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        all_files.sort()

        if filter_ext != "All Files (*)":
            target_files = [f for f in all_files if f.lower().endswith(filter_ext)]
        else:
            target_files = all_files

        renamed_count = 0
        skipped_count = len(all_files) - len(target_files)

        total = len(target_files)
        if total == 0:
            return 0, skipped_count

        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(0)

        # Create a temporary mapping of old to new filenames to avoid conflicts
        rename_map = {}
        
        for index, filename in enumerate(target_files):
            name, ext = os.path.splitext(filename)
            if mode == 0:  # Numbering
                new_base = f"{prefix}{index + 1:03d}"  # Zero-padded for better sorting
            else:  # Alphabet
                new_base = f"{prefix}{self.index_to_letters(index)}"

            src = os.path.join(folder, filename)
            dst = os.path.join(folder, f"{new_base}{ext}")
            
            # Check if destination already exists and adjust
            counter = 1
            final_dst = dst
            while os.path.exists(final_dst) and final_dst != src:
                if mode == 0:
                    final_dst = os.path.join(folder, f"{new_base}_{counter}{ext}")
                else:
                    final_dst = os.path.join(folder, f"{new_base}_{counter}{ext}")
                counter += 1
                
            rename_map[src] = final_dst
            
            self.status_label.setText(f"Processing: {filename}")
            self.progress_bar.setValue(index + 1)
            QApplication.processEvents()
        
        # Perform the actual renaming
        for index, (src, dst) in enumerate(rename_map.items()):
            os.rename(src, dst)
            renamed_count += 1
            self.progress_bar.setValue(index + 1)
            QApplication.processEvents()

        return renamed_count, skipped_count

    def index_to_letters(self, index):
        letters = ""
        index += 1  # Start from 1 for A
        while True:
            index, rem = divmod(index - 1, 26)
            letters = chr(65 + rem) + letters
            if index == 0:
                break
        return letters

    # === Drag and Drop ===
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            self.drop_frame.setStyleSheet("""
                ModernFrame {
                    background-color: #e3f2fd;
                    border-radius: 8px;
                    border: 2px dashed #3498db;
                }
            """)
            event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self.drop_frame.setStyleSheet("""
            ModernFrame {
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        
    def dropEvent(self, event):
        self.drop_frame.setStyleSheet("""
            ModernFrame {
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if os.path.isdir(path):
                self.current_folder = path
                self.drop_icon.setText("✅")
                self.drop_label.setText(f"Selected: {os.path.basename(path)}")
                self.btn_rename.setEnabled(True)
            else:
                QMessageBox.warning(
                    self, 
                    "Invalid Drop", 
                    "<h3>Please select a folder</h3>"
                    "<p>The item you dropped is not a folder. Please drop a folder to continue.</p>"
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Use Fusion style for better cross-platform appearance
    window = FileRenamer()
    window.show()
    sys.exit(app.exec_())