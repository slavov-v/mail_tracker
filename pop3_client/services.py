from message import Message
from sys_utils import (
    read_message_list_file,
    read_message_file,
    delete_msg_file,
    write_content_to_file,
    clear_file_content,
    read_id_file,
    write_new_id
)


def handle_list(msg: str) -> Message:
    _, user = msg.split(' ')
    try:
        message_list = read_message_list_file(f'{user}_list.txt')
        messages = '\n'.join(message_list)

        return_message = f'Mailbox scan list follows\n{messages}'
    except FileNotFoundError:
        return_message = 'No messages'

    return Message(success=True, message=return_message)


def handle_retr(msg: str) -> Message:
    try:
        message_id = int(msg.split(' ')[-1])
        contents = read_message_file(f'{message_id}.txt')

        return Message(success=True,
                       message=f'{len(contents)} octets\n{contents}')
    except ValueError:
        return Message(success=False, message='Message file not found')


def handle_dele(msg: str) -> Message:
    _, user, message_id = msg.split(' ')
    list_file_contents = read_message_list_file(f'{user}_list.txt')

    to_remove = None
    for index, line in enumerate(list_file_contents):
        read_id = line.split(' ')[-1]

        if read_id and read_id == message_id:
            to_remove = index
            break

    if to_remove is not None:
        del list_file_contents[to_remove]

        clear_file_content(f'{user}_list.txt')
        write_content_to_file(f'{user}_list.txt', '\n'.join(list_file_contents))

    deleted, delete_response = delete_msg_file(f'{message_id}.txt')

    return Message(success=deleted, message=delete_response)


def handle_save(msg: str) -> None:
    command_and_subject, *data = msg.split('|')

    subject = ' '.join(command_and_subject.split(' ')[1:])
    sender, recipient, content = data
    ids = read_id_file()

    last_id = ids[-1]

    write_new_id(last_id + 1)

    list_file_path = f'{recipient.split("@")[0]}_list.txt'
    list_file_message = f'{subject} {last_id + 1}\n'
    write_content_to_file(list_file_path, list_file_message)

    message_file_path = f'{last_id + 1}.txt'
    write_content_to_file(message_file_path, content)


def get_action_prefix(msg: str) -> str:
    return msg.split(' ')[0]


def dispatch(msg: str) -> Message:
    dispatcher = {
        'LIST': handle_list,
        'RETR': handle_retr,
        'DELE': handle_dele,
        'SAVE': handle_save
    }

    msg = msg.decode('utf-8')
    action_prefix = get_action_prefix(msg)

    return dispatcher[action_prefix](msg)
