from PySide6 import QtCore
from .storage.abstract_storage import AbstractStorage
from .storage.projects_datastore import ProjectsDataStore, ProjectMeta


class WelcomeModel(QtCore.QAbstractListModel):
    def __init__(self, storage: AbstractStorage):
        super().__init__()

        self._data_store = ProjectsDataStore(storage)
        self._recent_projects = self._data_store.get_projects()

    @property
    def recent_projects(self) -> list[ProjectMeta]:
        return self._recent_projects
