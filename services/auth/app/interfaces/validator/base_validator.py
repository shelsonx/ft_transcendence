from dataclasses import dataclass
from ...entities.validation_data import ValidationData
from abc import ABC, abstractmethod
from typing import Any 

@dataclass
class BaseValidator(ABC):

  validation_data: ValidationData

  @abstractmethod
  def validate(self, *args, **kwargs) -> ValidationData:
    pass
  
  