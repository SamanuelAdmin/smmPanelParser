from PySide6.QtWidgets import QMessageBox


class MessageBox(QMessageBox):
	def __init__(self, title, text, type_mes):
		super().__init__(type_mes, title, text)
		self.exec()