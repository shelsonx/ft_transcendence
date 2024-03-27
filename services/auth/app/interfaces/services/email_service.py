from abc import ABC, abstractmethod
from typing import List

class IEmailService(ABC):

    @abstractmethod
    def send_email(self,  
            subject: str,
            message: str,
            from_email: str,
            recipient_list: List[str],
            html_message=None,) -> None:
        pass
