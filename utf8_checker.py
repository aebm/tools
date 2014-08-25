#!/usr/bin/env python
# Check if a list of files is utf-8 encoded

import codecs
from itertools import imap
from operator import or_
import sys

def check_file(filename):
    error = False
    with codecs.open(filename, encoding='utf-8') as f:
        c = 1
        try:
            for line in f:
                c += 1
        except UnicodeDecodeError as e:
            error = True
            print(('Invalid file: {filename} at line: {n_l} '
                'with error: {e}').format(filename=filename, n_l=c, e=str(e)))
    return error

def main():
    if len(sys.argv) < 2:
        print('Give me filenames!!!')
        sys.exit(1)
    if reduce(or_, imap(check_file, sys.argv[1:]), False):
        sys.exit(1)

if __name__ == '__main__':
    main()
