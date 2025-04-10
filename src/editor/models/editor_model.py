from PySide6 import QtCore
from .datastore import AbstractStorage
from .datastore import ConfigDataStore

from scenario.models import Project, Scenario, State, Point, Action


class ScenariesModel(QtCore.QObject):
    scenaries_changed = QtCore.Signal(list)
    _states_changed = QtCore.Signal()   # for global project_changed signal

    def __init__(
        self,
        scenaries: list[Scenario],
    ):
        super(ScenariesModel, self).__init__()
        self._scenaries = scenaries
        # cache for singleton-like behaviour of StatesModel
        self._states_models = dict[Scenario, StatesModel]()

    def set_scenaries(self, scenaries: list[Scenario]) -> None:
        self._scenaries = scenaries
        self.scenaries_changed.emit(self.get_scenaries())

    def update_scenario(self, scenario: Scenario) -> None:
        self.scenaries_changed.emit(self.get_scenaries())
    
    def delete_scenario(self, scenario: Scenario) -> None:
        del self._scenaries[self._scenaries.index(scenario)]
        self.scenaries_changed.emit(self.get_scenaries())

    def add_scenario(self, scenario: Scenario) -> None:
        self._scenaries.append(scenario)
        self.scenaries_changed.emit(self._scenaries)

    def get_scenaries(self) -> list[Scenario]:
        return self._scenaries

    def get_states_model(self, scenario: Scenario) -> None:
        states_model = self._states_models.get(scenario)
        if states_model is not None:
            return states_model
        states_model = StatesModel(scenario)
        states_model.states_changed.connect(
            lambda _: self._states_changed.emit()
        )
        self._states_models[scenario] = states_model
        return states_model


class StatesModel(QtCore.QObject):
    states_changed = QtCore.Signal(list)

    def __init__(self, scenario: Scenario):
        super(StatesModel, self).__init__()
        self._scenario = scenario

    def get_scenario(self) -> Scenario:
        return self._scenario

    def get_states(self) -> list[State]:
        return self._scenario.states

    def add_state(self, state: State) -> None:
        self._scenario.states.append(state)
        self.states_changed.emit(self.get_states())

    def add_state_action(self, state: State, action: Action) -> None:
        state.actions.append(action)
        self.states_changed.emit(self.get_states())

    def add_state_connection(self, state_from: State, state_to: State) -> None:
        state_from.next_states.add(state_to.state_id)
        # self.states_changed.emit(self.get_states()) оно крашит, хз почему

    def set_state_position(self, state: State, position: Point) -> None:
        state.position = position
        # self.states_changed.emit(self.get_states()) блять, опять

    def update_state(self, state: State, **kwargs) -> None:
        for name, value in kwargs.items():
            setattr(state, name, value)
        self.states_changed.emit(self.get_states())

    def delete_state(self, state: State) -> None:
        self.states_changed.emit(self.get_states())


class EditorModel(QtCore.QObject):
    def __init__(
        self, 
        storage: AbstractStorage, 
        project: Project
    ):
        super().__init__()

        self._config_data_store = ConfigDataStore(storage)
        self._project = project 

        self._scenaries_model = ScenariesModel(self._project.scenaries)

    @property
    def scenaries_model(self) -> ScenariesModel:
        return self._scenaries_model

    def get_project(self) -> Project:
        return self._project

    def set_project(self, project: Project) -> None:
        self._project = project
        self._scenaries_model.set_scenaries(project.scenaries)

