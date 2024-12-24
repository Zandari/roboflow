from PySide6 import QtWidgets, QtCore, QtGui

from editor.models.editor_model import EditorModel
from editor.controllers.editor_controller import EditorController

from .widgets.scenario_treeview import ScenarioTreeViewWidget
from .widgets.state_edit import StateEditWidget
from .widgets.node_edit import NodeEdit
from .widgets.execute_widget import ExecuteWidget


class EditorWindow(QtWidgets.QMainWindow):
    project_saved = QtCore.Signal()

    def __init__(
        self,
        controller: EditorController,
        model: EditorModel,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Roboflow Editor")
        self.resize(1280, 720)

        self._controller = controller
        self._model = model

        self._init_menu_bar()

        self._tree_view = ScenarioTreeViewWidget(
            model=self._model.scenaries_model, 
            controller=self._controller,
            parent=self
        )
        self._tree_view.scenario_selected.connect(
            self._on_scenario_selected
        )

        tree_view_dock = QtWidgets.QDockWidget("", self)
        tree_view_dock.setWidget(self._tree_view)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, tree_view_dock)

        self._state_edit = StateEditWidget(
            scenario=None, 
            state=None,
            controller=self._controller
        )
        state_edit_dock = QtWidgets.QDockWidget("", self)
        state_edit_dock.setWidget(self._state_edit)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, state_edit_dock)

        self._execute_widget = ExecuteWidget(
            controller=self._controller
        )
        execute_widget_dock = QtWidgets.QDockWidget("", self)
        execute_widget_dock.setWidget(self._execute_widget)
        self.setCorner(
            QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea
        )
        self.setCorner(
            QtCore.Qt.BottomRightCorner, QtCore.Qt.RightDockWidgetArea
        )
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, execute_widget_dock)

        self._node_edit = NodeEdit(
            model=None,
            controller=self._controller
        )
        self._node_edit.state_selected.connect(self._on_state_selected)
        self.setCentralWidget(self._node_edit)

    @QtCore.Slot()
    def _on_state_selected(self, scenario, state) -> None:
        self._state_edit.set_state(scenario, state)
        self._state_edit.set_enabled(True)

    @QtCore.Slot()
    def _on_scenario_selected(self, scenario) -> None:
        self._node_edit.set_model(
            self._model.scenaries_model.get_states_model(scenario)
        )
        self._execute_widget.set_scenario(scenario)
        self._node_edit.enable()

    def _init_menu_bar(self) -> None:
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('File')
        save_action = QtGui.QAction('Save', self)
        save_action.triggered.connect(
            self._controller.save_project
        )
        file_menu.addAction(save_action)

       #view_menu = menu_bar.addMenu('View')
       #view_menu.addAction('Scenaries')
       #view_menu.addAction('States info')
       #view_menu.addAction('Execution Logs')

