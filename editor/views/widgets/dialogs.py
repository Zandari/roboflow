from qtpy import QtCore, QtWidgets


class ConfirmationDialog(QtWidgets.QDialog):
    def __init__(self, text: str, title: str = "Confirmation"):
        super().__init__()

        self.setWindowTitle(title)

        self._label = QtWidgets.QLabel(text)
        self._confirm_button = QtWidgets.QPushButton("Confirm")
        self._confirm_button.clicked.connect(self.accept)
        self._dismiss_button = QtWidgets.QPushButton("Dismiss")
        self._dismiss_button.clicked.connect(self.reject)

        action_layout = QtWidgets.QHBoxLayout()
        action_layout.addWidget(self._confirm_button)
        action_layout.addWidget(self._dismiss_button)

        main_layout = QtWidgets.QVBoxLayout()

        main_layout.addWidget(self._label)
        main_layout.addLayout(action_layout)

        self.setLayout(main_layout)


class LineInputDialog(QtWidgets.QDialog):
    def __init__(self, text: str, title: str):
        super().__init__()

        self.setWindowTitle(title)

        self._label = QtWidgets.QLabel(text)
        self._line_edit = QtWidgets.QLineEdit()

        self._confirm_button = QtWidgets.QPushButton("Confirm")
        self._confirm_button.clicked.connect(self.accept)
        self._dismiss_button = QtWidgets.QPushButton("Cancel")
        self._dismiss_button.clicked.connect(self.reject)

        action_layout = QtWidgets.QHBoxLayout()
        action_layout.addWidget(self._confirm_button)
        action_layout.addWidget(self._dismiss_button)

        main_layout = QtWidgets.QVBoxLayout()

        main_layout.addWidget(self._label)
        main_layout.addWidget(self._line_edit)
        main_layout.addLayout(action_layout)

        self.setLayout(main_layout)

    def get_text(self) -> str:
        return self._line_edit.text()