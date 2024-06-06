import sys
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QComboBox, QLineEdit,
                             QPushButton, QListWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox)
from PyQt6.QtGui import QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt

class SuperMarketNavigator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SuperMarket Navigator")
        self.initUI()
        self.plan_image_path = None

    def initUI(self):
        main_layout = QHBoxLayout()

        # Left layout for store plan
        store_plan_layout = QVBoxLayout()
        store_plan_label = QLabel("Plan du magasin :")
        self.store_plan_image = QLabel()
        store_plan_layout.addWidget(store_plan_label)
        store_plan_layout.addWidget(self.store_plan_image)

        # Right layout for text and controls
        text_layout = QVBoxLayout()

        # Project Information section
        project_info_layout = QVBoxLayout()
        self.project_info_label = QLabel()
        project_info_layout.addWidget(self.project_info_label)
        text_layout.addLayout(project_info_layout)

        # Store selection section
        store_layout = QHBoxLayout()
        store_label = QLabel("Sélectionnez le magasin :")
        self.store_combobox = QComboBox()
        store_layout.addWidget(store_label)
        store_layout.addWidget(self.store_combobox)
        text_layout.addLayout(store_layout)

        # Shopping list section
        shopping_list_layout = QVBoxLayout()
        shopping_list_label = QLabel("Liste Des Produits :")
        shopping_list_layout.addWidget(shopping_list_label)
        self.shopping_list_box = QListWidget()
        shopping_list_layout.addWidget(self.shopping_list_box)
        text_layout.addLayout(shopping_list_layout)

        # Available products section
        available_products_layout = QVBoxLayout()
        available_products_label = QLabel("Produits disponibles :")
        self.product_listbox = QListWidget()
        add_selected_button = QPushButton("Ajouter les produits sélectionnés")
        add_selected_button.clicked.connect(self.add_selected_products)

        available_products_layout.addWidget(available_products_label)
        available_products_layout.addWidget(self.product_listbox)
        available_products_layout.addWidget(add_selected_button)
        text_layout.addLayout(available_products_layout)

        # Select JSON file button
        select_file_button = QPushButton("Sélectionner le fichier JSON")
        select_file_button.clicked.connect(self.select_json_file)
        text_layout.addWidget(select_file_button)

        # Navigation button
        navigate_button = QPushButton("Lancer la navigation")
        navigate_button.clicked.connect(self.show_navigation_path)
        text_layout.addWidget(navigate_button)

        main_layout.addLayout(store_plan_layout)
        main_layout.addLayout(text_layout)

        self.setLayout(main_layout)

    def select_json_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("JSON files (*.json)")
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            self.load_project_data(selected_file)

    def load_project_data(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.project_data = json.load(file)

            # Set project information
            project_info = (
                f"Project Name: {self.project_data.get('project_name', 'N/A')}\n"
                f"Author: {self.project_data.get('author', 'N/A')}\n"
                f"Date: {self.project_data.get('date', 'N/A')}\n"
                f"Store Name: {self.project_data.get('store_name', 'N/A')}\n"
                f"Store Address: {self.project_data.get('store_address', 'N/A')}\n"
            )
            self.project_info_label.setText(project_info)

            # Clear existing stores and products
            self.store_combobox.clear()
            self.product_listbox.clear()

            # Load stores
            store_name = self.project_data.get('store_name', 'N/A')
            self.store_combobox.addItem(store_name)
            self.store_combobox.setCurrentText(store_name)

            # Load products
            products = self.project_data.get('products', [])
            for product in products:
                self.product_listbox.addItem(product)

            # Load store plan image
            self.plan_image_path = self.project_data.get('plan_image_path', '')
            if self.plan_image_path:
                pixmap = QPixmap(self.plan_image_path)
                self.store_plan_image.setPixmap(pixmap)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load project data: {e}")

    def show_navigation_path(self):
        if not self.plan_image_path:
            QMessageBox.warning(self, "Erreur", "Aucun plan de magasin disponible.")
            return

        # Load the store plan image
        pixmap = QPixmap(self.plan_image_path)
        painter = QPainter(pixmap)
        pen = QPen(Qt.GlobalColor.red, 3)
        painter.setPen(pen)

        # Draw the grid
        self.draw_grid(painter, pixmap.width(), pixmap.height())

        # Convert grid coordinates to pixel coordinates
        def grid_to_pixel(x, y, width, height, num_cells):
            cell_width = width // num_cells
            cell_height = height // num_cells
            return (x * cell_width, y * cell_height)

        # Draw the path to selected products (for demonstration, using fixed coordinates)
        path_grid = [(7, 10), (8, 10), (8, 9), (9, 9)]
        path_pixels = [grid_to_pixel(x, y, pixmap.width(), pixmap.height(), 10) for x, y in path_grid]
        for i in range(len(path_pixels) - 1):
            painter.drawLine(path_pixels[i][0], path_pixels[i][1], path_pixels[i+1][0], path_pixels[i+1][1])

        painter.end()

        # Update the label with the new pixmap
        self.store_plan_image.setPixmap(pixmap)
        QMessageBox.information(self, "Navigation", "Suivez les flèches rouges sur le plan pour acheter les produits sélectionnés.")

    def draw_grid(self, painter, width, height):
        pen = QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.SolidLine)
        painter.setPen(pen)
        num_cells = 10  # Define the number of cells in the grid
        cell_width = width // num_cells
        cell_height = height // num_cells

        for i in range(num_cells + 1):
            # Draw vertical lines
            painter.drawLine(i * cell_width, 0, i * cell_width, height)
            # Draw horizontal lines
            painter.drawLine(0, i * cell_height, width, i * cell_height)

    def add_selected_products(self):
        selected_items = self.product_listbox.selectedItems()
        for item in selected_items:
            self.shopping_list_box.addItem(item.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SuperMarketNavigator()
    ex.show()
    sys.exit(app.exec())
