from message import Message


def handle_user(msg: str):
    # TODO: Authenticate from Django here
    authenticated = True

    message = 'user accepted'

    if not authenticated:
        message = "authentication failed"

    return Message(success=authenticated, message=message)


def handle_pass(msg: str):
    pass


def handle_list(msg: str):
    pass


def handle_top(msg: str):
    pass


def handle_retr(msg: str):
    pass


def handle_dele(msg: str):
    pass


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
