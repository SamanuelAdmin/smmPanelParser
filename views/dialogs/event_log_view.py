from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget

from utils.loggerbuffer import LoggerBuffer


class LogWindow(QWidget):
    def __init__(self, loggerBuffer: LoggerBuffer):
        super().__init__()
        self.resize(800, 400)
        self.setMaximumSize(800, 400)
        self.setMinimumWidth(800)
        self.setWindowTitle('Журнал')

        self.loggerBuffer = loggerBuffer

        self.layout = QVBoxLayout()
        self.layout.setObjectName(u"verticalLayout_5")
        self.listWidget = QListWidget()
        self.layout.addWidget(self.listWidget)

        self.setLayout(self.layout)
        self.loadLogs()

    def loadLogs(self):
        for logString in self.loggerBuffer.getLogsAsString().split('\n'):
            self.listWidget.addItem(logString)