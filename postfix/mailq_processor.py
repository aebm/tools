import csv
import fileinput
import re
import sys

def main():
    pattern = 'NOQUEUE: .+? from=(?P<from>\S*) to=(?P<to>\S*) .+? helo=(?P<helo>\S*)'
    prog = re.compile(pattern)
    csv_w = csv.writer(sys.stdout)
    csv_w.writerow(['from', 'to'])
    from_f = None
    to_f = None
    for line in fileinput.input():
        line = line.rstrip()
        if len(line) == 0:
            # skip empty line
            continue
        if line[0] == '-':
            continue
        if line[0] == '(':
            # skip reason
            continue
        if line[0] != ' ':
            # it is a sender 
            from_f = line.rsplit(None, 1)[-1]
            # reset 'to field'
            to_f = None
        else:
            line = line.lstrip()
            if line[0] == '(':
                # skip reason
                continue
            # it is a receipment
            to_f = line
        if from_f and to_f:
            pass
            csv_w.writerow([from_f, to_f])

if __name__ == '__main__':
    main()
