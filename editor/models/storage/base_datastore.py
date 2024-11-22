
from .abstract_storage import AbstractStorage
from abc import ABC, abstractmethod
from dacite import from_dict


def _abstract_const_param(func):
    return staticmethod(property(abstractmethod(func)))


class BaseDataStore(ABC):
    @_abstract_const_param
    def _RECORD_NAME(cls) -> str:
        ...

    @_abstract_const_param
    def _DEFAULT_RECORD(cls) -> str:
        ...

    @_abstract_const_param
    def _STORE_DATACLASS(cls) -> object:
        ...

    def __init__(self, storage: AbstractStorage):
        self._storage = storage
        self._store: self._STORE_DATACLASS = self._update_store()

    def update(self) -> None:
        self._store = self._update_store()

    def _update_store(self) -> _STORE_DATACLASS:
        # TODO probably would break on converting str to datetime on touched_at
        return from_dict(
            data_class=self._STORE_DATACLASS, 
            data=self._storage.get_record(
                record_name=self._RECORD_NAME, 
                default=self._DEFAULT_RECORD, 
                overwrite=True
            )
        )