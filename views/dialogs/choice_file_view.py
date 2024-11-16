from PySide6.QtWidgets import QFileDialog


class FileDialog(QFileDialog):
	def __init__(self, window_title: str, file_types: list=[], file_mode=QFileDialog.ExistingFiles):
		super().__init__()
		self.setWindowTitle(window_title)
		self.setFileMode(file_mode)

		if len(file_types) > 0:
			self.setNameFilters(file_types)

		self.exec_data = self.exec()