#!/bin/bash
# List the users connected to mysql ordered by number of connections
mysqladmin processlist | awk -F '|' 'BEGIN { flag = 0 }  flag == 1 && /^\|/ { print $3 } /^\|/ { flag = 1 }' | sort | uniq -c | sort -nr
