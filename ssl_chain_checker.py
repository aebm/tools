#!/usr/bin/env python3

import argparse
import datetime
import re
import subprocess
import sys

def get_cert_chain_from(filename):
    begin_regex = r'^-+?BEGIN CERTIFICATE-+\n$'
    end_regex = r'^-+?END CERTIFICATE-+\n?$'
    chain = []
    try:
        with open(filename, 'rb') as f:
            begin_seen = False
            for line in f:
                tline = line.decode()
                if begin_seen:
                    cert.append(line)
                    r = re.fullmatch(end_regex, tline)
                    if r is not None:
                        begin_seen = False
                        chain.append(cert)
                else:
                    r = re.fullmatch(begin_regex, tline)
                    if r is not None:
                        begin_seen = True
                        cert = [line]
    except Exception as e:
        print('When processing: {}, returned: {}'.format(filename, e), file=sys.stderr)
    return chain

def _parse_openssl_data(lines):
    d = {}
    for line in lines:
        key, data = line.split('=', maxsplit=1)
        d[key] = data
    return d

def get_openssl_data(cert):
    cmd = [
            'openssl',
            'x509',
            '-nameopt',
            'RFC2253',
            '-noout',
            '-issuer',
            '-subject',
            '-dates',
    ]
    r = subprocess.run(cmd, input=b''.join(cert), capture_output=True)
    if r.returncode != 0:
        print('{} returned: {}'.format(' '.join(cmd), r.returncode), file=sys.stderr)
        return _parse_openssl_data([])
    lines = [ l for l in r.stdout.decode('utf8').split('\n') if l ]
    return _parse_openssl_data(lines)

def print_openssl_data(cert):
    timeformat = '%b %d %H:%M:%S %Y %Z'
    expired = 'YES'
    if len(cert) == 0:
        return
    now = datetime.datetime.utcnow()
    not_before = datetime.datetime.strptime(cert['notBefore'], timeformat)
    not_after = datetime.datetime.strptime(cert['notAfter'], timeformat)
    if not_before < now and now < not_after:
        expired = 'NO'
    print('Expired:', expired)
    print('Issuer:', cert['issuer'])
    print('Subject:', cert['subject'])
    print('Not before:', cert['notBefore'])
    print('Not after:', cert['notAfter'])
    print()
 
def main():
    parser = argparse.ArgumentParser(description='Print certificate chain and check if it is expired.')
    parser.add_argument('certs', nargs='+', metavar='certificate', help='cert file to check')
    args = parser.parse_args()
    for f in args.certs:
        chain = get_cert_chain_from(f)
        if chain:
            print('chain for {}\n'.format(f))
        for cert in reversed(chain):
            print_openssl_data(get_openssl_data(cert))

if __name__ == '__main__':
    main()
