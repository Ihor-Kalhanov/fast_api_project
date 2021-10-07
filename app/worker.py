import time
import smtplib

from starlette.responses import JSONResponse
from celery import Celery
from email.message import EmailMessage

celery = Celery(
    name='tasks',
    broker='amqp://user:password@broker:5672//'
)


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


@celery.task(serializer='json')
def send_email(email_list):
    MAIL_SERVER = 'smtp.gmail.com'

    gmail_user = 'ihor.kalhanov-mt181@nung.edu.ua'
    gmail_password = 'Maffia12345'

    email_subject = "This is subject"
    email_text = "This is text."

    msg = EmailMessage()
    msg.set_content(email_text)
    msg['From'] = gmail_user
    msg['To'] = email_list
    msg['Subject'] = email_subject
    try:
        server = smtplib.SMTP(MAIL_SERVER, 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.close()
        print('Email sent!')
    except:
        print('Something went wrong...')
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
