from . import BaseApiExeption

class FieldAlreadyExists(BaseApiExeption):
    def __init__(self, field: str):
        super().__init__(f"{field} already exists", status_code=400)