import sys
import sqlite3
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView


class StoreApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Loja")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.init_database()
        self.create_table()
        self.load_data()

        self.create_widgets()
        self.update_table()

    def init_database(self):
        self.conn = sqlite3.connect('store.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                price REAL,
                                quantity INTEGER,
                                promo_price REAL)''')
        self.conn.commit()

    def create_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Preço", "Quantidade", "Preço Promocional"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.layout.addWidget(self.table)

    def load_data(self):
        self.cursor.execute("SELECT * FROM products")
        products = self.cursor.fetchall()
        for product in products:
            self.add_row_to_table(product)

    def create_widgets(self):
        self.name_input = QLineEdit()
        self.price_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.promo_price_input = QLineEdit()

        self.add_button = QPushButton("Adicionar Produto")
        self.add_button.clicked.connect(self.add_product)

        self.layout.addWidget(QLabel("Nome do Produto:"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel("Preço:"))
        self.layout.addWidget(self.price_input)
        self.layout.addWidget(QLabel("Quantidade:"))
        self.layout.addWidget(self.quantity_input)
        self.layout.addWidget(QLabel("Preço Promocional (Opcional):"))
        self.layout.addWidget(self.promo_price_input)
        self.layout.addWidget(self.add_button)

    def add_product(self):
        name = self.name_input.text().strip()
        price = float(self.price_input.text())
        quantity = int(self.quantity_input.text())
        promo_price = float(self.promo_price_input.text()) if self.promo_price_input.text() else None

        self.cursor.execute("INSERT INTO products (name, price, quantity, promo_price) VALUES (?, ?, ?, ?)",
                            (name, price, quantity, promo_price))
        self.conn.commit()

        self.add_row_to_table((self.cursor.lastrowid, name, price, quantity, promo_price))
        self.clear_input_fields()

    def add_row_to_table(self, data):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        for i, item in enumerate(data):
            self.table.setItem(row_position, i, QTableWidgetItem(str(item)))

    def clear_input_fields(self):
        self.name_input.clear()
        self.price_input.clear()
        self.quantity_input.clear()
        self.promo_price_input.clear()

    def update_table(self):
        self.table.setRowCount(0)
        self.load_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StoreApp()
    window.show()
    sys.exit(app.exec_())
