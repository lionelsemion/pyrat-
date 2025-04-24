import smtplib, ssl
from email.message import EmailMessage

import os
from dotenv import load_dotenv

load_dotenv()


def send_mail(name, url, receiver_email):
    with open("./mail_template.txt") as f:
        text = f.read()
        text = text.replace("{name}", name)
        text = text.replace("{url}", url)

    message = EmailMessage()
    message.set_content(text)

    sender_email = os.getenv("EMAIL_ADDRESS")

    message["Subject"] = "Dein KI-Song ist fertig"
    message["From"] = sender_email
    message["To"] = receiver_email

    port = 465  # For SSL
    password = os.getenv("EMAIL_PASSWORD")

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("mail.cyon.ch", port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(message)
