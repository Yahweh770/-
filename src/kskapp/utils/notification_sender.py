import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'admin@company.com'
    msg['To'] = to_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('your_email@gmail.com', 'password')
            server.send_message(msg)
    except Exception as e:
        print(f"Ошибка email: {e}")

def send_sms(to_number, message):
    client = Client("TWILIO_SID", "TWILIO_TOKEN")
    try:
        client.messages.create(
            body=message,
            from_="+1234567890",
            to=to_number
        )
    except Exception as e:
        print(f"Ошибка SMS: {e}")