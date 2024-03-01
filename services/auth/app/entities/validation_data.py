from dataclasses import dataclass


@dataclass
class ValidationData:

  is_success: bool
  message: str

