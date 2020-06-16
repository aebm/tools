#!/usr/bin/env python3

import argparse
import socket

def parse_args():
    parser = argparse.ArgumentParser(description='TCP PONG server')
    parser.add_argument('--ip', default='0.0.0.0', type=str, help='IP to bind to. Default: 0.0.0.0')
    parser.add_argument('--port', default=1666, type=int, help='port to bind to. Default: 1666')
    return parser.parse_args()

def main():
    args = parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (args.ip, args.port)

    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    sock.listen(1)

    while True:
        print('Waiting for connection')
        connection, client_address = sock.accept()
        try:
            print('Connection from: ', client_address)

            while True:
                data = connection.recv(64)
                print('received {}'.format(data))
                if data:
                    print('send pong')
                    connection.sendall(b'PONG')
                else:
                    print('no data from: ', client_address)
                    break
        finally:
            connection.close()

if __name__ == '__main__':
    main()
