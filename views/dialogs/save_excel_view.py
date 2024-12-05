from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton


class SaveExcelDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.resize(400, 100)
		self.setMaximumSize(400, 200)
		self.setMinimumWidth(400)
		self.setWindowTitle('Сохранение в Excel')

		self.layout = QVBoxLayout()

		self.layout.addWidget(QLabel(text='Макс. количество сервисов в одном excel файле'))

		self.max_count_services = QLineEdit()
		self.max_count_services.setPlaceholderText('Необязательно, по умолчанию 1000')
		self.layout.addWidget(self.max_count_services)

		self.set_dir_btn = QPushButton(text='Выбрать папку, куда сохранять результат')
		self.set_dir_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		self.layout.addWidget(self.set_dir_btn)

		self.start = QPushButton(text='Начать сохранять в Excel')
		self.start.setEnabled(False)
		self.start.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		self.layout.addWidget(self.start)

		self.setLayout(self.layout)