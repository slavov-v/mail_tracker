from message import Message
from sys_utils import (
    read_message_list_file,
    read_message_file,
    delete_msg_file,
    write_content_to_file
)


def handle_list(msg: str):
    _, user = msg.split(' ')
    try:
        message_list = read_message_list_file(f'{user}_list.txt')
        messages = '\n'.join(message_list)

        return_message = f'Mailbox scan list follows\n{messages}'
    except FileNotFoundError:
        return_message = 'No messages'

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
    _, user, message_id = msg.split(' ')
    list_file_contents = read_message_list_file(f'{user}_list.txt')

    to_remove = None
    for index, line in enumerate(list_file_contents):
        read_id = line.split(' ')[-1]
        if read_id and int(read_id) == message_id:
            to_remove = index

    if to_remove is not None:
        list_file_contents.pop(index)

        write_content_to_file(f'{user}_list.txt', '\n'.join(list_file_contents))

    deleted, delete_response = delete_msg_file(f'{message_id}.txt')

    return Message(success=deleted, message=delete_response)


def get_action_prefix(msg):
    return msg.split(' ')[0]


def dispatch(msg: str):
    dispatcher = {
        'LIST': handle_list,
        'RETR': handle_retr,
        'DELE': handle_dele
    }

    msg = msg.decode('utf-8')
    action_prefix = get_action_prefix(msg)

    return dispatcher[action_prefix](msg)
