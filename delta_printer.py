#!/usr/bin/env python

import datetime
import fileinput
import re

def get_datetime(s):
    t = s.split()
    return datetime.datetime.strptime(' '.join(t[:2]), '%Y-%m-%d %H:%M:%S,%f')
    
prog = re.compile('end:')

begin = None
end = None

for line in fileinput.input():
    line = line.rstrip()
    if prog.search(line):
        # END
        if begin is None:
            # no matching begin
            continue
        end = get_datetime(line)
        delta = end - begin
        begin = None
        print(delta.total_seconds())
    else:
        # BEGIN
        begin = get_datetime(line)
