#!/usr/bin/env python3

import argparse
import socket
import time

def parse_args():
    parser = argparse.ArgumentParser(description='TCP PING client')
    parser.add_argument('dest', default='0.0.0.0', type=str, help='Dest to connect')
    parser.add_argument('port', type=int, help='port to connect to.')
    parser.add_argument('seconds', type=int, help='seconds to sleep between messages')
    return parser.parse_args()

def main():
    args = parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (args.dest, args.port)
    print('Connectiong to {} port {}'.format(*server_address))

    sock.connect(server_address)

    sleep_sec = args.seconds

    try:
        while True:
            message = b'PING'
            print('sending {}'.format(message))
            sock.sendall(message)
    
            amount_received = 0
            amount_expected = len(b'PONG')
    
            while amount_received < amount_expected:
                data = sock.recv(16)
                amount_received += len(data)
                print('received {}'.format(data))
                if not data:
                    break
    
            print('Sleep {}s'.format(sleep_sec))
            time.sleep(sleep_sec)
    
    finally:
        print('Closing socket')
        sock.close()

if __name__ == '__main__':
    main()
