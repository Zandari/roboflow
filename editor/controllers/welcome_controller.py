from PySide6 import QtCore


class WelcomeController(QtCore.QObject):
    def __init__(self, model: QtCore.QObject):
        super().__init__()
        self._model = model