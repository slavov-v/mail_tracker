from django.utils import timezone
from django.conf import settings
from django.core.management.base import BaseCommand

from web.utils import EstablishConnection, parse_list_message


def time_run(func):
    def wrapper(*args, **kwargs):
        start = timezone.now()
        result = func(*args, **kwargs)
        end = timezone.now()

        print(f'{" ".join(args)} {end - start}')
        return result
    return wrapper


@time_run
def run_list_stats(file_size, message_count, username):
    with EstablishConnection() as connection:
        connection.send(settings.POP3_LIST_COMMAND.format(username).encode('utf-8'))
        data = connection.receive()
        parsed_data = parse_list_message(data.decode('utf-8'))

        context = {
            'response': parsed_data[0],
            'content': parsed_data[1]
        }

    return context


@time_run
def run_retr_stats(file_size, id):
    with EstablishConnection() as connection:
        connection.send(settings.POP3_RETRIEVE_COMMAND.format(id).encode('utf-8'))
        data = connection.receive()

        context = {
            'received_data': data.decode('utf-8'),
            'message_id': id
        }

    return context


@time_run
def run_dele_stats(file_size, id):
    with EstablishConnection() as connection:
        connection.send(settings.POP3_DELETE_COMMAND.format(
            'test',
            id).encode('utf-8'))


@time_run
def run_save_stats(message_size, message):
    with EstablishConnection() as connection:
        connection.send(settings.POP3_SAVE_COMMAND.format(message).encode('utf-8'))


class Command(BaseCommand):
    def handle(self, *args, **options):
        usernames = ['test', 'test1', 'test2', 'test3', 'test4']
        file_sizes = ['231', '569', '909', '2691', '4510']
        message_count = ['30', '70', '100', '300', '500']

        for index, username in enumerate(usernames):
            run_list_stats(f'LIST Size:{file_sizes[index]}', f'Messages:{message_count[index]}', username=username)

        file_sizes = [100, 500, 1000, 2000, 4000, 8000, 15000, 50000, 150000, 300000]
        for i in range(1, 11):
            run_retr_stats(f'RETR Size: {file_sizes[i-1]}', id=i)

        for index, i in enumerate(range(2001, 2011)):
            run_dele_stats(f'DELE Size: {file_sizes[index]}', id=i)

        for index, message in enumerate():
            pass
