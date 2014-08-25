#!/usr/bin/env python
# Delete the logstash indexes older than N days from today

from argparse import ArgumentParser
from datetime import date, timedelta
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
        'older than N days from now'))
    parser.add_argument('es_server', help='Connection string host:port')
    parser.add_argument('days', type=int, help='Days to keep before today')
    args = parser.parse_args()
    es = Elasticsearch(args.es_server)
    idx = es.indices
    idx_dict = idx.status().get('indices')
    ls_idx = ifilter(is_logstash_idx, idx_dict.iterkeys())
    today = date.today() 
    days = abs(args.days)
    limit = today - timedelta(days)
    to_rm = ifilter(is_older_than(limit), ls_idx)
    map(idx.delete, to_rm)

if __name__ == '__main__':
    main()
