from dataclasses import dataclass
from typing import Union, Dict, List


@dataclass()
class ApiDataResponse:
    data: object = None
    message: Union[str, Dict[str, List[str]]] = "Ok"
    is_success: bool = True

    def to_dict(self):
        return {
            "data": self.data,
            "message": self.message,
            "is_success": self.is_success,
        }
