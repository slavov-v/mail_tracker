import socket

from services import dispatch

HOST = 'localhost'
PORT = 50007


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))

    while True:
        s.listen(1)

        connection, address = s.accept()

        with connection:
            message = connection.recv(1024)
            if not message:
                return

            print(message)

            result = dispatch(message)
            connection.sendall(str(result).encode('utf-8'))


if __name__ == '__main__':
    print(f'POP3 processor running on {HOST}:{PORT}')
    main()
