from django.utils import timezone
from django.conf import settings
from django.core.management.base import BaseCommand

from web.utils import EstablishConnection, parse_list_message


def time_run(func):
    def wrapper(*args, **kwargs):
        start = timezone.now()
        result = func(*args, **kwargs)
        end = timezone.now()

        print(f'{args} {end - start}')
        return result
    return wrapper


@time_run
def run_list(username):
    with EstablishConnection() as connection:
        connection.send(settings.POP3_LIST_COMMAND.format(username).encode('utf-8'))
        data = connection.receive()
        parsed_data = parse_list_message(data.decode('utf-8'))

        context = {
            'response': parsed_data[0],
            'content': parsed_data[1]
        }

    return context


class Command(BaseCommand):
    def handle(self, *args, **options):
        usernames = ['test', 'test1', 'test2', 'test3']
        for username in usernames:
            run_list(username)
