from .base_datastore import BaseDataStore
from dataclasses import dataclass, asdict


@dataclass
class _Store:
    ... # TODO unknown for now


class ConfigDataStore(BaseDataStore):
    _RECORD_NAME = "config"
    _DEFAULT_RECORD = asdict(_Store())
    _STORE_MODEL = _Store

    ...