from django.core.mail import send_mail
import os


class Util:
  @staticmethod
  def sending_mail(data):
    send_mail(
      subject = data['subject'],
      message = data['message'],
      from_email = os.environ.get('EMAIL_FROM'),
      recipient_list=[data['to_email']]
    )

# from django.core.mail import EmailMessage
# import os

# class Util:
#   @staticmethod
#   def send_email(data):
#     email = EmailMessage(
#       subject=data['subject'],
#       body=data['body'],
#       from_email=os.environ.get('EMAIL_FROM'),
#       to=[data['to_email']]
#     )
#     email.send()


# nik10-mah