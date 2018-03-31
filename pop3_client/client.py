from sys_utils import read_init_file
from services import dispatch


def main():
    while True:
        # Blocking the main process until an action is read
        init_action = read_init_file()
        dispatch(init_action)




if __name__ == '__main__':
    main()
