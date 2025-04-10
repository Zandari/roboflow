from qtpy import QtCore
from datetime import datetime
from .datastore import AbstractStorage
from .datastore.projects_datastore import ProjectsDataStore, ProjectInfo


class ProjectAlreadyExist(Exception):
    pass


class WelcomeModel(QtCore.QObject):
    projects_changed = QtCore.Signal(list) 

    def __init__(self, storage: AbstractStorage):
        super().__init__()

        self._data_store = ProjectsDataStore(storage)

    def update(self) -> None:
        self._data_store.update()
        self.projects_changed.emit(self._data_store.projects)

    def get_projects(self) -> list[ProjectInfo]:
        return self._data_store.projects

    def add_project(
        self, 
        name: str, 
        file_path: str, 
        updated_at: datetime | None = None
    ) -> None:
        if updated_at is None:
            updated_at = datetime.now()

        if file_path in [f.file_path for f in self._data_store.projects]:
            return
            # raise ProjectAlreadyExist(
            #     f"Project \"{file_path}\" already in the data store."
            # )

        self._data_store.projects.append(
            ProjectInfo(
                name=name, 
                file_path=file_path, 
                updated_at=updated_at
            )
        )
        self._data_store.save()

        self.projects_changed.emit(self._data_store.projects)

    def remove_project(self, file_path: str) -> bool:
        is_removed = False

        for i, proj in enumerate(self._data_store.projects):
            if proj.file_path == file_path:
                self._data_store.projects.remove(i)
                self._data_store.save()
                self.projects_changed.emit(self._data_store.projects)
                is_removed = True

        if is_removed:
            self.projects_changed.emit(self._data_store.projects)

        return is_removed

