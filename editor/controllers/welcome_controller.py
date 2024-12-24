from PySide6 import QtCore
import os


class WelcomeController(QtCore.QObject):
    project_opened = QtCore.Signal(str)
    project_created = QtCore.Signal(str)

    def __init__(self, model: QtCore.QObject):
        super().__init__()
        self._model = model

    def create_project(self, file_path: str) -> None:
        self._model.add_project(
            name=os.path.basename(file_path),
            file_path=file_path
        )
        self.project_created.emit(file_path)

    def import_project(self, file_path: str) -> None:
        self._model.add_project(
            name=os.path.basename(file_path),
            file_path=file_path
        )
        self.project_opened.emit(file_path)
    
    def open_project(self, file_path: str) -> None:
        self.project_opened.emit(file_path)