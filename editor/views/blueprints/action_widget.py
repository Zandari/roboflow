# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'action_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpinBox,
    QTabWidget, QTextEdit, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 10, 381, 281))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(30, 40, 151, 71))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(9, 11, 31, 20))
        self.click_x_spinbox = QSpinBox(self.groupBox)
        self.click_x_spinbox.setObjectName(u"click_x_spinbox")
        self.click_x_spinbox.setGeometry(QRect(50, 10, 91, 24))
        self.click_y_spinbox = QSpinBox(self.groupBox)
        self.click_y_spinbox.setObjectName(u"click_y_spinbox")
        self.click_y_spinbox.setGeometry(QRect(50, 40, 91, 24))
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(9, 41, 31, 20))
        self.click_by_coords_checkbox = QCheckBox(self.tab)
        self.click_by_coords_checkbox.setObjectName(u"click_by_coords_checkbox")
        self.click_by_coords_checkbox.setGeometry(QRect(30, 20, 141, 22))
        self.click_by_text_checkbox = QCheckBox(self.tab)
        self.click_by_text_checkbox.setObjectName(u"click_by_text_checkbox")
        self.click_by_text_checkbox.setGeometry(QRect(200, 20, 141, 22))
        self.groupBox_2 = QGroupBox(self.tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(200, 40, 151, 71))
        self.click_text_lineedit = QLineEdit(self.groupBox_2)
        self.click_text_lineedit.setObjectName(u"click_text_lineedit")
        self.click_text_lineedit.setGeometry(QRect(10, 30, 131, 23))
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 10, 56, 16))
        self.add_click_button = QPushButton(self.tab)
        self.add_click_button.setObjectName(u"add_click_button")
        self.add_click_button.setGeometry(QRect(20, 220, 80, 24))
        self.label_7 = QLabel(self.tab)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(30, 140, 81, 21))
        self.click_duration_spinbox = QSpinBox(self.tab)
        self.click_duration_spinbox.setObjectName(u"click_duration_spinbox")
        self.click_duration_spinbox.setGeometry(QRect(120, 140, 111, 24))
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.delay_duration_spinbox = QSpinBox(self.tab_2)
        self.delay_duration_spinbox.setObjectName(u"delay_duration_spinbox")
        self.delay_duration_spinbox.setGeometry(QRect(100, 20, 101, 24))
        self.label_4 = QLabel(self.tab_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 20, 81, 21))
        self.add_delay_button = QPushButton(self.tab_2)
        self.add_delay_button.setObjectName(u"add_delay_button")
        self.add_delay_button.setGeometry(QRect(20, 220, 80, 24))
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.text_textedit = QTextEdit(self.tab_3)
        self.text_textedit.setObjectName(u"text_textedit")
        self.text_textedit.setGeometry(QRect(20, 40, 331, 171))
        self.label_5 = QLabel(self.tab_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 20, 81, 16))
        self.add_text_button = QPushButton(self.tab_3)
        self.add_text_button.setObjectName(u"add_text_button")
        self.add_text_button.setGeometry(QRect(20, 220, 80, 24))
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.runapp_package_lineedit = QLineEdit(self.tab_4)
        self.runapp_package_lineedit.setObjectName(u"runapp_package_lineedit")
        self.runapp_package_lineedit.setGeometry(QRect(20, 40, 341, 23))
        self.label_6 = QLabel(self.tab_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(20, 20, 91, 16))
        self.add_runapp_button = QPushButton(self.tab_4)
        self.add_runapp_button.setObjectName(u"add_runapp_button")
        self.add_runapp_button.setGeometry(QRect(20, 220, 80, 24))
        self.tabWidget.addTab(self.tab_4, "")

        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("Form", u"X", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Y", None))
        self.click_by_coords_checkbox.setText(QCoreApplication.translate("Form", u"By Coordinates", None))
        self.click_by_text_checkbox.setText(QCoreApplication.translate("Form", u"By Text", None))
        self.groupBox_2.setTitle("")
        self.label_3.setText(QCoreApplication.translate("Form", u"Text", None))
        self.add_click_button.setText(QCoreApplication.translate("Form", u"Add Click", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Duration(ms)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"Click", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Duration(ms)", None))
        self.add_delay_button.setText(QCoreApplication.translate("Form", u"Add Delay", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Delay", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Text to Enter", None))
        self.add_text_button.setText(QCoreApplication.translate("Form", u"Add Text", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Form", u"Text", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Package Name", None))
        self.add_runapp_button.setText(QCoreApplication.translate("Form", u"Add RunApp", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("Form", u"Run App", None))
    # retranslateUi

