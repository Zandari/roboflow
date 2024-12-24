from .storage import AbstractStorage
from abc import ABC, abstractmethod
from dacite import from_dict
from dataclasses import asdict
from typing import Protocol, ClassVar, Any


def _abstract_const_param(func):
    return staticmethod(property(abstractmethod(func)))


class _DataclassProtocol(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Any]] 


class BaseDataStore(ABC):
    @_abstract_const_param
    def _RECORD_NAME(cls) -> str:
        ...

    @_abstract_const_param
    def _DEFAULT_RECORD(cls) -> dict:
        ...

    @_abstract_const_param
    def _STORE_MODEL(cls) -> _DataclassProtocol:
        ...

    def __init__(self, storage: AbstractStorage):
        self._storage = storage
        self._store: self._STORE_DATACLASS | None = None 

    def update(self) -> None:
        self._store = self._update_store()
# 
    def _update_store(self) -> _STORE_MODEL:
        # TODO probably would break on converting str to datetime on touched_at
        return from_dict(
            data_class=self._STORE_MODEL, 
            data=self._storage.get_record(
                record_name=self._RECORD_NAME, 
                default=self._DEFAULT_RECORD, 
                overwrite=True
            )
        )

    def save(self) -> None:
        self._storage.set_record(
            record_name=self._RECORD_NAME,
            data=asdict(self._store),
        )
        