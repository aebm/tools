#!/usr/bin/env python

import multiprocessing
import os
import subprocess

def write(index):
    path = '/tmp'
    while True:
        subprocess.call(['dd', 'if=/dev/zero', 'of={}'.format(os.path.join(path, str(index))), 'oflag=direct', 'conv=fsync'])

def read(_):
    while True:
        subprocess.call(['dd', 'if=/dev/sda', 'of=/dev/null', 'iflag=direct'])

def main():
    n = 500
    pool1 = multiprocessing.Pool(processes=n)
    pool2 = multiprocessing.Pool(processes=n)
    r1 = pool1.map_async(write, xrange(n), 1)
    r2 = pool2.map_async(read, xrange(n), 1)
    r1.wait()
    r2.wait()


if __name__ == '__main__':
    main()
