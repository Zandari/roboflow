from PySide6 import QtCore
from pathlib import Path

from .views.welcome_widget import WelcomeWidget
from .controllers.welcome_controller import WelcomeController
from .models.welcome_model import WelcomeModel

from .models.storage.json_storage import JsonFileStorage


class Application(QtCore.QObject):
    def __init__(self, **kwargs):
        super(Application, self).__init__(**kwargs)

        # TODO on windows probably should store in APPDATA
        self._local_storage = JsonFileStorage(Path.home() / '.roboflow')
        self._local_storage.init_storage()

        self._init_welcome_window()

    def _init_welcome_window(self) -> None:
        self._welcome_model = WelcomeModel(self._local_storage)
        self._welcome_controller = WelcomeController(None)
        self._welcome_view = WelcomeWidget(
            controller=self._welcome_controller,
            model=self._welcome_model
        )
        self._welcome_view.show()