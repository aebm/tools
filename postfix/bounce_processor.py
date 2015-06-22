import csv
import fileinput
import re
import sys

def main():
    pattern = 'NOQUEUE: .+? from=(?P<from>\S*) to=(?P<to>\S*) .+? helo=(?P<helo>\S*)'
    prog = re.compile(pattern)
    csv_w = csv.writer(sys.stdout)
    csv_w.writerow(['from', 'to', 'helo'])
    for line in fileinput.input():
        mobj = prog.search(line)
        if mobj:
            csv_w.writerow([mobj.group('from'), mobj.group('to'), mobj.group('helo')])

if __name__ == '__main__':
    main()
