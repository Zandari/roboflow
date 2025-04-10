from abc import ABC, abstractmethod


class AbstractStorage(ABC):
    
    @abstractmethod
    def init_storage(self) -> None:
        """
        Check if storage structure exists and create it if not.
        """
        ...

    @abstractmethod
    def get_record(
        self,
        record_name: str,
        default: dict | None,
        overwrite: bool,
    ) -> dict:
        """ Reads record from storage.

        Args:
            record_name (str): Name of record.
            default     (Any): Returned value, if record reading failed. 
                               If equals None - raise Exception.
            overwrite  (bool): Should default value be written if error 
                               occured while reading record.

        Returns:
            dict: records content.
        """
        ...

    @abstractmethod
    def set_record(self, record_name: str, data: dict) -> None:
        """ Writes data into record.

        Args:
            record_name (str): Name of record.
            data (dict): Data that should be put into record
        """
        ...
