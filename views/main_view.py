from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtGui import (QCursor,QFont, QFontDatabase)
from PySide6.QtWidgets import (QMainWindow, QFrame, QGridLayout, QGroupBox, 
							QLayout, QPushButton, QSizePolicy, QTableView, 
							QVBoxLayout, QWidget, QLabel, QLineEdit, QAbstractItemView, QRadioButton, QHeaderView, QProgressBar)


class MainWindow(QMainWindow):
	def __init__(self) -> None:
		super().__init__()
		if not self.objectName():
			self.setObjectName(u"self")
		self.resize(1200, 600)
		sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
		self.setSizePolicy(sizePolicy)

		font = QFont()
		font.setBold(True)

		self.setFont(font)
		self.centralwidget = QWidget(self)
		self.centralwidget.setObjectName(u"centralwidget")
		self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
		self.verticalLayout_4.setObjectName(u"verticalLayout_4")
		self.btn_add = QPushButton(self.centralwidget)
		self.btn_add.setObjectName(u"btn_add")
		self.btn_add.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

		self.verticalLayout_4.addWidget(self.btn_add)

		self.btn_edit = QPushButton(self.centralwidget)
		self.btn_edit.setObjectName(u"btn_edit")
		self.btn_edit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

		self.verticalLayout_4.addWidget(self.btn_edit)

		self.line = QFrame(self.centralwidget)
		self.line.setObjectName(u"line")
		self.line.setFrameShape(QFrame.Shape.HLine)
		self.line.setFrameShadow(QFrame.Shadow.Sunken)

		self.verticalLayout_4.addWidget(self.line)

		self.btn_import = QPushButton(self.centralwidget)
		self.btn_import.setObjectName(u"btn_import")
		self.btn_import.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

		self.verticalLayout_4.addWidget(self.btn_import)

		self.btn_export = QPushButton(self.centralwidget)
		self.btn_export.setObjectName(u"btn_export")
		self.btn_export.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

		self.verticalLayout_4.addWidget(self.btn_export)

		self.btn_viewlog = QPushButton(self.centralwidget)
		self.btn_viewlog.setObjectName(u"btn_viewlog")
		self.btn_viewlog.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		self.verticalLayout_4.addWidget(self.btn_viewlog)

		self.line_2 = QFrame(self.centralwidget)
		self.line_2.setObjectName(u"line_2")
		self.line_2.setFrameShape(QFrame.Shape.HLine)
		self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

		self.verticalLayout_4.addWidget(self.line_2)


		self.line_4 = QFrame(self.centralwidget)
		self.line_4.setObjectName(u"line_2")
		self.line_4.setFrameShape(QFrame.Shape.HLine)
		self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

		self.verticalLayout_4.addWidget(self.line_4)

		self.gridLayout = QGridLayout()
		self.gridLayout.setObjectName(u"gridLayout")
		self.groupBox_2 = QGroupBox(self.centralwidget)
		self.groupBox_2.setObjectName(u"groupBox_2")
		self.groupBox_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
		self.verticalLayout_5.setObjectName(u"verticalLayout_5")
		self.checkBox_delete_not_worked_sites = QRadioButton(self.groupBox_2)
		self.checkBox_delete_not_worked_sites.setObjectName(u"checkBox_delete_not_worked_sites")
		self.checkBox_delete_not_worked_sites.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

		self.verticalLayout_5.addWidget(self.checkBox_delete_not_worked_sites)

		self.checkBox_delete_all_not_worked_keys_sites = QRadioButton(self.groupBox_2)
		self.checkBox_delete_all_not_worked_keys_sites.setObjectName(u"checkBox_delete_all_not_worked_keys_sites")
		self.checkBox_delete_all_not_worked_keys_sites.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

		self.verticalLayout_5.addWidget(self.checkBox_delete_all_not_worked_keys_sites)

		self.checkBox_delete_selected_sites = QRadioButton(self.groupBox_2)
		self.checkBox_delete_selected_sites.setObjectName(u"checkBox_delete_selected_sites")
		self.checkBox_delete_selected_sites.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

		self.verticalLayout_5.addWidget(self.checkBox_delete_selected_sites)

		self.btn_delete = QPushButton(self.groupBox_2)
		self.btn_delete.setObjectName(u"btn_delete")
		self.btn_delete.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

		self.verticalLayout_5.addWidget(self.btn_delete)


		self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)

		self.groupBox = QGroupBox(self.centralwidget)
		self.groupBox.setObjectName(u"groupBox")
		self.groupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.groupBox.setFlat(False)
		self.groupBox.setCheckable(False)
		self.verticalLayout_3 = QVBoxLayout(self.groupBox)
		self.verticalLayout_3.setObjectName(u"verticalLayout_3")
		self.verticalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
		self.checkBox_check_sites = QRadioButton(self.groupBox)
		self.checkBox_check_sites.setObjectName(u"checkBox_check_sites")
		self.checkBox_check_sites.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

		self.verticalLayout_3.addWidget(self.checkBox_check_sites)

		self.checkBox_check_keys = QRadioButton(self.groupBox)
		self.checkBox_check_keys.setObjectName(u"checkBox_check_keys")
		self.checkBox_check_keys.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

		self.verticalLayout_3.addWidget(self.checkBox_check_keys)

		self.btn_check = QPushButton(self.groupBox)
		self.btn_check.setObjectName(u"btn_check")
		self.btn_check.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

		self.verticalLayout_3.addWidget(self.btn_check)

		self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

		self.verticalLayout_4.addLayout(self.gridLayout)

		self.line_3 = QFrame(self.centralwidget)
		self.line_3.setObjectName(u"line_3")
		self.line_3.setFrameShape(QFrame.Shape.HLine)
		self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

		self.verticalLayout_4.addWidget(self.line_3)

		self.tableView = QTableView(self.centralwidget)
		self.tableView.setFont(QFont(font.setBold(False)))
		self.tableView.setObjectName(u"tableView")
		self.tableView.viewport().setProperty("cursor", QCursor(Qt.CursorShape.PointingHandCursor))
		self.tableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

		self.verticalLayout_4.addWidget(self.tableView)

		self.btn_parse = QPushButton(self.centralwidget)
		self.btn_parse.setObjectName(u"btn_parse")
		self.btn_parse.setFont(QFont(font.setBold(True)))
		self.btn_parse.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		self.btn_parse.setAutoRepeat(False)
		self.btn_parse.setAutoDefault(False)
		self.btn_parse.setFlat(False)

		self.verticalLayout_4.addWidget(self.btn_parse)

		self.progress_bar = QProgressBar()
		self.verticalLayout_4.addWidget(self.progress_bar)

		self.setCentralWidget(self.centralwidget)

		self.retranslateUi()

		self.btn_parse.setDefault(False)

		QMetaObject.connectSlotsByName(self)


	def retranslateUi(self):
		self.setWindowTitle(QCoreApplication.translate("Parser", u"Parser", None))
		self.btn_add.setText(QCoreApplication.translate("self", u"\u0414\u041e\u0411\u0410\u0412\u0418\u0422\u042c", None))
		self.btn_edit.setText(QCoreApplication.translate("self", u"\u0418\u0417\u041c\u0415\u041d\u0418\u0422\u042c", None))
		self.btn_import.setText(QCoreApplication.translate("self", u"\u0417\u0410\u0413\u0420\u0423\u0417\u0418\u0422\u042c", None))
		self.btn_export.setText(QCoreApplication.translate("self", u"\u0412\u042b\u0413\u0420\u0423\u0417\u0418\u0422\u042c", None))
		self.btn_viewlog.setText("ЛОГИ")
		self.groupBox_2.setTitle(QCoreApplication.translate("self", u"\u0423\u0434\u0430\u043b\u0435\u043d\u0438\u0435", None))
		self.checkBox_delete_not_worked_sites.setText(QCoreApplication.translate("self", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0432\u0441\u0435 \u043d\u0435\u0440\u0430\u0431\u043e\u0447\u0438\u0435 \u0441\u0430\u0439\u0442\u044b", None))
		self.checkBox_delete_all_not_worked_keys_sites.setText(QCoreApplication.translate("self", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0432\u0441\u0435 \u0441\u0430\u0439\u0442\u044b \u0441 \u043d\u0435\u0440\u0430\u0431\u043e\u0447\u0438\u043c \u043a\u043b\u044e\u0447\u043e\u043c", None))
		self.checkBox_delete_selected_sites.setText(QCoreApplication.translate("self", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0442\u043e\u043b\u044c\u043a\u043e \u0432\u044b\u0434\u0435\u043b\u0435\u043d\u043d\u044b\u0435 \u0441\u0430\u0439\u0442\u044b", None))
		self.btn_delete.setText(QCoreApplication.translate("self", u"\u0423\u0414\u0410\u041b\u0418\u0422\u042c", None))
		self.groupBox.setTitle(QCoreApplication.translate("self", u"\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430", None))
		self.checkBox_check_sites.setText(QCoreApplication.translate("self", u"\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0442\u043e\u043b\u044c\u043a\u043e \u0432\u044b\u0434\u0435\u043b\u0435\u043d\u043d\u044b\u0445 \u0441\u0430\u0439\u0442\u043e\u0432", None))
		self.checkBox_check_keys.setText(QCoreApplication.translate("self", u"\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u043a\u043b\u044e\u0447\u0435\u0439 \u0442\u043e\u043b\u044c\u043a\u043e \u0432\u044b\u0434\u0435\u043b\u0435\u043d\u043d\u044b\u0445 \u0441\u0430\u0439\u0442\u043e\u0432", None))
		self.btn_check.setText(QCoreApplication.translate("self", u"\u041f\u0420\u041e\u0412\u0415\u0420\u0418\u0422\u042c", None))
		self.btn_parse.setText(QCoreApplication.translate("self", u"\u041f\u0410\u0420\u0421\u0418\u0422\u042c", None))
	# retranslateUi

	def update_progress(self):
		self.progress_bar.setValue(self.progress_bar.value() + 1)

	def view_table(self, table_model):
		self.tableView.setModel(table_model)

		self.set_table_size()

		self.tableView.resizeColumnsToContents()
		self.tableView.resizeRowsToContents()

	def set_table_size(self):
		header = self.tableView.horizontalHeader()
		header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(1, QHeaderView.Stretch)
		header.setSectionResizeMode(2, QHeaderView.Stretch)

# class Ui_DialogEditPanel(object):
# 	def setupUi(self, Dialog):
# 		if not Dialog.objectName():
# 			Dialog.setObjectName(u"Dialog")
# 		Dialog.resize(300, 110)
# 		Dialog.setMinimumSize(QSize(300, 110))
# 		Dialog.setMaximumSize(QSize(300, 110))
# 		self.gridLayout = QGridLayout(Dialog)
# 		self.gridLayout.setObjectName(u"gridLayout")
# 		self.label = QLabel(Dialog)
# 		self.label.setObjectName(u"label")
#
# 		self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
#
# 		self.lineEdit_2 = QLineEdit(Dialog)
# 		self.lineEdit_2.setObjectName(u"lineEdit_2")
#
# 		self.gridLayout.addWidget(self.lineEdit_2, 0, 1, 1, 1)
#
# 		self.label_2 = QLabel(Dialog)
# 		self.label_2.setObjectName(u"label_2")
#
# 		self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
#
# 		self.lineEdit = QLineEdit(Dialog)
# 		self.lineEdit.setObjectName(u"lineEdit")
#
# 		self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
#
# 		self.edit = QPushButton(Dialog)
# 		self.edit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
# 		self.edit.setObjectName(u"btn_edit")
# 		sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
# 		sizePolicy.setHorizontalStretch(0)
# 		sizePolicy.setVerticalStretch(0)
# 		sizePolicy.setHeightForWidth(self.edit.sizePolicy().hasHeightForWidth())
# 		# self.btn_edit.setSizePolicy(sizePolicy)
# 		# self.btn_edit.setStyleSheet(u"font-size: 11px;")
#
# 		self.gridLayout.addWidget(self.edit, 2, 0, 1, 2)
#
#
# 		self.retranslateUi(Dialog)
#
# 		QMetaObject.connectSlotsByName(Dialog)
# 	# setupUi
#
# 	def retranslateUi(self, Dialog) -> None:
# 		Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
# 		self.label.setText(QCoreApplication.translate("Dialog", u"API URL", None))
# 		self.lineEdit_2.setPlaceholderText("")
# 		self.label_2.setText(QCoreApplication.translate("Dialog", u"API KEY", None))
# 		self.edit.setText(QCoreApplication.translate("Dialog", u"EDIT", None))
# 	# retranslateUi

