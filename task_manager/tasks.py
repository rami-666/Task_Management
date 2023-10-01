from celery import shared_task
from core import settings
import smtplib
from email.message import EmailMessage


@shared_task
def send_task_assignment_email(user_email, task_title, task_priority, task_due):
    subject = 'Task Assignment'
    text = f'You have been assigned a new task: \n\nTask Name: {task_title}\nPriority: {task_priority}\nDue Date: {task_due}'
    from_email = settings.EMAIL_HOST_USER  # Replace with your email address or use a configured sender
    recipient_list = [user_email]
    # Prepare actual message
    message = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

    %s
    """ % (from_email, ", ".join(recipient_list), subject, text)
    print(f"CELERY WORKER LAUNCHED")

    msg = EmailMessage()
    msg.set_content(text)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = user_email

    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    print("SMTP connection done")

    server.login(from_email, settings.EMAIL_HOST_PASSWORD)

    server.sendmail(from_email, recipient_list, message)
    print("message sent")
    server.quit()
