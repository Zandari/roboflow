from .views.welcome_window import WelcomeWindow
from .views.editor_window import EditorWindow

from .controllers.welcome_controller import WelcomeController
from .controllers.editor_controller import EditorController

from .models.welcome_model import WelcomeModel
from .models.editor_model import EditorModel

from .models.datastore.storage import JsonFileStorage

from scenario.models import Project

from qtpy import QtCore
from pathlib import Path

import os



class ProjectManager:
    _DEFAULT_PROJECT = Project(
        version="v0.1",
        scenaries=[],
    )

    def __init__(self):
        self._file_path: str | None = None
        self._current_project = self._DEFAULT_PROJECT

    def get_project(self) -> Project:
        return self._current_project

    def create_project(self, file_path: str | os.PathLike):
        self._current_project = self._DEFAULT_PROJECT
        with open(file_path, 'w') as file:
            file.write(self._current_project.to_xml())
        self._file_path = file_path

    def open_project(self, file_path: str | os.PathLike) -> Project:
        with open(file_path, 'r') as file:
            self._current_project = Project.from_xml(file.read())
        self._file_path = file_path
        return self._current_project

    def save_project(self) -> None:
        with open(self._file_path, 'w') as file:
            file.write(self._current_project.to_xml())



class Application(QtCore.QObject):
    def __init__(self, **kwargs):
        super(Application, self).__init__(**kwargs)

        # TODO on windows probably should store in APPDATA or registry
        self._local_storage = JsonFileStorage(Path.home() / '.roboflow')
        self._local_storage.init_storage()

        self._project_manager = ProjectManager()

        self._welcome_model = None
        self._welcome_controller = None
        self._welcome_window = None

        self._editor_model = None
        self._welcome_controller = None
        self._welcome_window = None

        self._init_welcome_window()
        self._init_editor_window()

        self._welcome_window.show()

    def _init_editor_window(self) -> None:
        self._editor_model = EditorModel(
            storage=self._local_storage,
            project=Project(
                version="",
                scenaries=[],
            )
        )
        self._editor_controller = EditorController(self._editor_model)
        self._editor_controller.project_saved.connect(
            self._project_manager.save_project
        )
        self._editor_window = EditorWindow(
            controller=self._editor_controller,
            model=self._editor_model,
        )

    def _init_welcome_window(self) -> None:
        self._welcome_model = WelcomeModel(self._local_storage)
        self._welcome_controller = WelcomeController(self._welcome_model)
        self._welcome_window = WelcomeWindow(
            controller=self._welcome_controller,
            model=self._welcome_model
        )

        self._welcome_model.update()

        self._welcome_controller.project_opened.connect(self._open_project)
        self._welcome_controller.project_created.connect(
            lambda fp: self._open_project(fp, create=True)
        )


    def _open_project(self, file_path: str, create: bool = False) -> None:
        try:
            if create:
                project = self._project_manager.create_project(file_path)
            else:
                project = self._project_manager.open_project(file_path)
        except Exception as e:   
            raise e        # TODO show message
        else:
            self._editor_model.set_project(project)
            self._welcome_window.hide()
            self._editor_window.show()