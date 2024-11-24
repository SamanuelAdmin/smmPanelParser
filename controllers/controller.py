import threading

import requests
from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QMessageBox, QFileDialog

# database import
from models import database_controller
from models.api_manager.api_client import PanelApiClient, CurrencyApiClient
from models.checker.runner import CheckerRunner
# database logic
from models.database_service import DatabaseService

# excel logic
from models.excel_manager.excel_controller import ExcelController
from models.excel_manager.saver import ServicesSpliter, ServicesSaver

# parsing logic
from models.parser.parsing_manager import ParsingManager

# import all exceptions
from utils.exceptions.database_exceptions import *
from utils.loggerbuffer import LoggerBuffer

# import all views
from views.main_view import MainWindow
from views.elements.message_box import MessageBox
from views.elements import panels_table
from views.dialogs import (
	new_panel_view,
	edit_panel_view,
	event_log_view,
	choice_file_view,
	save_excel_view,
	export_excel_view,
)


class Controller(QObject):
	def __init__(self, view: MainWindow, loggerBuffer: LoggerBuffer) -> None:
		super().__init__()
		self.loggerBuffer = loggerBuffer

		self.view = view
		self.databaseService = DatabaseService(
			database_controller.Database()
		)

		self.connect()
		self.load_panel_table()

	def panels_table_update(function):
		def wrapper(self, *args, **kwargs):
			function(self, *args, **kwargs)
			self.view.set_table_size()

		return wrapper

	def load_panel_table(self) -> None:
		panel_list = self.databaseService.get_panels()
		table_model = panels_table.generatePanelsTable(panel_list)  # generate panel table

		self.view.view_table(table_model)

	def connect(self) -> None:
		self.view.btn_add.clicked.connect(self.open_dialog_new_panel)
		self.view.btn_edit.clicked.connect(self.open_dialog_edit_panel)
		self.view.btn_delete.clicked.connect(self.delete_panels)
		self.view.btn_import.clicked.connect(self.import_excel_to_panels)
		self.view.btn_export.clicked.connect(self.open_export_excel_dialog)
		self.view.btn_check.clicked.connect(self.check_panels)
		self.view.btn_parse.clicked.connect(self.ui_save_excel)

		self.view.btn_viewlog.clicked.connect(self.showEventLog)

	# ================== ADD PANEL ==================
	def showEventLog(self):
		self.logsWindow = event_log_view.LogWindow(self.loggerBuffer)
		self.logsWindow.show()

	# ================== ADD PANEL ==================
	def open_dialog_new_panel(self) -> None:
		self.new_panel_dialog = new_panel_view.NewPanel()
		self.new_panel_dialog.add.clicked.connect(self.add_panel)
		self.new_panel_dialog.exec()

	@panels_table_update
	def add_panel(self) -> None:
		url = self.new_panel_dialog.lineEdit_2.text()
		key = self.new_panel_dialog.lineEdit.text()
		if not url or not key:
			MessageBox('Ошибка', 'Пожалуйста, заполните все поля', type_mes=QMessageBox.Icon.Critical)
		elif not 'https://' in url:
			MessageBox('Ошибка', 'Введенный url неправильный, нехвататет протокола https://', type_mes=QMessageBox.Icon.Critical)
		else:
			self.databaseService.add_panel(url, key)
			self.load_panel_table()  # refresh panel table
			self.new_panel_dialog.accept()


	# ================== EDIT PANEL ==================
	def open_dialog_edit_panel(self) -> None:
		selected_row = self.view.tableView.selectionModel().selectedRows(column=0) # забираем id записи

		if len(selected_row) == 1:
			self.edit_panel_dialog = edit_panel_view.EditPanel()

			panel_id, url, key, is_work, is_work_key = self.databaseService.get_panels_by(panel_id=selected_row[0].data())

			self.edit_panel_dialog.lineEdit_2.setText(url)  # API url to change
			self.edit_panel_dialog.lineEdit.setText(key)   # API key to change

			self.edit_panel_dialog.edit.clicked.connect(lambda: self.edit_panel(selected_row))
			return self.edit_panel_dialog.exec()

		MessageBox('Ошибка', 'Пожалуйста, выберите ОДНУ запись, которую хотите редактировать',
				   type_mes=QMessageBox.Icon.Critical)


	@panels_table_update
	def edit_panel(self, selected_row) -> None:
		id = selected_row[0].data()
		url = self.edit_panel_dialog.lineEdit_2.text()
		key = self.edit_panel_dialog.lineEdit.text()

		if not url or not key:
			MessageBox('Ошибка', 'Пожалуйста, заполните все поля', type_mes=QMessageBox.Icon.Critical)
		else:
			try:
				self.databaseService.edit_panel(id, url, key)
				self.load_panel_table()
				self.edit_panel_dialog.accept() # close da window

				MessageBox('Успех', 'Успешно изменено', type_mes=QMessageBox.Icon.Information)
			except UniqueError as error:
				MessageBox('Ошибка', error, type_mes=QMessageBox.Icon.Critical)


	# ================== DELETE PANEL ==================
	def deleteByQuery(self, query) -> None:
		for row in query:
			self.databaseService.delete_panel(int(row[0]))

	@panels_table_update
	def delete_panels(self):
		if self.view.checkBox_delete_selected_sites.isChecked(): # delete_selected_sites
			selected_rows = self.view.tableView.selectionModel().selectedRows(column=0)

			for row in selected_rows:
				self.databaseService.delete_panel(int(row.data()))

		elif self.view.checkBox_delete_all_not_worked_keys_sites.isChecked(): # delete_all_not_worked_keys_sites
			query = self.databaseService.get_panels_by(worked_keys_sites=True)
			self.deleteByQuery(query)

		elif self.view.checkBox_delete_not_worked_sites.isChecked():  # delete_not_worked_sites
			query = self.databaseService.get_panels_by(work=True)
			self.deleteByQuery(query)

		self.load_panel_table()


	##############################################
	# ================== LOADER ==================
	##############################################

	@panels_table_update
	def import_excel_to_panels(self):
		file_dialog = choice_file_view.FileDialog(
			'Выберите excel файл(-ы), который вы хотите импортировать',
			file_types = ['*.xlsx, *.XLSX', '*.csv, *.CSV']
		)

		if file_dialog.exec() == QFileDialog.Accepted:
			for path in file_dialog.selectedFiles():
				try: 
					rows = ExcelController.load_excel_file(path)
				except: 
					continue

				for row in rows:
					if row[0].value and row[1].value:
						try:
							self.databaseService.add_panel(
								str(row[0].value), str(row[1].value)
							)
						except UniqueError as error: continue # will not save is value is already exist

				# SUS !!!!! DONT TOUCH IT!!!!
				# self.db.db_connect.commit() # save to database

			MessageBox('Успех', 'Успешно импортировал excel файл в бд!', type_mes=QMessageBox.Icon.Information)

		self.load_panel_table()


	#  EXPORT PANELS TO EXCEL
	def open_export_excel_dialog(self):
		self.export_excel_window = export_excel_view.ExportExcelDialog()
		self.export_excel_window.set_dir_btn.clicked.connect(self.export_file_dialog)
		self.export_excel_window.save_btn.clicked.connect(self.expot_excel)
		self.export_excel_window.save_btn.setEnabled(False)
		self.export_excel_window.exec()

	def export_file_dialog(self):
		file_dialog = choice_file_view.FileDialog(
			'Выберите дерикторию для сохранения', file_mode=QFileDialog.Directory
		)

		if file_dialog.exec_data == QFileDialog.Accepted:
			self.export_excel_window.set_dir_btn.setText(file_dialog.selectedFiles()[0])
			self.export_excel_window.save_btn.setEnabled(True)
			self.export_excel_window.export_path = file_dialog.selectedFiles()[0]

	def expot_excel(self):
		if self.export_excel_window.export_path:
			filename = self.export_excel_window.text_input.text().strip() if self.export_excel_window.text_input.text().strip() else 'export'

			if self.export_excel_window.radio_btn_work.isChecked():
				query = self.databaseService.get_panels_by(work=True)
				ExcelController.export_excel_file(query, self.export_excel_window.export_path, filename)

				MessageBox(
					'Успех',
					f'Успешно экспортировал в excel файл!\n"{self.export_excel_window.export_path}/{filename}.xlsx"',
					type_mes=QMessageBox.Icon.Information
				)

			elif self.export_excel_window.radio_btn_key_not_worked.isChecked():
				query = self.databaseService.get_panels_by(worked_keys_sites=True)
				ExcelController.export_excel_file(query, self.export_excel_window.export_path, filename)

				MessageBox(
					'Успех',
					f'Успешно экспортировал в excel файл!\n{self.export_excel_window.export_path}/{filename}.xlsx',
						type_mes=QMessageBox.Icon.Information
				)
			else:
				MessageBox('Ошибка', 'Пожалуйста, выберите как именно экспортировать',
						   type_mes=QMessageBox.Icon.Critical)
				return

			self.export_excel_window.close()


	##############################################
	# ================= CHECKER ==================
	##############################################

	@panels_table_update
	def on_check_completed(self):
		self.load_panel_table()
		MessageBox(title='Успех', text='Успешно завершил проверку!', type_mes=QMessageBox.Icon.Information)
		self.view.progress_bar.setValue(0)

	def check_panels(self):
		selected_rows = self.view.tableView.selectionModel().selectedRows(column=0)  # забираем id записей
		if len(selected_rows) < 1:
			return MessageBox(
				'Ошибка', 'Пожалуйста выделите записи из таблицы, которые вы хотите проверить',
					type_mes=QMessageBox.Icon.Critical
			)

		panels = [
			self.databaseService.get_panels_by(
					panel_id=int(panel_id.data())
				) for panel_id in selected_rows
		] # getting all panels from database via those id`s

		self.checkerRunner = CheckerRunner(
			DatabaseService(database_controller.Database()),
			PanelApiClient().setSession(
				requests.Session()
			)
		)

		if self.view.checkBox_check_keys.isChecked():
			self.checkerRunner.mode_func = 'key'
		elif self.view.checkBox_check_sites.isChecked():
			self.checkerRunner.mode_func = 'work'

		self.checkerRunner.panels = panels
		self.checkerRunner.start()

		self.checkerRunner.сompletion.connect(self.on_check_completed)

		self.view.progress_bar.setValue(0)
		self.view.progress_bar.setMaximum(len(panels))
		self.checkerRunner.progress.connect(self.view.update_progress)


	##############################################
	# ================= PARSER ===================
	##############################################

	def save_file_for_parse_dialog(self):
		file_dialog = choice_file_view.FileDialog('Выберите дерикторию для сохранения', file_mode=QFileDialog.Directory)

		if file_dialog.exec_data == QFileDialog.Accepted:
			self.save_excel_for_parse_dialog.set_dir_btn.setText(file_dialog.selectedFiles()[0])
			self.save_excel_for_parse_dialog.start.setEnabled(True)
			self.save_excel_for_parse_dialog.export_path = file_dialog.selectedFiles()[0]

	def ui_save_excel(self):
		self.save_excel_for_parse_dialog = save_excel_view.SaveExcelDialog()
		self.save_excel_for_parse_dialog.set_dir_btn.clicked.connect(self.save_file_for_parse_dialog)
		self.save_excel_for_parse_dialog.start.clicked.connect(self.start_parse)
		self.save_excel_for_parse_dialog.exec()

	def start_parse(self):
		self.save_excel_for_parse_dialog.close()

		# getting all panels
		panels = self.databaseService.get_panels(filterFunc=lambda panel: panel[3]) # choice only working
		try: assert len(panels) > 0
		except AssertionError: 
			MessageBox(title='Ошибка', text='Нечего парсить, так как все панели нерабочие или с нерабочим ключом', type_mes=QMessageBox.Icon.Critical)
			return

		self.parser_panels = ParsingManager(
			panels,
			PanelApiClient().setSession( requests.Session() ),
			CurrencyApiClient( requests.Session() ),
			DatabaseService(database_controller.Database())
		)

		self.parser_panels.complete.connect(self.save_services)
		self.view.progress_bar.setValue(0)
		self.view.progress_bar.setMaximum(len(panels) * 2)
		self.parser_panels.progress.connect(self.view.update_progress)

		self.parser_panels.start()

	@Slot(list)
	def save_services(self, services):
		self.view.progress_bar.setValue(0) # clear progress bar

		try: assert len(services) > 0
		except AssertionError: 
			MessageBox(title='Ошибка', text='Нечего сохранять', type_mes=QMessageBox.Icon.Critical)
			self.parsing_complete()
			return

		services = sorted(services, key=lambda x: float(x["currency_to_usd"]))

		splitedServices = ServicesSpliter().split(services, 1000)

		saver = ServicesSaver() \
				.setServices(splitedServices) \
				.setSavingPath(self.save_excel_for_parse_dialog.export_path)

		saver.on_save.connect(self.view.update_progress)
		self.view.progress_bar.setMaximum(len(splitedServices))
		saver.complete.connect(self.parsing_complete)
		saver.start()

		# fixing the "QThread error" (when thread already has been closed after saver start). This line allow to new thread work
		threading.Thread(target=saver.wait).start()

	def parsing_complete(self):
		print('[INFO] Парсинг завершен успешно.')

		MessageBox(
			title='Успех', text='Успешно завершил парсинг!',
			type_mes=QMessageBox.Icon.Information
		)

		self.view.progress_bar.setValue(0)