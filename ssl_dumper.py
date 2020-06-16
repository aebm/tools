#!/usr/bin/env python3

import argparse
import collections
import subprocess
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='Find and show certificate data')
    parser.add_argument('path', type=str, help='path to search for certificates')
    return parser.parse_args()

def run_grep(path):
    cmd = [ 'grep',
            '-lRIF',
            'BEGIN CERTIFICATE',
    ]
    cmd.append(path)
    print('Run: {}'.format(' '.join(cmd)), file=sys.stderr)
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        print('egrep returned: {}'.format(r.returncode), file=sys.stderr)
    return [ e for e in r.stdout.decode('utf-8').split('\n') if e ]

def get_sums(files):
    ans = []
    for fname in files:
        r = subprocess.run(['md5sum', fname], capture_output=True)
        if r.returncode != 0:
            print('error running: md5sum {}'.format(fname), file=sys.stderr)
            continue
        ans.append((r.stdout.decode('utf-8').split()[0], fname))
    return ans

def group_by_digest(list_):
    d = collections.defaultdict(list)
    for digest, filename in list_:
        d[digest].append(filename)
    return d

def _parse_openssl_data(lines):
    d = {}
    for line in lines:
        key, data = line.split('=', maxsplit=1)
        d[key] = data
    return d

def get_openssl_data(filename):
    cmd = [
            'openssl',
            'x509',
            '-in',
            filename,
            '-noout',
            '-issuer',
            '-subject',
            '-dates',
    ]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        print('{} returned: {}'.format(' '.join(cmd), r.returncode), file=sys.stderr)
        return None
    lines = [ l for l in r.stdout.decode('utf8').split('\n') if l ]
    return _parse_openssl_data(lines)

def process_grouped(grouped):
    for digest, values in grouped.items():
        cert_data = get_openssl_data(values[0])
        if cert_data is not None:
            print()
            print('HASH: {}'.format(digest))
            print('ISSUER: {}'.format(cert_data['issuer']))
            print('SUBJECT: {}'.format(cert_data['subject']))
            print('START: {}'.format(cert_data['notBefore']))
            print('END: {}'.format(cert_data['notAfter']))
            print('FILES:')
            for v in values:
                print('  {}'.format(v))

def main():
    args = parse_args()
    files = run_grep(args.path)
    digest_files = get_sums(files)
    del files
    grouped = group_by_digest(digest_files)
    del digest_files
    process_grouped(grouped)

if __name__ == '__main__':
    main()
