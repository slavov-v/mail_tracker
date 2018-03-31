import os


def read_init_file() -> str:
    init_fd = os.open('init_message.txt', os.O_RDONLY)

    while init_fd == -1:
        init_fd = os.open('init_message.txt', os.O_RDONLY)

    read_bytes = os.read(init_fd, 256)

    if len(read_bytes) == 0:
        read_init_file()

    os.close(fd)

    return read_bytes.decode('utf-8').split('\n')[0]
