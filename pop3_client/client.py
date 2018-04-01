import time

from sys_utils import read_init_file
from services import dispatch


def main():
    dispatched_actions = 0

    while True:
        try:
            # Blocking the main process until an action is read
            init_actions = read_init_file()
            dispatch(init_actions[dispatched_actions])
            dispatched_actions += 1
        except IndexError:
            time.sleep(1)


if __name__ == '__main__':
    main()
