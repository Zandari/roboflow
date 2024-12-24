from .blueprints.welcome_widget import Ui_Form
from qtpy import QtWidgets, QtCore

# For typings
from editor.models.welcome_model import WelcomeModel, ProjectInfo
from editor.controllers.welcome_controller import WelcomeController


class WelcomeWindow(QtWidgets.QWidget):
    def __init__(
        self, 
        controller: WelcomeController,
        model: WelcomeModel,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._controller = controller
        self._model = model

        self._model.projects_changed.connect(
            self._update_recent_projects
        )

        self._ui = Ui_Form()
        self._ui.setupUi(self)

        self._ui.create_button.clicked.connect(
            self._on_create_project
        )

        self._ui.import_button.clicked.connect(
            self._on_import_project
        )

        self._ui.open_button.clicked.connect(
            self._on_open_project
        )

    def _get_file_path(
        self, 
        window_title: str, 
        accept_mode: QtWidgets.QFileDialog.AcceptMode
    ) -> str:
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setWindowTitle(window_title)
        file_dialog.setAcceptMode(accept_mode)
        if accept_mode == QtWidgets.QFileDialog.AcceptOpen:
            file_dialog.setFileMode(
                QtWidgets.QFileDialog.FileMode.ExistingFile
            )

        file_path = None
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
        return file_path

    def _on_open_project(self) -> None:
        cur_item = self._ui.recent_list.currentItem()
        if cur_item is None:
            return
        self._controller.open_project(cur_item.file_path)

    @QtCore.Slot()
    def _on_import_project(self) -> None:
        file_path = self._get_file_path(
            window_title="Import Project",
            accept_mode=QtWidgets.QFileDialog.AcceptOpen,
        )
        if file_path is not None:
            self._controller.import_project(file_path)

    @QtCore.Slot()
    def _on_create_project(self) -> None:
        file_path = self._get_file_path(
            window_title="Create Project",
            accept_mode=QtWidgets.QFileDialog.AcceptSave
        )
        if file_path is not None:
            self._controller.create_project(file_path)

    def _update_recent_projects(self, projects: list[ProjectInfo]) -> None:
        self._ui.recent_list.clear()
        for project in projects:
            item = QtWidgets.QListWidgetItem(project.name)
            item.file_path = project.file_path
            self._ui.recent_list.addItem(item)