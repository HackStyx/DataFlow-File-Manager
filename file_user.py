import os
import sys
import shutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QMenu, QMenuBar, QWidget, 
                             QLineEdit, QListWidget, QLabel, QMessageBox,
                             QFileDialog, QInputDialog, QVBoxLayout)
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt

class DataFlow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("DataFlow File Manager")
        self.setWindowIcon(QIcon('icon.png')) 
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.current_directory = os.getcwd()
        
        self.dir_label = QLabel(self.current_directory)
        self.dir_label.setStyleSheet("color: black;")
        
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("QListView {background: #333; color: #fff;}")
        
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Enter path")
        self.path_input.returnPressed.connect(self.open_directory)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.dir_label)
        layout.addWidget(self.path_input)
        layout.addWidget(self.list_widget)
        self.central_widget.setLayout(layout)

        # Menu actions
        self.move_action = QAction("Move", self) 
        self.move_action.triggered.connect(self.move_item)
        
        self.copy_action = QAction("Copy", self)
        self.copy_action.triggered.connect(self.copy_item)
        
        self.delete_action = QAction("Delete", self)
        self.delete_action.triggered.connect(self.delete_item)

        self.rename_action = QAction("Rename", self)
        self.rename_action.triggered.connect(self.rename_item)
        
        self.sort_action = QAction("Sort", self)
        self.sort_action.triggered.connect(self.sort_dialog)
        
        # Menu bar
        menu_bar = QMenuBar()
        menu_bar.addAction(self.move_action)
        menu_bar.addAction(self.copy_action)  
        menu_bar.addAction(self.delete_action)
        menu_bar.addAction(self.rename_action)
        menu_bar.addAction(self.sort_action)
        
        self.setMenuBar(menu_bar)
        
        self.refresh_directory()

    def refresh_directory(self):
        self.list_widget.clear()
        for item in os.listdir(self.current_directory):
            self.list_widget.addItem(item)

    def open_directory(self):
        path = self.path_input.text()
        if os.path.isdir(path):
            self.current_directory = path
            self.dir_label.setText(self.current_directory)
            self.refresh_directory()
        else:
            QMessageBox.warning(self, "Error", "Invalid directory")

    def move_item(self):
        selected = self.list_widget.selectedItems()[0]
        dest_dir = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if dest_dir:
            shutil.move(os.path.join(self.current_directory, selected.text()),
                        os.path.join(dest_dir, selected.text()))
            self.refresh_directory()

    def copy_item(self):
        selected = self.list_widget.selectedItems()[0]
        dest_dir = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if dest_dir:
            shutil.copy(os.path.join(self.current_directory, selected.text()),
                        os.path.join(dest_dir, selected.text()))
            self.refresh_directory()

    def delete_item(self):
        selected = self.list_widget.selectedItems()[0]
        reply = QMessageBox.question(self, "Confirm Deletion",  
                                     "Are you sure you want to delete this item?",
                                     QMessageBox.Yes, QMessageBox.No)
                                     
        if reply == QMessageBox.Yes:
            os.remove(os.path.join(self.current_directory, selected.text()))
            self.refresh_directory()

    def rename_item(self):
        selected = self.list_widget.selectedItems()[0]
        new_name, ok = QInputDialog.getText(self, "Rename", "New Name:")
        if ok:
            os.rename(os.path.join(self.current_directory, selected.text()),
                      os.path.join(self.current_directory, new_name))
            self.refresh_directory()
    
    def sort_dialog(self):
        items = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
        sort_type, ok = QInputDialog.getItem(self, "Sort", "Sort by:", ["Name", "Time"], 0, False)
        if ok:
            if sort_type == "Name":
                items.sort()
            elif sort_type == "Time":
                items.sort(key=lambda x: os.path.getmtime(os.path.join(self.current_directory, x)))
            self.list_widget.clear()
            self.list_widget.addItems(items)     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataFlow() 
    window.show()
    sys.exit(app.exec())
