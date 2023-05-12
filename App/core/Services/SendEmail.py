import smtplib
from email.message import EmailMessage
import Setting

def send_email(recipient_email, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = Setting.SMTP_SENDER_MAIL
    msg['To'] = recipient_email

    # Login to the Gmail SMTP server
    with smtplib.SMTP(Setting.SMTP_SERVER, Setting.SMTP_PORT) as server:
        server.ehlo()  # Can be omitted
        server.starttls()
        server.login(Setting.SMTP_SENDER_MAIL, Setting.SMTP_PASSWORD)

        # Send the email
        server.send_message(msg)

        # Logout of the SMTP server
        server.quit()