from dataclasses import dataclass

@dataclass()
class SignInDto:
    email: str
    password: str