#!/usr/bin/env python
# List all th elasticsearch indexes

from argparse import ArgumentParser
from elasticsearch import Elasticsearch

def main():
    parser = ArgumentParser(description='List all the elasticsearch indexes')
    parser.add_argument('es_server', help='Connection string host:port')
    args = parser.parse_args()
    es = Elasticsearch(args.es_server)
    idx = es.indices
    idx_dict = idx.status().get('indices')
    print('\n'.join(idx_dict.keys()))

if __name__ == '__main__':
    main()
