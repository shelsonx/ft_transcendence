
from dataclasses import dataclass

@dataclass()
class SignUpDto:
    email: str
    password: str
    user_name: str