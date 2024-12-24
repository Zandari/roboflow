"""
The package is intended for accessing the program's utility data files
"""

from .config_datastore import ConfigDataStore
from .projects_datastore import ProjectsDataStore
from .storage import JsonFileStorage, AbstractStorage

__all__ = [
    "ConfigDataStore",
    "ProjectsDataStore",

    "AbstractStorage",
    "JsonFileStorage",
]