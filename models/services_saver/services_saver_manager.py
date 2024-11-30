from PySide6.QtCore import QThread, Signal

from models.database_service import DatabaseService
from models.services_saver.saver import Saver



class ServicesSaverManager(QThread):
	on_complite = Signal()
	progress = Signal()

	def __init__(self, databaseServices: DatabaseService):
		super().__init__()

		self.databaseServices = databaseServices
		self.services: list[dict] = None

	def setServices(self, services: list[dict]):
		self.services = services

	def run(self):
		try:
			saver = Saver(self.databaseServices)
			for _ in saver.save(self.services):
				self.progress.emit()
		finally:
			self.on_complite.emit()