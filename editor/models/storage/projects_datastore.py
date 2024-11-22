from .base_datastore import BaseDataStore
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class ProjectMeta:
    name: str
    file_path: str
    touched_at: datetime


@dataclass
class _Store:
    projects: list[ProjectMeta]


class ProjectsDataStore(BaseDataStore):
    _RECORD_NAME = "projects"
    _DEFAULT_RECORD = asdict(_Store([]))
    _STORE_DATACLASS = _Store

    def get_projects(self) -> list[ProjectMeta]:
        return self._store.projects