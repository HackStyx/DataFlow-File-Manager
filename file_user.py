import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QMenuBar, QWidget, QLineEdit, QListWidget, QLabel, QMessageBox,QVBoxLayout
from PyQt5.QtGui import QIcon, QPalette, QColor  
from PyQt5.QtCore import Qt

class DataFlow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.set_dark_theme()
        
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle("DataFlow File Manager")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        # u can add  custom background image
#        self.central_widget.setStyleSheet("background-image: url(./images/bg.jpg);")
        self.setCentralWidget(self.central_widget)

        self.current_directory = os.getcwd()
        
        self.dir_label = QLabel(self.current_directory)
        self.dir_label.setStyleSheet("color: white;")
        
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("QListView {background: #292929; border: none; color: white;}")
        
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
        self.copy_action = QAction("Copy", self)
        self.delete_action = QAction("Delete", self)
        self.rename_action = QAction("Rename", self)
        
        self.sort_name_action = QAction("By Name", self)
        self.sort_time_action = QAction("By Time", self)
        
        # Sort menu
        self.sort_menu = QMenu("Sort", self)
        self.sort_menu.addAction(self.sort_name_action)
        self.sort_menu.addAction(self.sort_time_action)
        
        self.sort_action = QAction("Sort", self)
        self.sort_action.setMenu(self.sort_menu)

        # Menu bar
        menu_bar = QMenuBar()
        menu_bar.addAction(self.move_action)
        menu_bar.addAction(self.copy_action)
        menu_bar.addAction(self.delete_action)
        menu_bar.addAction(self.rename_action)
        menu_bar.addAction(self.sort_action) 
        self.setMenuBar(menu_bar)

        # Connections
        self.sort_name_action.triggered.connect(self.sort_by_name)
        self.sort_time_action.triggered.connect(self.sort_by_time)
        
        self.refresh_directory()
        
    # Reself.sort_action = QAction("Sort", self)  
        self.sort_action.setMenu(self.sort_menu)

        # Menu bar
        menu_bar = QMenuBar()
        menu_bar.addAction(self.move_action)
        menu_bar.addAction(self.copy_action)
        menu_bar.addAction(self.delete_action) 
        menu_bar.addAction(self.rename_action)
        menu_bar.addAction(self.sort_action)
        self.setMenuBar(menu_bar)

        # Connections
        self.sort_name_action.triggered.connect(self.sort_by_name)
        self.sort_time_action.triggered.connect(self.sort_by_time)
        
        self.refresh_directory()

    def refresh_directory(self):
        self.list_widget.clear()
        for item in os.listdir(self.current_directory):
            self.list_widget.addItem(item)

    def open_directory(self):
        path = self.path_input.text()
        if os.path.isdir(path):
            self.current_directory = path
            self.dir_label.setText("Current Directory: " + self.current_directory)
            self.refresh_directory()
        else:
            QMessageBox.warning(self, "Error", "Invalid directory")
            
    def sort_by_name(self):
        self.list_widget.sortItems(Qt.AscendingOrder)

    def sort_by_time(self):
        items = [(os.path.join(self.current_directory, i.text()), i) for i in self.list_widget.findItems('', Qt.MatchContains)]
        items.sort(key=lambda x: os.path.getmtime(x[0]))
        self.list_widget.clear()
        for item in items:
            self.list_widget.addItem(item[1])
            
    def set_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        QApplication.setPalette(dark_palette)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataFlow()
    window.show()
    sys.exit(app.exec())