import sys
import os
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                             QInputDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem)
from PyQt6.QtGui import QPixmap, QColor, QAction
from PyQt6.QtCore import Qt

class application_1(QMainWindow):
    def __init__(self):
        super().__init__()

        # Variables
        self.grid_size = 20
        self.products = []
        self.product_positions = {}
        self.plan_image_path = ""
        self.plan_pixmap = None
        self.project_name = ""
        self.project_author = ""
        self.project_date = ""
        self.store_name = ""
        self.store_address = ""

        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Supermarket Application")

        # Menu bar
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')
        
        new_project_action = QAction('New Project', self)
        new_project_action.triggered.connect(self.new_project)
        file_menu.addAction(new_project_action)

        open_project_action = QAction('Open Project', self)
        open_project_action.triggered.connect(self.open_project)
        file_menu.addAction(open_project_action)

        save_project_action = QAction('Save Project', self)
        save_project_action.triggered.connect(self.save_project)
        file_menu.addAction(save_project_action)

        file_menu.addSeparator()

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

    def new_project(self):
        self.project_name, _ = QInputDialog.getText(self, "Project Name", "Enter the project name:")
        self.project_author, _ = QInputDialog.getText(self, "Author Name", "Enter the author name:")
        self.project_date, _ = QInputDialog.getText(self, "Creation Date", "Enter the creation date:")
        self.store_name, _ = QInputDialog.getText(self, "Store Name", "Enter the store name:")
        self.store_address, _ = QInputDialog.getText(self, "Store Address", "Enter the store address:")
        self.load_plan()

    def load_plan(self):
        self.plan_image_path, _ = QFileDialog.getOpenFileName(self, "Select Store Plan", "", "Image Files (*.png *.jpg *.jpeg)")
        if self.plan_image_path:
            self.plan_pixmap = QPixmap(self.plan_image_path)
            self.plan_pixmap = self.plan_pixmap.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.scene.clear()
            self.pixmap_item = QGraphicsPixmapItem(self.plan_pixmap)
            self.scene.addItem(self.pixmap_item)
            self.draw_grid()

    def draw_grid(self):
        self.clear_grid()
        width = self.plan_pixmap.width()
        height = self.plan_pixmap.height()
        pen = QColor(200, 200, 200)

        for i in range(0, width, self.grid_size):
            self.scene.addLine(i, 0, i, height, pen)
        for i in range(0, height, self.grid_size):
            self.scene.addLine(0, i, width, i, pen)

    def clear_grid(self):
        for item in self.scene.items():
            if isinstance(item, QGraphicsPixmapItem):
                continue
            self.scene.removeItem(item)
    
    def open_project(self):
        pass
    
    def save_project(self):
        pass
    
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = application_1()
    window.show()
    sys.exit(app.exec())