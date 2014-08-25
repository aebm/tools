#!/usr/bin/env python
# Delete all logstash indexes older than a given date

from argparse import ArgumentParser
from datetime import date
from itertools import ifilter
from elasticsearch import Elasticsearch

def is_logstash_idx(e):
    return e.startswith('logstash')

def is_older_than(limit_date):
    def _iot(e):
        _, p_date = e.split('-')
        y, m, d = p_date.split('.')
        idx_date = date(year=int(y), month=int(m), day=int(d))
        return idx_date < limit_date
    return _iot

def main():
    parser = ArgumentParser(description=('Delete all the logstash indexes '
        'older than the given date'))
    parser.add_argument('es_server', help='Connection string host:port')
    parser.add_argument('year', type=int)
    parser.add_argument('month', type=int)
    parser.add_argument('day', type=int)
    args = parser.parse_args()
    es = Elasticsearch(args.es_server)
    idx = es.indices
    idx_dict = idx.status().get('indices')
    ls_idx = ifilter(is_logstash_idx, idx_dict.iterkeys())
    to_rm = ifilter(is_older_than(date(year=args.year, month=args.month,
        day=args.day)), ls_idx)
    map(idx.delete, to_rm)

if __name__ == '__main__':
    main()
