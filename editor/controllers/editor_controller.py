from qtpy import QtCore
from editor.models.editor_model import EditorModel
from scenario.models import Scenario, State, Point, Action
from roboflow.main import execute_scenario
from random import randrange


class EditorController(QtCore.QObject):
    project_saved = QtCore.Signal()    

    def __init__(self, model: EditorModel):
        super(EditorController, self).__init__()
        self._model = model

    def execute(self, scenario: Scenario) -> None:
        execute_scenario(scenario)

    def save_project(self) -> None:
        self.project_saved.emit()

    def create_scenario(self, name: str | None = None) -> None:
        project = self._model.get_project()

        if name is None:
            index = len(project.scenaries)
            scenaries_names = (s.name for s in project.scenaries)
            name = f"Scenario {index}"
            while name in scenaries_names:
                name = f"Scenario {index}"
                index += 1

        state = State.get_blank_instance()
        state.name = "initial"
        scenar = Scenario(
            name=name,
            initial_state_id=0,
            states=[state]
        )

        self._model.scenaries_model.add_scenario(scenar)

    def create_state(self, scenario: Scenario) -> None:
        state_id = 1
        all_ids = (s.state_id for s in scenario.states)
        while state_id in all_ids:
            state_id += 1

        state = State.get_blank_instance()
        state.state_id = state_id
        state.name = "untitled"

        self._model.scenaries_model \
            .get_states_model(scenario) \
            .add_state(state)

    def update_state(self, scenario: Scenario, state: State, **kwargs) -> None:
        self._model.scenaries_model \
            .get_states_model(scenario) \
            .update_state(state, **kwargs)

    def add_state_connection(
        self, 
        scenario: Scenario,
        state_from: State, 
        state_to: State
    ) -> None:
        self._model.scenaries_model \
            .get_states_model(scenario) \
            .add_state_connection(state_from, state_to)

    def add_state_action(
        self,
        scenario: Scenario,
        state: State,
        action: Action
    ) -> None:
        self._model.scenaries_model \
            .get_states_model(scenario) \
            .add_state_action(state, action)

    def set_state_position(
        self,
        scenario: Scenario,
        state: State,
        pos: Point
    ) -> None:
        self._model.scenaries_model \
            .get_states_model(scenario) \
            .set_state_position(state, pos)

    def delete_scenario(self, scenario: Scenario) -> None:
        self._model.scenaries_model.delete_scenario(scenario)

    def update_scenario(self, scenario: Scenario) -> None:
        self._model.scenaries_model.update_scenario(scenario)

    def rename_scenario(self, scenario: Scenario, name: str) -> None:   # TODO блять
        scenario.name = name
        self._model.scenaries_model.update_scenario(scenario)

    def commit_changes(self) -> None:
        self.on_commit_changes.emit()
