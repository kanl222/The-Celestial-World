from PyQt5.QtWidgets import *

class MagicEditor(QWidget):
    def __init__(self):
        super().__init__()

        # Создание таблицы для отображения списка заклинаний
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['Name', 'Type', 'Cost', 'Damage', 'Cooldown', 'Range', 'Up Level Magic'])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        # создание формы для заполнения данными о новом заклинании
        self.form_layout = QFormLayout()
        self.magic_name = QLineEdit()
        self.form_layout.addRow("Name:", self.magic_name)
        self.magic_type = QLineEdit()
        self.form_layout.addRow("Type:", self.magic_type)
        self.magic_cost = QLineEdit()
        self.form_layout.addRow("Cost:", self.magic_cost)
        self.magic_damage = QLineEdit()
        self.form_layout.addRow("Damage:", self.magic_damage)
        self.magic_cooldown = QLineEdit()
        self.form_layout.addRow("Cooldown:", self.magic_cooldown)
        self.magic_range = QLineEdit()
        self.form_layout.addRow("Range:", self.magic_range)
        self.magic_up_level = QLineEdit()
        self.form_layout.addRow("Up level magic:", self.magic_up_level)

        # создание кнопок для добавления, редактирования и удаления заклинаний
        self.add_button = QPushButton("Add Magic")
        self.add_button.clicked.connect(self.add_new_magic)

        self.edit_button = QPushButton("Edit Magic")
        self.edit_button.clicked.connect(self.edit_magic)

        self.delete_button = QPushButton("Delete Magic")
        self.delete_button.clicked.connect(self.delete_magic)

        # добавление таблицы, формы и кнопок на окно
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.edit_button)
        self.layout.addWidget(self.delete_button)
        self.setLayout(self.layout)

        # список уже существующих заклинаний
        self.magic_list = {}

        # заполнение таблицы данными из списка
        self.update_table()

    def update_table(self):
        # Обновление таблицы данными из списка
        self.table.setRowCount(len(self.magic_list))
        for row, (id, magic) in enumerate(self.magic_list.items()):
            self.table.setItem(row, 0, QTableWidgetItem(magic.get('name')))
            self.table.setItem(row, 1, QTableWidgetItem(magic.get('type')))
            self.table.setItem(row, 2, QTableWidgetItem(str(magic.get('cost', ''))))
            self.table.setItem(row, 3, QTableWidgetItem(str(magic.get('damage', ''))))
            self.table.setItem(row, 4, QTableWidgetItem(str(magic.get('cooldown', ''))))
            self.table.setItem(row, 5, QTableWidgetItem(str(magic.get('rang', ''))))
            self.table.setItem(row, 6, QTableWidgetItem(str(magic.get('up_level_magic', ''))))
        self.table.resizeColumnsToContents()

    def add_new_magic(self):
        # получение значений из формы
        try:
            name = self.magic_name.text()
            magic_type = self.magic_type.text()
            cost = int(self.magic_cost.text())
            damage = int(self.magic_damage.text())
            cooldown = int(self.magic_cooldown.text())
            rang = int(self.magic_range.text())
            up_level_magic = int(self.magic_up_level.text())
        except ValueError:
            return 1

        # создание нового объекта заклинания и добавление его в список
        new_magic = {
            "name": name,
            "type": magic_type,
            "cost": cost,
            "damage": damage,
            "cooldown": cooldown,
            "rang": rang,
            "up_level_magic": up_level_magic,

    }
        self.magic_list[id(new_magic)] = new_magic
        self.update_table()

    def edit_magic(self):
        # получение выбранной строки в таблице
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return

        # получение объекта заклинания по ID
        id = list(self.magic_list)[selected_row]
        magic = self.magic_list[id]

        # заполнение формы данными из выбранного объекта заклинания
        self.magic_name.setText(magic.get('data').get('name', ''))
        self.magic_type.setText(magic.get('data').get('type', ''))
        self.magic_cost.setText(str(magic.get('data').get('cost', '')))
        self.magic_damage.setText(str(magic.get('data').get('damage', '')))
        self.magic_cooldown.setText(str(magic.get('data').get('cooldown', '')))
        self.magic_range.setText(str(magic.get('data').get('rang', '')))
        self.magic_up_level.setText(str(magic.get('data').get('up_level_magic', '')))

        # обновление объекта заклинания данными из формы
        magic['name'] = self.magic_name.text()
        magic['type'] = self.magic_type.text()
        magic['cost'] = int(self.magic_cost.text())
        magic['damage'] = int(self.magic_damage.text())
        magic['cooldown'] = int(self.magic_cooldown.text())
        magic['rang'] = int(self.magic_range.text())
        magic['up_level_magic'] = int(self.magic_up_level.text())

        self.update_table()

    def delete_magic(self):
        # получение выбранной строки в таблице
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return

        # удаление объекта заклинания по ID
        id = list(self.magic_list)[selected_row]
        self.magic_list.pop(id)

        self.update_table()



# пример использования
if __name__ == "__main__":
    app = QApplication([])
    magic_editor = MagicEditor()
    magic_editor.show()
    app.exec_()
