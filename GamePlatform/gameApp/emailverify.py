from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import random
import string
from GamePlatform.settings import DEFAULT_FROM_EMAIL
def generate_verification_code(length=4):
    characters = string.ascii_letters + string.digits
    verification_code = ''.join(random.choice(characters) for _ in range(length))
    return verification_code

def send_verify_code(userEmail):
    subject = 'Please Verify Your Email'
    from_email = DEFAULT_FROM_EMAIL
    to_email = [userEmail]
    verification_code=generate_verification_code(4)
    content = render_to_string('verifycontent.html', {'verification_code': verification_code})
    email = EmailMessage(subject, content, from_email, to_email)
    email.content_subtype = 'html'  # 使用 HTML 內容
    email.send()
    return verification_code

if __name__ == "__main__":
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GamePlatform.settings')
    django.setup()
    send_verify_code("one810607@gmail.com")