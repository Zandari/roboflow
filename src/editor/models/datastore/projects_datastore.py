from .base_datastore import BaseDataStore
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass(frozen=True)
class ProjectInfo:
    name: str
    file_path: str
    updated_at: datetime


@dataclass(frozen=True)
class _Store:
    projects: list[ProjectInfo]


class ProjectsDataStore(BaseDataStore):
    _RECORD_NAME = "projects"
    _DEFAULT_RECORD = asdict(_Store([]))
    _STORE_MODEL = _Store

    @property
    def projects(self) -> list[ProjectInfo]:
        return self._store.projects