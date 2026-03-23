import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender: str, password: str, receiver: str, subject: str, body: str) -> bool:
    """
    Send an email using Gmail SMTP.

    Args:
        sender (str): Sender's email address
        password (str): Sender's password or app password
        receiver (str): Recipient's email address
        subject (str): Email subject
        body (str): Email body

    Returns:
        bool: True if sent successfully, False otherwise
    """
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False