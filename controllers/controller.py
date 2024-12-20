import os
import threading
import requests

from fileinput import filename

from urllib.parse import urlparse

from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QMessageBox, QFileDialog
from datetime import datetime

# database import
from models import database_controller
from models.api_manager.api_client import PanelApiClient, CurrencyApiClient
from models.checker.runner import CheckerRunner
# database logic
from models.database_service import DatabaseService
from models.excel_manager.check_result_saver import CheckResultSaver

# excel logic
from models.excel_manager.excel_controller import ExcelController
from models.excel_manager.saver import ServicesSpliter, ServicesSaver

# parsing logic
from models.parser.parsing_manager import ParsingManager

# saver
from models.services_saver.services_saver_manager import ServicesSaverManager

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
		self.saver = None
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
		self.view.btn_parse.clicked.connect(self.start_parse)

		self.view.btn_viewlog.clicked.connect(self.showEventLog)

		self.view.btn_export_services.clicked.connect(self.ui_save_excel)

	def showEventLog(self):
		self.logsWindow = event_log_view.LogWindow(self.loggerBuffer)
		self.logsWindow.show()

	def url_validation(self, url: str) -> bool:
		validation_url = urlparse(url)
		return all([validation_url.scheme, validation_url.netloc, validation_url.path])
	
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
		else:
			try:
				validation_url = self.url_validation(url)
				if validation_url:
					self.databaseService.add_panel(url, key)
					self.load_panel_table()  # refresh panel table
					self.new_panel_dialog.accept()
				else:
					MessageBox('Ошибка', 'Неправильный url', type_mes=QMessageBox.Icon.Critical)
			except Exception as err:
				MessageBox('Ошибка', err, type_mes=QMessageBox.Icon.Critical)


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

		if file_dialog.exec_data == QFileDialog.Accepted:
			for path in file_dialog.selectedFiles():
				try: 
					rows = ExcelController.load_excel_file(path)
				except: 
					continue

				for row in rows:
					if row[0].value and row[1].value:
						try:
							url = str(row[0].value)
							key = str(row[1].value)


							if not self.url_validation(url):
								continue

							self.databaseService.add_panel(
								url, key
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
			filename = file_dialog.selectedFiles()[0]

			self.export_excel_window.set_dir_btn.setText(filename)
			self.export_excel_window.save_btn.setEnabled(True)
			self.export_excel_window.export_path = filename

	def expot_excel(self):
		if self.export_excel_window.export_path:
			filename = self.export_excel_window.text_input.text().strip() if self.export_excel_window.text_input.text().strip() else 'export'

			# set correct file name if need it (yeah, again)
			INVALID_SYMBOLS = '\'/\\:*?"<>|.'
			filename = ''.join(list(filter(lambda x: x not in INVALID_SYMBOLS, filename))) \
				.replace('\\', '_')

			query = None # objects to save

			if self.export_excel_window.radio_btn_work.isChecked():
				query = self.databaseService.get_panels_by(work=True)
			elif self.export_excel_window.radio_btn_key_not_worked.isChecked():
				query = self.databaseService.get_panels_by(worked_keys_sites=True)
			else:
				return MessageBox('Ошибка', 'Пожалуйста, выберите как именно экспортировать',
						   type_mes=QMessageBox.Icon.Critical)

			if len(query) == 0:
				self.export_excel_window.close()

				return MessageBox('Инфо', 'Нет не рабочих сайтов или не верных ключей!',
						   type_mes=QMessageBox.Icon.Information)

			ExcelController.export_excel_file(query, self.export_excel_window.export_path, filename)

			MessageBox(
				'Успех',
				f'Успешно экспортировал в excel файл!\n"{self.export_excel_window.export_path}/{filename}.xlsx"',
				type_mes=QMessageBox.Icon.Information
			)

			self.export_excel_window.close()


	##############################################
	# ================= CHECKER ==================
	##############################################

	@panels_table_update
	def on_check_completed(self):
		self.load_panel_table()

		self.view.progress_bar.setValue(0)

		if self.checkResultSaver:
			if not self.checkResultSaver.isEmpty():
				file_dialog = choice_file_view.FileDialog(
					'Выберите дерикторию для сохранения результатов проверки',
					file_mode=QFileDialog.Directory
				)

				if file_dialog.exec_data == QFileDialog.Accepted:
					filename = f'check_result_{str(datetime.now())[:-7]}.xlsx' \
						.replace(':', '_') \
						.replace(' ', '_')

					if self.checkResultSaver.save(
						# path to file + filename
						f'{file_dialog.selectedFiles()[0]}/{filename}'
					):
						return MessageBox(title='Успех', text=f'Результаты проверки сохранены в файл {filename}', type_mes=QMessageBox.Icon.Information)

		return MessageBox(title='Успех', text='Успешно завершил проверку!', type_mes=QMessageBox.Icon.Information)


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

		self.checkResultSaver = CheckResultSaver() \
			if self.view.checkBox_saveresult_keys.isChecked() \
			else None # if you need to save a checking result


		self.checkerRunner = CheckerRunner(
			DatabaseService(database_controller.Database()),
			PanelApiClient().setSession(
				requests.Session()
			),
			checkResultSaver=self.checkResultSaver
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
			dirname = file_dialog.selectedFiles()[0]

			self.save_excel_for_parse_dialog.set_dir_btn.setText(dirname)
			self.save_excel_for_parse_dialog.start.setEnabled(True)
			self.save_excel_for_parse_dialog.export_path = dirname

	def ui_save_excel(self):
		self.save_excel_for_parse_dialog = save_excel_view.SaveExcelDialog()
		self.save_excel_for_parse_dialog.set_dir_btn.clicked.connect(self.save_file_for_parse_dialog)
		self.save_excel_for_parse_dialog.start.clicked.connect(self.save_services)
		self.save_excel_for_parse_dialog.exec()

	def start_parse(self):

		# getting all panels
		try:
			panels = self.databaseService.get_panels_by(work=True, worked_keys_sites=True)
			panels = sorted(panels, key=lambda x: x[3] and x[4])
		
			try: assert len(panels) > 0
			except AssertionError: 
				MessageBox(title='Ошибка', text='Нечего парсить, так как все панели нерабочие или с нерабочим ключом', type_mes=QMessageBox.Icon.Critical)
				return
		except Exception as err:
			MessageBox(title='Ошибка', text=f'Возникла непредвиденная ошибка при получении рабочих панелей, при запуске парсинга:\n{err}', type_mes=QMessageBox.Icon.Critical)
			return


		self.parser_panels = ParsingManager(
			panels
		) # sessions will be created at the parsing manager
		# it wont be only one - every single session for every panel

		self.parser_panels.complete.connect(self.save_services_to_database)
		self.view.progress_bar.setValue(0)
		self.view.progress_bar.setMaximum(len(panels))
		self.parser_panels.progress.connect(self.view.update_progress)
		self.view.progress_bar.setFormat("Спарсил: %p% (%v из %m)")

		self.parser_panels.start()

	@Slot(list)
	def save_services_to_database(self, services):
		self.view.progress_bar.setValue(0)
		self.view.progress_bar.setMaximum(len(services) // 1000 + 1)

		self.serviceSaverManager = ServicesSaverManager(DatabaseService(database_controller.Database()))
		self.serviceSaverManager.progress.connect(self.view.update_progress)
		self.view.progress_bar.setFormat("Добавил/Изменил: %p% (%v K из %m K)")
		self.serviceSaverManager.on_complete.connect(self.parsing_complete)
		self.serviceSaverManager.setServices(services)

		self.serviceSaverManager.start()

	def save_services(self):
		self.save_excel_for_parse_dialog.close()

		services = self.databaseService.get_services()

		try: assert len(services) > 0
		except AssertionError: 
			MessageBox(title='Ошибка', text='Нечего выгружать', type_mes=QMessageBox.Icon.Critical)
			self.parsing_complete()
			return

		services = sorted(services, key=lambda x: float(x["currency_to_usd"]))

		splitServices = ServicesSpliter().split(
			services,
			int(self.save_excel_for_parse_dialog.max_count_services.text()) \
				if self.save_excel_for_parse_dialog.max_count_services.text() else 1000
		)

		print(f'Saving {len(services)} to the {len(splitServices)} files...')

		self.saver = ServicesSaver()
		self.saver.setServices(splitServices) \
				.setSavingPath(self.save_excel_for_parse_dialog.export_path)

		self.view.progress_bar.setMaximum(len(splitServices))
		self.view.progress_bar.setFormat("Сохранил: %p% (%v из %m)")
		self.saver.on_save.connect(self.view.update_progress)
		self.saver.complete.connect(self.saver_complete)
		self.saver.start()


	def parsing_complete(self):
		print('[INFO] Парсинг завершен успешно.')
		self.view.progress_bar.setFormat("%p%")
		MessageBox(
			title='Успех', text='Успешно завершил парсинг!',
			type_mes=QMessageBox.Icon.Information
		)

		self.view.progress_bar.setValue(0)

	def saver_complete(self):
		print('[INFO] Сохранение завершено успешно.')
		self.view.progress_bar.setFormat("%p%")
		MessageBox(
			title='Успех', text='Успешно завершил сохранение!',
			type_mes=QMessageBox.Icon.Information
		)

		self.view.progress_bar.setValue(0)