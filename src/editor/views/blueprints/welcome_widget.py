# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'welcome_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(541, 408)
        self.create_button = QPushButton(Form)
        self.create_button.setObjectName(u"create_button")
        self.create_button.setGeometry(QRect(310, 70, 171, 24))
        self.recent_list = QListWidget(Form)
        self.recent_list.setObjectName(u"recent_list")
        self.recent_list.setGeometry(QRect(10, 10, 241, 381))
        self.open_button = QPushButton(Form)
        self.open_button.setObjectName(u"open_button")
        self.open_button.setGeometry(QRect(310, 170, 171, 24))
        self.import_button = QPushButton(Form)
        self.import_button.setObjectName(u"import_button")
        self.import_button.setGeometry(QRect(310, 110, 171, 24))
        self.close_button = QPushButton(Form)
        self.close_button.setObjectName(u"close_button")
        self.close_button.setGeometry(QRect(310, 310, 171, 24))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.create_button.setText(QCoreApplication.translate("Form", u"Create New Project", None))
        self.open_button.setText(QCoreApplication.translate("Form", u"Open Selected Project", None))
        self.import_button.setText(QCoreApplication.translate("Form", u"Import Project", None))
        self.close_button.setText(QCoreApplication.translate("Form", u"Close", None))
    # retranslateUi

