import socket

from django.core.mail import send_mail
from django.conf import settings


def parse_list_message(message):
    response, *content = message.split('\n')
    response = ' '.join(response.split(' ')[1:])

    result_content = []

    for item in content:
        if not len(item) > 0:
            continue

        subject, item_id = item.split(' ')

        result_content.append({
            'subject': subject,
            'id': item_id
        })

    print(result_content)

    return response, result_content


def send_email(sender, subject, recipients, content):
    LOCAL_DOMAINS = ['localhost', '127.0.0.1', '0.0.0.0']
    recipient_domain = recipients[0].split('@')[-1].split('.')[0]

    if recipient_domain in LOCAL_DOMAINS:
        message = f'{subject}|{sender}|{",".join(recipients)}|{content}'

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((settings.POP3_HOST, settings.POP3_PORT))
            s.sendall(settings.POP3_SAVE_COMMAND.format(message).encode('utf-8'))

        return

    send_mail(subject, content, sender, recipients, fail_silently=False)
