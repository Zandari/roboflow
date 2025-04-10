from qtpy import QtWidgets, QtCore, QtGui
from scenario.models import Scenario, State
from roboflow.main import logger
from editor.controllers.editor_controller import EditorController
import logging
import qtawesome as qta


class LogHandler(logging.Handler):
    #on_new_record = QtCore.Signal(str)

    def __init__(self, parent):
        super(LogHandler, self).__init__()
        self._parent = parent
        #super(logging.Handler, self).__init__()

    def emit(self, record: logging.LogRecord):
        message = self.format(record)
        self._parent.add_record(message)


class LogWidget(QtWidgets.QPlainTextEdit):
    def __init__(self, parent = None):
        super().__init__(parent=parent)

        self.setObjectName("LogWidget")

        self.setReadOnly(True)

        self._clear_button = QtWidgets.QPushButton(
            qta.icon("mdi.eraser"), "", self
        )
        self._clear_button.setFixedSize(24, 24)
        self._clear_button.clicked.connect(self.clear)
        self._move_button_to_corner()

        self._handler = LogHandler(self)
        #self._handler.on_new_record.connect(self.appendPlainText)

    def add_record(self, record) -> None:
        self.appendPlainText(record)
    def resizeEvent(self, event: QtGui.QResizeEvent):
        super().resizeEvent(event)
        self._move_button_to_corner()

    def _move_button_to_corner(self):
        self._clear_button.move(
            self.width() - self._clear_button.size().width() - 5,
            self.height() - self._clear_button.size().height() - 5,
        )

    def get_handler(self) -> logging.Handler:
        return self._handler


class ExecuteWidget(QtWidgets.QWidget):
    def __init__(
        self, 
        controller: EditorController,
        scenario: Scenario = None,
    ):
        super().__init__()
        self._controller = controller

        self._start_button = QtWidgets.QPushButton(qta.icon("fa.play"), "Start")
        self._start_button.setFixedWidth(80)
        self._start_button.clicked.connect(self._on_start)
        self._device_combobox = QtWidgets.QComboBox()
        self._device_combobox.setMinimumWidth(200)
        self._update_devices_button = QtWidgets.QPushButton("Update")
        self._update_devices_button.setFixedWidth(60)

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(self._start_button)
        h_layout.addItem(QtWidgets.QSpacerItem(
            10, 0, 
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        ))
        #h_layout.addWidget(self._device_combobox)
        #h_layout.addWidget(self._update_devices_button)
        h_layout.addItem(QtWidgets.QSpacerItem(
            10, 10,
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        ))

        self._log_widget = LogWidget(self)
        #self._logs_textedit = QtWidgets.QTextEdit()

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(h_layout)
        main_layout.addWidget(self._log_widget)

        self._scenario = scenario
        if scenario is None:
            self._start_button.setEnabled(False)

        self.setLayout(main_layout)

        logger.addHandler(self._log_widget.get_handler())

    def set_scenario(self, scenario: Scenario) -> None:
        self._scenario = scenario
        self._start_button.setEnabled(True)

    @QtCore.Slot()
    def _on_start(self) -> None:
        self._controller.execute(self._scenario)