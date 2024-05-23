import sys
import os
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                             QInputDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem)
from PyQt6.QtGui import QPixmap, QColor, QAction
from PyQt6.QtCore import Qt

def open_project(self):
        project_file_path, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "Project Files (*.json)")
        if not project_file_path:
            return

        with open(project_file_path, 'r') as project_file:
            project_info = json.load(project_file)

        self.project_name = project_info.get("project_name", "")
        self.project_author = project_info.get("author", "")
        self.project_date = project_info.get("date", "")
        self.store_name = project_info.get("store_name", "")
        self.store_address = project_info.get("store_address", "")
        self.grid_size = project_info.get("grid_size", 20)
        self.products = project_info.get("products", [])
        self.product_positions = project_info.get("product_positions", {})
        self.plan_image_path = project_info.get("plan_image_path", "")

        if self.plan_image_path and os.path.exists(self.plan_image_path):
            self.plan_pixmap = QPixmap(self.plan_image_path)
            self.plan_pixmap = self.plan_pixmap.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.scene.clear()
            self.pixmap_item = QGraphicsPixmapItem(self.plan_pixmap)
            self.scene.addItem(self.pixmap_item)
            self.draw_grid()

            for product, (col, row) in self.product_positions.items():
                self.scene.addText(product).setPos(col * self.grid_size, row * self.grid_size)