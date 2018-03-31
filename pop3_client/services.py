def handle_user(user_id: str):
    pass


def handle_pass(password: str):
    pass


def handle_list():
    pass


def handle_top(msg_id: int):
    pass


def handle_retr(msg_id: int):
    pass


def handle_dele(msg_id: int):
    pass


dispatcher = {
    'USER': handle_user,
    'PASS': handle_pass,
    'LIST': handle_list,
    'RETR': handle_retr,
    'DELE': handle_dele
}
