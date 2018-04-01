from message import Message
from sys_utils import (
    read_message_list_file,
    read_message_file, delete_msg_file
)


def handle_user(msg: str):
    # TODO: Authenticate from Django here
    authenticated = True

    message = 'user accepted'

    if not authenticated:
        message = 'authentication failed'

    return Message(success=authenticated, message=message), 'user'


def handle_pass(msg: str, user):
    if user is None:  # or authentication from Django fails
        return Message(success=False, message='authentication failed')

    return Message(success=True,
                   message='password accepted, connection established')


def handle_list(msg: str, user):
    message_list = read_message_list_file(f'{user}_list.txt')
    messages = '\n'.join(message_list)

    return_message = f'Mailbox scan list follows\n{messages}'

    return Message(success=True, message=return_message)


def handle_retr(msg: str):
    try:
        message_id = int(msg.split(' ')[-1])
        contents = read_message_file(f'{message_id}.txt')

        return Message(success=True,
                       message=f'{len(contents)} octets\n{contents}')
    except ValueError:
        return Message(success=False, message='Message file not found')


def handle_dele(msg: str):
    message_id = msg.split(' ')[-1]
    deleted, delete_response = delete_msg_file(f'{message_id}.txt')

    return Message(success=deleted, message=delete_response)


def get_action_prefix(msg):
    return msg.split(' ')[0][1:]


def dispatch(msg: str):
    dispatcher = {
        'USER': handle_user,
        'PASS': handle_pass,
        'LIST': handle_list,
        'RETR': handle_retr,
        'DELE': handle_dele
    }

    action_prefix = get_action_prefix(msg)

    return dispatcher[action_prefix](msg)
