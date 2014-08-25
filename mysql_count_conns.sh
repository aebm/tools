#!/bin/bash
# Print the how many connections open has mysql

mysqladmin processlist | awk  'BEGIN { count = -1 } /^\|/ { count++ } END { print count }'
