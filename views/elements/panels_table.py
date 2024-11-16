from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QColor, QStandardItem


def generatePanelsTable(panels: list):
    table_model = QStandardItemModel()
    table_model.setHorizontalHeaderLabels(['id', 'url', 'api key'])

    num_row = 0
    for row in panels:  # Ходим по строкам(устанавливаем текущую строку и получаем bool)
        col_num = 0
        for col in range(3):
            if col_num == 1:
                value = bool(row[3])
                if value:
                    bg_color = QColor(Qt.green)
                else:
                    bg_color = QColor(Qt.red)
                fg_color = QColor(Qt.black)
                value = row[col]
            elif col_num == 2:
                value = bool(row[4])
                if value:
                    bg_color = QColor(Qt.green)
                else:
                    bg_color = QColor(Qt.red)
                fg_color = QColor(Qt.black)
                value = row[col]
            else:
                value = str(row[col])
                bg_color = QColor(Qt.gray)
                fg_color = QColor(Qt.white)

            item = QStandardItem(value)
            item.setBackground(bg_color)
            item.setForeground(fg_color)
            table_model.setItem(num_row, col, item)
            col_num += 1
        num_row += 1

    return table_model