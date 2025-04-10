from qtpy import QtWidgets, QtCore
from scenario.models import (
    State, Scenario, Statement, ValueType, Condition, Point,
    ClickCoordsAction, ClickTextAction, WaitAction, WriteAction,
    RunAppAction, Action
)
from editor.controllers.editor_controller import EditorController
import qtawesome as qta
from ..blueprints.action_widget import Ui_Form


class ActionWidget(QtWidgets.QWidget):
    action_added = QtCore.Signal(Action)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Action")

        self._ui = Ui_Form()
        self._ui.setupUi(self)

        self._ui.click_by_coords_checkbox.stateChanged.connect(
            self._on_coords_checkbox_state_changed
        )
        self._ui.click_by_text_checkbox.stateChanged.connect(
            self._on_text_checkbox_state_changed
        )
        self._on_text_checkbox_state_changed(False)

        self._ui.add_click_button.clicked.connect(self._on_add_click)
        self._ui.add_delay_button.clicked.connect(self._on_add_delay)
        self._ui.add_text_button.clicked.connect(self._on_add_text)
        self._ui.add_runapp_button.clicked.connect(self._on_add_runapp)

    @QtCore.Slot()
    def _on_coords_checkbox_state_changed(self, state) -> None:
        state = bool(state)
        self._ui.click_x_spinbox.setEnabled(state)
        self._ui.click_y_spinbox.setEnabled(state)
        self._ui.click_by_text_checkbox.setChecked(not state)

    @QtCore.Slot()
    def _on_text_checkbox_state_changed(self, state) -> None:
        state = bool(state)
        self._ui.click_text_lineedit.setEnabled(state)
        self._ui.click_by_coords_checkbox.setChecked(not state)

    @QtCore.Slot()
    def _on_add_click(self) -> None:
        if self._ui.click_by_coords_checkbox.isChecked():
            self.action_added.emit(
                ClickCoordsAction(
                    coords=Point(
                        x=self._ui.click_x_spinbox.value(),
                        y=self._ui.click_y_spinbox.value(),
                    ),
                    duration_ms=self._ui.click_duration_spinbox.value()
                )
            )
        elif self._ui.click_by_text_checkbox.isChecked():
            self.action_added.emit(
                ClickTextAction(
                    text=self._ui.click_text_lineedit.text(),
                    duration_ms=self._ui.click_duration_spinbox.value()
                )
            )

    @QtCore.Slot()
    def _on_add_delay(self) -> None:
        self.action_added.emit(
            WaitAction(
                duration_ms=self._ui.delay_duration_spinbox.value()
            )
        )

    @QtCore.Slot()
    def _on_add_text(self) -> None:
        self.action_added.emit(
            WriteAction(
                text=self._ui.text_textedit.toPlainText()
            )
        )

    @QtCore.Slot()
    def _on_add_runapp(self) -> None:
        self.action_added.emit(
            RunAppAction(
                package_name=self._ui.runapp_package_lineedit.text()
            )
        )


class StatementEditWiget(QtWidgets.QWidget):
    def __init__(self, statement: Statement):
        super().__init__()

        self._statement = statement

        value_type_values = [e.value for e in ValueType]

        self._value_type_combobox_1 = QtWidgets.QComboBox(self)
        self._value_type_combobox_1.addItems(value_type_values)
        self._value_type_combobox_1.setCurrentText(
            self._statement.value_type_1.value
        )

        self._value_lineedit_1 = QtWidgets.QLineEdit()
        self._value_lineedit_1.setText(self._statement.value1)

        self._condition_combobox = QtWidgets.QComboBox()
        self._condition_combobox.addItems([e.value for e in Condition])
        self._condition_combobox.setCurrentText(
            self._statement.condition.value
        )

        self._value_lineedit_2 = QtWidgets.QLineEdit()
        self._value_lineedit_2.setText(self._statement.value2)

        self._value_type_combobox_2 = QtWidgets.QComboBox()
        self._value_type_combobox_2.addItems(value_type_values)
        self._value_type_combobox_2.setCurrentText(
            self._statement.value_type_2.value
        )

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self._value_type_combobox_1)
        layout.addWidget(self._value_lineedit_1)
        layout.addWidget(self._condition_combobox)
        layout.addWidget(self._value_lineedit_2)
        layout.addWidget(self._value_type_combobox_2)

        #self.setMinimumHeight(70)
        
        self.setLayout(layout)

    def get_statement(self) -> Statement:
        return Statement(
            value_type_1=ValueType(self._value_type_combobox_1.currentText()),
            value1=self._value_lineedit_1.text(),
            value_type_2=ValueType(self._value_type_combobox_2.currentText()),
            value2=self._value_lineedit_2.text(),
            condition=Condition(self._condition_combobox.currentText()),
        )


