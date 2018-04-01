import os


def read_init_file() -> str:
    """
    Reads the file with requests and returns the last request
    """

    init_fd = os.open('init_message.txt', os.O_RDONLY)

    while init_fd == -1:
        init_fd = os.open('init_message.txt', os.O_RDONLY)

    read_bytes = os.read(init_fd, 256)

    if len(read_bytes) == 0:
        read_init_file()

    os.close(init_fd)

    return read_bytes.decode('utf-8').split('\n')[-1]


def read_message_list_file(filepath: str) -> str:
    """
    Reads all contents of a message file and returns a list of the messages
    """
    message_fd = os.open(filepath, os.O_RDONLY)

    while message_fd == -1:
        message_fd = os.open(filepath, os.O_RDONLY)

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


def read_message_file(filepath: str):
    message_fd = os.open(filepath, os.O_RDONLY)

    retry_count = 0

    while message_fd == -1:
        if retry_count == 11:
            raise ValueError('Message file not found')

        message_fd = os.open(filepath, os.O_RDONLY)
        retry_count += 1

    end_reached = False
    messagefile_contents = ''

    while not end_reached:
        read_bytes = os.read(message_fd, 4096)

        if len(read_bytes) < 1:
            end_reached = True
            break

        messagefile_contents += read_bytes.decode('utf-8')

    return messagefile_contents
