from PySide6.QtCore import QSize, Qt, QCoreApplication, QMetaObject
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QPushButton, QSizePolicy


class EditPanel(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Edit panel")

        if not self.objectName():
            self.setObjectName(u"self")

        self.resize(300, 110)
        self.setMinimumSize(QSize(300, 110))
        self.setMaximumSize(QSize(300, 110))
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_2 = QLineEdit(self)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout.addWidget(self.lineEdit_2, 0, 1, 1, 1)

        self.label_2 = QLabel(self)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)

        self.edit = QPushButton(self)
        self.edit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.edit.setObjectName(u"btn_edit")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit.sizePolicy().hasHeightForWidth())

        self.gridLayout.addWidget(self.edit, 2, 0, 1, 2)

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.label.setText(QCoreApplication.translate("self", u"API URL", None))
        # self.lineEdit_2.setText("API")
        # self.lineEdit.setText("KEY")
        self.label_2.setText(QCoreApplication.translate("self", u"API KEY", None))
        self.edit.setText(QCoreApplication.translate("self", u"EDIT", None))
