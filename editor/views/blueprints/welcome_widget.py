# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'welcome_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
        Form.resize(647, 403)
        self.create_button = QPushButton(Form)
        self.create_button.setObjectName(u"create_button")
        self.create_button.setGeometry(QRect(70, 30, 80, 24))
        self.recent_widget = QListWidget(Form)
        self.recent_widget.setObjectName(u"recent_widget")
        self.recent_widget.setGeometry(QRect(70, 90, 481, 192))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.create_button.setText(QCoreApplication.translate("Form", u"Create", None))
    # retranslateUi

