from django.core.mail import EmailMessage
from django.conf import settings

def sendOtp(request,email,value):
    body = f'hi ,{request.user.username}\n your otp is {value}'
    email = EmailMessage(
        'testing',
        body,
        settings.EMAIL_HOST_USER,
        [email]
    )

    email.fail_silently=False
    email.send()