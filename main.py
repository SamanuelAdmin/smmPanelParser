import sys
from datetime import datetime

from PySide6.QtWidgets import QApplication

from models.database_controller import Database
from views.main_view import MainWindow
from controllers.controller import Controller

from utils.logger import ConsoleOutputLogger
from utils.loggerbuffer import LoggerBuffer


def main():
	try:
		loggerBuffer = LoggerBuffer( 'LOG_' + str(datetime.now()).replace(' ', '_').replace(':', '_') + '.log')
		consoleOutputLogger = ConsoleOutputLogger(loggerBuffer)
		consoleOutputLogger.start()

		Database.connect()
		Database.cursor()
		Database.create_table()
		Database.execute('PRAGMA foreign_keys = ON;') # On support foreign keys

		app = QApplication(sys.argv)
		view = MainWindow()
		controller = Controller(view, loggerBuffer)
		view.show()

		sys.exit(app.exec())
		
		consoleOutputLogger.stop()
	except KeyboardInterrupt: pass
	finally: pass

if __name__ == "__main__":
    main()
