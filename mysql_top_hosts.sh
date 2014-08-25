#!/bin/bash
# List the peers connected to mysql ordered by number of connections, the first argument is used to filter by the especified user
mysqladmin processlist | awk -F '|' "BEGIN { flag = 0 } flag == 1 && /^\|/ && \$3 ~ \"$1\" { split(\$4, conn, \":\"); print conn[1] } /^\|/ && \$3 ~ \"$1\" { flag = 1 }" | sort | uniq -c | sort -nr
