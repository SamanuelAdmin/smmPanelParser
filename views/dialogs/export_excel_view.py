from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QVBoxLayout, QRadioButton, QPushButton, QFrame, QLineEdit, QDialog


class ExportExcelDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.resize(400, 100)
		self.setMaximumSize(400, 200)
		self.setMinimumWidth(400)
		self.setWindowTitle('Экспорт в Excel')

		self.layout = QVBoxLayout()

		self.radio_btn_work = QRadioButton()
		self.radio_btn_work.setText('Экспортировать нерабочие сайты')
		self.radio_btn_work.setChecked(True)
		self.radio_btn_work.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		self.layout.addWidget(self.radio_btn_work)

		self.radio_btn_key_not_worked = QRadioButton()
		self.radio_btn_key_not_worked.setText('Экспортировать сайты с неправильным ключом')
		self.radio_btn_key_not_worked.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		self.layout.addWidget(self.radio_btn_key_not_worked)

		self.set_dir_btn = QPushButton(text='Выбрать папку сохранения')
		self.set_dir_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		self.layout.addWidget(self.set_dir_btn)

		line1 = QFrame()
		line1.setFrameShape(QFrame.HLine)
		line1.setFrameShadow(QFrame.Sunken)
		self.layout.addWidget(line1)

		self.text_input = QLineEdit()
		self.text_input.setPlaceholderText('Введите название сохраняемого файла(без .xlsx/.csv)')
		self.layout.addWidget(self.text_input)

		self.save_btn = QPushButton(text='Экспорт')
		self.save_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		self.layout.addWidget(self.save_btn)

		self.setLayout(self.layout)
		self._connect()

	def _connect(self):
		self.text_input.textEdited.connect(lambda: self.editing_text_save_btn(self.text_input.text()))


	def editing_text_save_btn(self, text):
		text = text.strip()
		if text:
			self.save_btn.setText(f'Экспорт в {text}.xlsx')
		else:
			self.save_btn.setText(f'Экспорт')