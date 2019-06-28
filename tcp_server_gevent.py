import gevent
from gevent import socket


def server():
    ip_port = ('', 9999)

    server_socket = socket.socket()
    server_socket.bind(ip_port)
    server_socket.listen(5)
    try:
        while True:
            client_socket, client_addr = server_socket.accept()
            print('{} connected!'.format(client_addr))
            gevent.spawn(handle_client, client_socket, client_addr)
    finally:
        server_socket.close()


def handle_client(client_socket, client_addr):
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if data:
                print('{}: {}'.format(client_addr, data))
                client_socket.send('Recv: {}'.format(data).encode())
            else:
                print('{} closed!'.format(client_addr))
                break
    except:
        client_socket.close()
        print('{} closed!'.format(client_addr))


if __name__ == '__main__':
    server()
