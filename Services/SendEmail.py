import smtplib
from email.message import EmailMessage

def send_email(sender_email, password, recipient_email, subject, body):
    smtp_server = "dinotech.net"
    port = 587  # For starttls
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Login to the Gmail SMTP server
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls()
        server.login(sender_email, password)

        # Send the email
        server.send_message(msg)

        # Logout of the SMTP server
        server.quit()