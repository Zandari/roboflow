from qtpy import QtWidgets, QtGui, QtCore
from scenario.models import Scenario
from editor.controllers.editor_controller import EditorController
from editor.models.editor_model import ScenariesModel
import qtawesome as qta

from .dialogs import ConfirmationDialog, LineInputDialog


class ScenarioTreeViewWidget(QtWidgets.QWidget):
    _ACTION_BUTTON_SIZE = QtCore.QSize(50, 30)

    scenario_selected = QtCore.Signal(Scenario)

    def __init__(
        self, 
        model: ScenariesModel, 
        controller: EditorController, 
        *args, **kwargs
    ):
        super(ScenarioTreeViewWidget, self).__init__(*args, **kwargs)

        self._model = model
        self._model.scenaries_changed.connect(
            self._update_tree_view
        )
        self._controller = controller

        self._item_model = QtGui.QStandardItemModel()
        self._item_model.setHorizontalHeaderLabels(['Scenaries'])

        self._tree_view = QtWidgets.QTreeView()
        self._tree_view.setModel(self._item_model)
        self._tree_view.setHeaderHidden(True)
        self._tree_view.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self._tree_view.setSelectionMode(
            QtWidgets.QTreeView.SingleSelection
        )
        self._tree_view.setEditTriggers(QtWidgets.QTreeView.NoEditTriggers)
        self._tree_view.setAlternatingRowColors(True)
        self._tree_view.doubleClicked.connect(
            self._on_item_double_clicked
        )

        self._add_scenario_button = QtWidgets.QPushButton(
            qta.icon("mdi.plus"),
            "Add"
        )
        self._add_scenario_button.clicked.connect(
            self._on_add_scenario
        )
        self._add_scenario_button.setMinimumSize(self._ACTION_BUTTON_SIZE)

        self._delete_scenario_button = QtWidgets.QPushButton(
            qta.icon("mdi.delete"),
            "Delete"
        )
        self._delete_scenario_button.clicked.connect(
            self._on_delete_scenario
        )
        self._delete_scenario_button.setMinimumSize(self._ACTION_BUTTON_SIZE)

        self._edit_scenario_button = QtWidgets.QPushButton(
            qta.icon("mdi.pencil"),
            "Edit"
        )
        self._edit_scenario_button.clicked.connect(
            self._on_edit_scenario
        )
        self._edit_scenario_button.setMinimumSize(self._ACTION_BUTTON_SIZE)

        action_layout = QtWidgets.QHBoxLayout()
        action_layout.addWidget(self._add_scenario_button)
        action_layout.addWidget(self._delete_scenario_button)
        action_layout.addWidget(self._edit_scenario_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(action_layout)
        main_layout.addWidget(self._tree_view)
        self.setLayout(main_layout)

        self._update_tree_view(self._model.get_scenaries())

    @QtCore.Slot()
    def _on_item_double_clicked(self, index) -> None:
        item = self._item_model.itemFromIndex(index)
        print(item.scenario)
        if item:
            self.scenario_selected.emit(item.scenario)

    @QtCore.Slot()
    def _on_edit_scenario(self) -> None:
        item = self._get_selected_item()
        if item is None:
            return

        dialog = LineInputDialog(
            title="Scenario Edit",
            text=f"Enter new name of \"{item.scenario.name}\":",
        )
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self._controller.rename_scenario(
                scenario=item.scenario,
                name=dialog.get_text()
            )

    @QtCore.Slot()
    def _on_delete_scenario(self) -> None:
        item = self._get_selected_item()
        if item is None:
            return

        dialog = ConfirmationDialog(
            f"Are you sure you want to delete the scenario \"{item.scenario.name}\"?"
        )
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self._controller.delete_scenario(item.scenario)

    @QtCore.Slot()
    def _on_add_scenario(self) -> None:
        self._controller.create_scenario()

    @QtCore.Slot()
    def _update_tree_view(self, scenaries: list[Scenario]) -> None:
        self._item_model.clear()
        root_item = self._item_model.invisibleRootItem()
        for scenar in scenaries:
            item = QtGui.QStandardItem(scenar.name)
            item.scenario = scenar
            root_item.appendRow(item)

    def _get_selected_item(self) -> QtGui.QStandardItem | None:
        index = self._tree_view.currentIndex()
        if index.isValid():
            return self._item_model.itemFromIndex(index)
