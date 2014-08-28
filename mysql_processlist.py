#!/usr/bin/env python

# Script to find out who is messing with toysql

import csv
import os
import sys
from argparse import ArgumentParser
from datetime import datetime
from time import sleep
import MySQLdb

def main():
    parser = ArgumentParser(description=('Prints in csv format the Mysql '
        'processlist output (with some additives: Ex timestamp) until the '
        'especified file is created or after the number of iterations given '
        'is reached'))
    parser.add_argument('file', help='file that will stop script execution')
    parser.add_argument('--user', default='root',
        help='MySQL user, defaults to root')
    parser.add_argument('--password', default= '',
        help='MySQL password, defaults to empty string')
    parser.add_argument('--host', default='127.0.0.1',
        help='MySQL host, defaults to 127.0.0.1')
    parser.add_argument('--sleep', default=0, type=float,
        help='seconds to sleep between queries, defaults to 0')
    parser.add_argument('--iterations', default=0, type=int,
        help='iterations to run, defaults to 0 (0 == nolimit)')
    args = parser.parse_args()
    csv_fields = ['TIMESTAMP']
    sql_fields = ['ID', 'USER', 'HOST', 'DB',
        'COMMAND', 'TIME', 'STATE', 'INFO']
    csv_fields.extend(sql_fields[:3])
    csv_fields.extend(['PORT'])
    csv_fields.extend(sql_fields[3:])
    db = MySQLdb.connect(host=args.host, user=args.user, passwd=args.password)
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    writer = csv.DictWriter(sys.stdout, csv_fields)
    try:
        writer.writeheader()
    except AttributeError:
        # Python older than 2.7
        header = dict((r, r) for r in csv_fields)
        writer.writerow(header)
    counter = 0
    while (not os.access(args.file, os.F_OK)
        and not (args.iterations > 0 and counter >= args.iterations)):
        timestamp = str(datetime.now())
        cur.execute('SELECT {0} FROM INFORMATION_SCHEMA.PROCESSLIST'.format(
            ','.join(sql_fields)))
        for row in cur:
            try:
                row['HOST'], row['PORT'] = row['HOST'].split(':') # split host port
            except ValueError:
                # Doesn't have a port
                row['PORT'] = ''
            row['TIMESTAMP'] = timestamp
            writer.writerow(row)
        counter += 1
        if args.sleep > 0:
            sleep(args.sleep)
    if cur:
        cur.close()
    if db:
        db.close()

if __name__ == '__main__':
    main()
