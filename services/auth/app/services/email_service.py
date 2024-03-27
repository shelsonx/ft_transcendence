from typing import List
from ..interfaces.services.email_service import IEmailService
from django.core.mail import send_mail

class EmailService(IEmailService):

  def send_email(self, subject: str, message: str, from_email: str, recipient_list: List[str], html_message=None) -> None:
    send_mail(subject, message, from_email, recipient_list, html_message)