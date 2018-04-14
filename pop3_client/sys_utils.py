import os
from typing import Tuple

SHARED_DIR = '../shared/'


def read_init_file() -> str:
    """
    Reads the file with requests and returns a list of the requests
    """

    init_fd = os.open(f'{SHARED_DIR}init_message.txt', os.O_RDONLY)

    while init_fd == -1:
        init_fd = os.open(f'{SHARED_DIR}init_message.txt', os.O_RDONLY)

    read_bytes = os.read(init_fd, 256)

    if len(read_bytes) == 0:
        read_init_file()

    os.close(init_fd)

    read_bytes.decode('utf-8').split('\n')


def read_message_list_file(filepath: str) -> str:
    """
    Reads all contents of a message file and returns a list of the messages
    """
    message_fd = os.open(f'{SHARED_DIR}{filepath}', os.O_RDONLY)

    while message_fd == -1:
        message_fd = os.open(f'{SHARED_DIR}{filepath}', os.O_RDONLY)

    end_reached = False
    messagefile_contents = ''

    while not end_reached:
        read_bytes = os.read(message_fd, 4096)

        if len(read_bytes) < 1:
            end_reached = True
            break

        messagefile_contents += read_bytes.decode('utf-8')

    os.close(message_fd)

    return messagefile_contents.split('\n')


def read_message_file(filepath: str) -> Tuple[bool, str]:
    try:
        message_fd = os.open(f'{SHARED_DIR}{filepath}', os.O_RDONLY)
    except FileNotFoundError:
        return False, 'Message file not found'

    end_reached = False
    messagefile_contents = ''

    while not end_reached:
        read_bytes = os.read(message_fd, 4096)

        if len(read_bytes) < 1:
            end_reached = True
            break

        messagefile_contents += read_bytes.decode('utf-8')

    return messagefile_contents


def read_id_file():
    try:
        # TODO: read till end of file
        fd = os.open(f'{SHARED_DIR}message_ids.txt', os.O_RDONLY)
        content = os.read(fd, 8192).decode('utf-8')
        os.close(fd)

        ids = content.split('\n')
        ids.remove('')

        return sorted([int(item) for item in ids])
    except FileNotFoundError:
        return [-1]


def write_new_id(new_id):
    write_content_to_file(f'{SHARED_DIR}message_ids.txt', f'{new_id}\n')


def delete_msg_file(filepath: str) -> Tuple[bool, str]:
    try:
        os.unlink(f'{SHARED_DIR}{filepath}')

        return True, 'Message deleted'
    except FileNotFoundError:
        return False, 'Message file not found'


def clear_file_content(filepath: str):
    fd = os.open(f'{SHARED_DIR}{filepath}', os.O_WRONLY)
    os.ftruncate(fd, 0)
    os.lseek(fd, 0, os.SEEK_SET)

    os.close(fd)


def write_content_to_file(filepath: str, content: str):
    fd = os.open(f'{SHARED_DIR}{filepath}', os.O_WRONLY | os.O_APPEND | os.O_CREAT)

    written_bytes = os.write(fd, content.encode('utf-8'))
    os.close(fd)

    return written_bytes
