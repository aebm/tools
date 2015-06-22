import collections
import csv
import fileinput
import re
import sys

def none_translator(elem):
    if elem is None:
        return ''
    return elem

def main():
    pattern = 'postfix/(?:smtpd|qmgr|local|smtp|error)\[\d+?\]:\s(?P<id>\w+?):'
    prog = re.compile(pattern)
    kv_pattern = '^(?P<key>.+?)=<?(?P<value>.*?)>?,?$'
    kv_prog = re.compile(kv_pattern)
    csv_w = csv.writer(sys.stdout)
    headers = ['id', 'status', 'from', 'orig_to', 'to', 'helo', 'client', 'relay', 'sasl_method', 'sasl_username', 'sasl_sender']
    csv_w.writerow(headers)
    noqueue = list()
    keys = set(headers)
    data = collections.defaultdict(dict)
    for line in fileinput.input():
        line = line.rstrip()
        mobj = prog.search(line)
        if mobj is None:
            continue
        msg_id = mobj.group('id')
        if msg_id == 'warning':
            continue
        if msg_id == 'NOQUEUE':
            d = dict()
        else:
            d = data[msg_id]
        for elem in line.split():
            mobj = kv_prog.match(elem)
            if mobj is None:
                continue
            k = mobj.group('key')
            v = mobj.group('value')
            if k not in keys:
                continue
            d[k] = v
            if k == 'helo':
                d['status'] = 'rejected'
        if msg_id == 'NOQUEUE':
            noqueue.append(d)
    for k, v in data.iteritems():
        row = [k]
        for header in headers[1:]:
            row.append(v.get(header, 'N/A'))
        csv_w.writerow(row)
    for elem in noqueue:
        row = ['noqueue']
        for header in headers[1:]:
            row.append(elem.get(header, 'N/A'))
        csv_w.writerow(row)

if __name__ == '__main__':
    main()
