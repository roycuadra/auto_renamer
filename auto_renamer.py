import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QFileDialog, QLabel, QMessageBox, QComboBox, QLineEdit,
    QProgressBar
)
from PyQt5.QtCore import Qt

class FileRenamer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto File Renamer")
        self.setGeometry(100, 100, 420, 320)

        self.setAcceptDrops(True)

        self.label = QLabel("Select a folder to auto-rename all files.\n(Or drag & drop a folder here.)")

        self.combo = QComboBox()
        self.combo.addItems(["Numbering (1, 2, 3...)", "Alphabet (A, B, C...)"])

        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("Enter custom prefix (e.g. Image_)")

        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            "All Files (*)",
            ".jpg", ".png", ".txt", ".pdf", ".mp3"
        ])

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        self.btn_browse = QPushButton("Browse Folder and Rename")
        self.btn_browse.clicked.connect(self.browse_folder)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.combo)
        layout.addWidget(self.prefix_input)
        layout.addWidget(QLabel("Filter by file type:"))
        layout.addWidget(self.filter_combo)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.btn_browse)
        self.setLayout(layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.rename_from_path(folder)

    def rename_from_path(self, folder):
        try:
            mode = self.combo.currentIndex()
            prefix = self.prefix_input.text().strip()
            selected_ext = self.filter_combo.currentText()
            renamed, skipped = self.auto_rename_files(folder, mode, prefix, selected_ext)
            self.progress_bar.setVisible(False)

            QMessageBox.information(
                self,
                "Done ✅",
                f"Renamed {renamed} file(s).\nSkipped {skipped} file(s)."
            )
        except Exception as e:
            self.progress_bar.setVisible(False)
            QMessageBox.critical(self, "Error", str(e))

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

        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(total)

        for index, filename in enumerate(target_files):
            name, ext = os.path.splitext(filename)
            if mode == 0:
                new_base = f"{prefix}{index + 1}"
            else:
                new_base = f"{prefix}{self.index_to_letters(index)}"

            src = os.path.join(folder, filename)
            dst = os.path.join(folder, f"{new_base}{ext}")
            os.rename(src, dst)

            renamed_count += 1
            self.progress_bar.setValue(index + 1)
            QApplication.processEvents()

        return renamed_count, skipped_count

    def index_to_letters(self, index):
        letters = ""
        while True:
            index, rem = divmod(index, 26)
            letters = chr(65 + rem) + letters
            if index == 0:
                break
            index -= 1
        return letters

    # === Drag and Drop ===
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if os.path.isdir(path):
                self.rename_from_path(path)
            else:
                QMessageBox.warning(self, "Invalid Drop", "Please drop a folder, not a file.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileRenamer()
    window.show()
    sys.exit(app.exec_())
