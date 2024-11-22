from .blueprints.welcome_widget import Ui_Form
from PySide6 import QtWidgets

# For typings
from model.welcome_model import WelcomeModel
from controllers.welcome_controller import WelcomeController


class WelcomeWidget(QtWidgets.QWidget):
    def __init__(
        self, 
        controller: WelcomeController,
        model: WelcomeModel,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._controller = controller

        self._ui = Ui_Form()
        self._ui.setupUi(self)
