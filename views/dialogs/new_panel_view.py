from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QGridLayout, QPushButton, QLabel, QLineEdit, QDialog


class NewPanel(QDialog):
	def __init__(self) -> None:
		super().__init__()

		self.setWindowTitle('Add panel')

		if not self.objectName():
			self.setObjectName(u"Dialog")

		self.resize(300, 95)
		self.setMinimumSize(QSize(300, 95))
		self.setMaximumSize(QSize(300, 95))
		self.gridLayout = QGridLayout()
		self.gridLayout.setObjectName(u"gridLayout")
		self.lineEdit_2 = QLineEdit()
		self.lineEdit_2.setObjectName(u"lineEdit_2")

		self.gridLayout.addWidget(self.lineEdit_2, 0, 1, 1, 1)

		self.lineEdit = QLineEdit()
		self.lineEdit.setObjectName(u"lineEdit")

		self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)

		self.label = QLabel()
		self.label.setObjectName(u"label") 

		self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

		self.label_2 = QLabel()
		self.label_2.setObjectName(u"label_2")

		self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

		self.add = QPushButton()
		self.add.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		self.add.setObjectName(u"btn_add")

		self.gridLayout.addWidget(self.add, 2, 0, 1, 2)
		
		self.setLayout(self.gridLayout)

		self.retranslateUi()

		# QMetaObject.connectSlotsByName(QDialog)

	def retranslateUi(self) -> None:
		self.label.setText(QCoreApplication.translate("Dialog", u"API URL", None))
		self.label_2.setText(QCoreApplication.translate("Dialog", u"API KEY", None))
		self.add.setText(QCoreApplication.translate("Dialog", u"ADD", None))