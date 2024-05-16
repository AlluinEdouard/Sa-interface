import sys
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QComboBox, QLineEdit,
                             QPushButton, QListWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox, QDialog)
from PyQt6.QtGui import QPixmap

class SuperMarketNavigator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SuperMarket Navigator")
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Project Information section
        project_info_layout = QVBoxLayout()
        self.project_info_label = QLabel()
        project_info_layout.addWidget(self.project_info_label)
        main_layout.addLayout(project_info_layout)

        # Store selection section
        store_layout = QHBoxLayout()
        store_label = QLabel("Sélectionnez le magasin :")
        self.store_combobox = QComboBox()
        store_layout.addWidget(store_label)
        store_layout.addWidget(self.store_combobox)
        main_layout.addLayout(store_layout)

        # Add new store section
        new_store_layout = QHBoxLayout()
        new_store_label = QLabel("Ajouter un nouveau magasin :")
        self.new_store_entry = QLineEdit()
        add_store_button = QPushButton("Ajouter le magasin")
        add_store_button.clicked.connect(self.add_new_store)

        new_store_layout.addWidget(new_store_label)
        new_store_layout.addWidget(self.new_store_entry)
        new_store_layout.addWidget(add_store_button)
        main_layout.addLayout(new_store_layout)

        # Shopping list section
        shopping_list_layout = QVBoxLayout()
        product_label = QLabel("Ajouter un produit (séparés par des virgules) :")
        self.product_entry = QLineEdit()
        add_button = QPushButton("Ajouter")
        add_button.clicked.connect(self.add_to_shopping_list)

        shopping_list_layout.addWidget(product_label)
        shopping_list_layout.addWidget(self.product_entry)
        shopping_list_layout.addWidget(add_button)

        self.shopping_list_box = QListWidget()
        shopping_list_layout.addWidget(self.shopping_list_box)
        main_layout.addLayout(shopping_list_layout)

        # Available products section
        available_products_layout = QVBoxLayout()
        available_products_label = QLabel("Produits disponibles :")
        self.product_listbox = QListWidget()
        add_selected_button = QPushButton("Ajouter les produits sélectionnés")
        add_selected_button.clicked.connect(self.add_selected_products)

        available_products_layout.addWidget(available_products_label)
        available_products_layout.addWidget(self.product_listbox)
        available_products_layout.addWidget(add_selected_button)
        main_layout.addLayout(available_products_layout)

        # Store plan section
        store_plan_layout = QVBoxLayout()
        store_plan_label = QLabel("Plan du magasin :")
        self.store_plan_image = QLabel()

        store_plan_layout.addWidget(store_plan_label)
        store_plan_layout.addWidget(self.store_plan_image)
        main_layout.addLayout(store_plan_layout)

        # Load JSON data
        self.load_project_data('stores.json')

        # Navigation button
        navigate_button = QPushButton("Lancer la navigation")
        navigate_button.clicked.connect(self.select_store)
        main_layout.addWidget(navigate_button)

        self.setLayout(main_layout)

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

            # Load stores
            store_name = self.project_data.get('store_name', 'N/A')
            self.store_combobox.addItem(store_name)
            self.store_combobox.setCurrentText(store_name)

            # Load products
            products = self.project_data.get('products', [])
            for product in products:
                self.product_listbox.addItem(product)

            # Load store plan image
            plan_image_path = self.project_data.get('plan_image_path', '')
            if plan_image_path:
                pixmap = QPixmap(plan_image_path)
                self.store_plan_image.setPixmap(pixmap)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load project data: {e}")

    def select_store(self):
        selected_store = self.store_combobox.currentText()
        QMessageBox.information(self, "Magasin sélectionné", f"Magasin sélectionné : {selected_store}")

    def add_to_shopping_list(self):
        products = self.product_entry.text()
        if products:
            product_list = [product.strip() for product in products.split(',')]
            for product in product_list:
                if product:
                    self.shopping_list_box.addItem(product)
            self.product_entry.clear()
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez saisir un produit à ajouter à la liste de courses.")

    def add_selected_products(self):
        selected_items = self.product_listbox.selectedItems()
        for item in selected_items:
            self.shopping_list_box.addItem(item.text())

    def add_new_store(self):
        new_store = self.new_store_entry.text()
        if new_store and new_store not in [self.store_combobox.itemText(i) for i in range(self.store_combobox.count())]:
            self.store_combobox.addItem(new_store)
            self.store_combobox.setCurrentText(new_store)
            self.new_store_entry.clear()
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez saisir un magasin valide qui n'est pas déjà dans la liste.")

    def load_json_data(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SuperMarketNavigator()
    ex.show()
    sys.exit(app.exec())
