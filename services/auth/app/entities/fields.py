from dataclasses import dataclass, field
from typing import Type, Any, List

@dataclass()
class Field:
  name: str
  is_required: bool = False
  field_type: Type[Any] = str
  validators: List[Any] = field(default_factory=list)