class StateEditWidget(QtWidgets.QWidget):
    def __init__(
        self,
        scenario: Scenario | None,
        state: State | None,
        controller: EditorController,
    ):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()

        self._controller = controller

        self._label1 = QtWidgets.QLabel("State Name")
        self._name_line_edit = QtWidgets.QLineEdit()
        # self._name_line_edit.setPlaceholderText("")

        self._label2 = QtWidgets.QLabel("Description")
        self._description_text_edit = QtWidgets.QTextEdit()
        self._description_text_edit.setFixedHeight(70)

        self._save_button = QtWidgets.QPushButton("Save")
        self._save_button.clicked.connect(
            self._on_save
        )

        self._label3 = QtWidgets.QLabel("Statements")
        self._statements_list_widget = QtWidgets.QListWidget()
        self._statements_list_widget.setSelectionMode(
            QtWidgets.QListWidget.NoSelection
        )
        self._add_statement_button = QtWidgets.QPushButton(qta.icon("mdi.plus"), "Add Statement")
        self._add_statement_button.clicked.connect(
            self._on_add_statement
        )

        self._label4 = QtWidgets.QLabel("Actions")
        self._actions_list_widget = QtWidgets.QListWidget()
        self._statements_list_widget.setSelectionMode(
            QtWidgets.QListWidget.NoSelection
        )
        self._add_action_button = QtWidgets.QPushButton(qta.icon("mdi.plus"), "Add Action")
        self._add_action_button.clicked.connect(
            self._on_add_action
        )

        self._state = state
        self._scenario = scenario
        if state is None or scenario is None:
            self.set_enabled(False)
        else:
            self._update_fields()

        layout.addWidget(self._label1)
        layout.addWidget(self._name_line_edit)

        layout.addWidget(self._label2)
        layout.addWidget(self._description_text_edit)

        layout.addWidget(self._label3)
        layout.addWidget(self._statements_list_widget)
        layout.addWidget(self._add_statement_button)

        layout.addWidget(self._label4)
        layout.addWidget(self._actions_list_widget)
        layout.addWidget(self._add_action_button)

        layout.addItem(QtWidgets.QSpacerItem(
            50, 50, 
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        ))
        layout.addWidget(self._save_button)
        layout.addStretch()
        self.setLayout(layout)

    def set_enabled(self, enable: bool) -> None:
        self._name_line_edit.setEnabled(enable)
        self._description_text_edit.setEnabled(enable)
        self._save_button.setEnabled(enable)
        self._statements_list_widget.setEnabled(enable)
        self._add_statement_button.setEnabled(enable)
        self._actions_list_widget.setEnabled(enable)
        self._add_action_button.setEnabled(enable)

    def set_state(self, scenario: Scenario, state: State) -> None:
        self._scenario = scenario
        self._state = state
        self._update_fields()

    def _update_fields(self) -> None:
        self._name_line_edit.setText(self._state.name)
        self._description_text_edit.setText(self._state.description)
        self._statements_list_widget.clear()
        for statement in self._state.statements:
            self._add_statement(statement)
        self._actions_list_widget
        self._actions_list_widget.clear()
        for action in self._state.actions:
            self._actions_list_widget.addItem(
                QtWidgets.QListWidgetItem(str(action))
            )

    def _get_statements(self) -> list[Statement]:
        result = list[Statement]()

        for index in range(self._statements_list_widget.count()):
            item = self._statements_list_widget.item(index)
            widget = self._statements_list_widget.itemWidget(item)
            if widget:
                result.append(widget.get_statement())

        return result

    def _add_statement(self, statement: Statement) -> None:
        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(QtCore.QSize(100, 40))
        self._statements_list_widget.addItem(item)
        self._statements_list_widget.setItemWidget(
            item,
            StatementEditWiget(statement)
        )

    @QtCore.Slot()
    def _on_add_action(self) -> None:
        self._action_widget = ActionWidget()
        self._action_widget.action_added.connect(
            self._on_action_added
        )
        self._action_widget.show()

    @QtCore.Slot() 
    def _on_action_added(self, action: Action) -> None:
        self._controller.add_state_action(
            scenario=self._scenario, 
            state=self._state,
            action=action
        )
        self._action_widget.close()
        self._actions_list_widget.addItem(
            QtWidgets.QListWidgetItem(str(action))
        )

    @QtCore.Slot()
    def _on_add_statement(self) -> None:
        self._add_statement(
            Statement.get_blank_instance()
        )


    @QtCore.Slot()
    def _on_save(self) -> None:
        if self._state is None or self._scenario is None:
            return

        state_name = self._name_line_edit.text()
        state_description = self._description_text_edit.toPlainText()
        state_statements = self._get_statements()

        self._controller.update_state(
            scenario=self._scenario,
            state=self._state,
            name=state_name,
            description=state_description,
            statements=state_statements,
            # TODO actions,
        )