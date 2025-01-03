from .abstract_storage import AbstractStorage
from datetime import date, datetime
import json
import os


class JsonFileStorage(AbstractStorage):
    def __init__(
        self, 
        path: str | os.PathLike, 
        record_ext: str = ".json"
    ):
        self._path = path
        self._record_ext = record_ext

    def _get_file_path(self, record_name: str):
        return os.path.join(
            self._path, record_name.lower() + self._record_ext
        )

    def init_storage(self) -> None:
        if os.path.isdir(self._path):
            return

        # TODO No error handling (((
        os.mkdir(self._path)

    def get_record(
        self,
        record_name: str,
        default: dict | None = None,
        overwrite: bool = False,
    ) -> dict:
        try:
            with open(self._get_file_path(record_name), "r") as file:
                return json.load(file, object_hook=self._json_deserial)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            if not default:
                raise e

        if overwrite:
            self.set_record(record_name, default)

        return default

    def set_record(self, record_name: str, data: dict) -> None:
        with open(self._get_file_path(record_name), "w") as file:
            json.dump(
                obj=data,
                fp=file,
                default=self._json_serial
            )
    @staticmethod
    def _json_deserial(data: dict) -> dict:
        result = dict()

        for key, value in data.items():
            if isinstance(value, str) and value.startswith("<date>"):
                result[key] = datetime.fromisoformat(
                    value.lstrip("<date>")
                )
            else:
                result[key] = value

        return result

    @staticmethod
    def _json_serial(obj):
        if isinstance(obj, (datetime, date)):
            return f"<date>{obj.isoformat()}"
        raise TypeError ("Type %s not serializable" % type(obj))
