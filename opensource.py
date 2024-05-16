import sys
import os
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                             QInputDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem)
from PyQt6.QtGui import QPixmap, QColor, QAction
from PyQt6.QtCore import Qt

class SupermarketApp(QMainWindow):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position().toPoint()
            if self.view.rect().contains(pos):
                scene_pos = self.view.mapToScene(pos)
                col = int(scene_pos.x()) // self.grid_size
                row = int(scene_pos.y()) // self.grid_size
                product, _ = QInputDialog.getText(self, "Product", "Enter the product name:")
                if product:
                    self.products.append(product)
                    self.product_positions[product] = (col, row)
                    self.scene.addText(product).setPos(col * self.grid_size, row * self.grid_size)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SupermarketApp()
    window.show()
    sys.exit(app.exec())