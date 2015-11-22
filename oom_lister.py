#!/usr/bin/env python
# List the process ordered by oom score

from __future__ import print_function
import argparse
from codecs import decode
from operator import itemgetter
from os import listdir
from os.path import join
import sys
try:
    from string import maketrans
except ImportError:
    # we are using python3 so this is a str static method
    maketrans = str.maketrans

PROC = '/proc'
SCORE = 'oom_score'
CMD = 'cmdline'
STATUS = 'status'
HEADERS = {
    'pid': 'PID',
    'score': 'SCORE',
    'cmd': 'CMD',
}

def print_vanished(pid):
    print('PID {pid} vanished'.format(pid=pid), file=sys.stderr)

def has_vanished(elem):
    return elem[1] is None or elem[2] is None

def get_decoded_str(s):
    if not isinstance(s, str):
        s = decode(s)
    return s

def get_pid_info(pid):
    thread_cmd = '[{thread_name}]'
    score = None
    cmd = None
    # We don't want exceptions showing up
    try:
        # Had to split the with so it can work with older pythons
        with open(join(PROC, pid, SCORE), 'rb') as f_s:
            with open(join(PROC, pid, CMD), 'rb') as f_cmd:
                score = f_s.readline()
                # decode string so we can use translate string operation
                cmd = get_decoded_str(f_cmd.readline())
            if not cmd:
                # a kernel thread?
                with open(join(PROC, pid, STATUS), 'rb') as f_status:
                    _, thread_name = f_status.readline().rstrip().split()
                    # decode string so we can use translate string operation
                    thread_name = get_decoded_str(thread_name)
                    cmd = thread_cmd.format(thread_name=thread_name)
    except IOError:
        return (int(pid), None, None)
    return (int(pid), int(score), cmd)

def get_lengths(elem):
    pid, score, _ = elem
    return(len(str(pid)), len(str(score)))

def printer(no_headers, pid_length, score_length):
    trans_table = maketrans('\x00', ' ')
    f_str = '{{pid:{pid}}} {{score:{score}}} {{cmd}}'.format(
        pid=pid_length,
        score=score_length)
    def _printer(info):
        try:
            if not no_headers:
                print(f_str.format(**HEADERS))
            for pid, score, cmd in info:
                # change null chars for spaces
                cmd = cmd.translate(trans_table).rstrip()
                print(f_str.format(pid=pid, score=score, cmd=cmd))
        except IOError:
            # If we are printing to a pipe and is closed swallow the exception
            pass
    return _printer

def main():
    parser = argparse.ArgumentParser(
        description='List processes ordered by oom_score')
    parser.add_argument(
        '-v',
        action='store_true',
        help='Verbose mode')
    parser.add_argument(
        '--no-headers',
        action='store_true',
        help='Don\'t print headers')
    args = parser.parse_args()
    if args.v:
        print('Get pids from /proc', file=sys.stderr)
    pids = (pid for pid in listdir(PROC) if pid.isdigit())
    if args.v:
        print('Get info from /proc', file=sys.stderr)
    processes_info = [get_pid_info(pid) for pid in pids]
    del pids
    if args.v:
        print('Removing stale process info', file=sys.stderr)
        [print_vanished(e[0]) for e in processes_info if has_vanished(e)]
    processes_info = [e for e in processes_info if not has_vanished(e)]
    if args.v:
        print('Calculating fields lengths for formatting', file=sys.stderr)
    lengths = []
    if not args.no_headers:
        lengths = [(len(HEADERS['pid']), len(HEADERS['score']))]
    else:
        lengths = [(0, 0)]
    if processes_info:
        lengths.extend([get_lengths(elem) for elem in processes_info])
    # see zip documentation on how to unzip a list
    # https://docs.python.org/3/library/functions.html#zip
    # for each tuple position the max value
    # self trolling ^_^
    max_lengths = map(max, *lengths)
    if args.v:
        print('Lengths are pid: {pid} score: {score}'.format(
            pid=max_lengths[0],
            score=max_lengths[1]),
            file=sys.stderr)
    f_printer = printer(args.no_headers, *max_lengths)
    if args.v:
        print('Printing results', file=sys.stderr)
    f_printer(sorted(processes_info, key=itemgetter(1), reverse=True))

if __name__ == '__main__':
    main()
