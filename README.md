tools
=====

Compilation of tools of the trade

* **diamond.py:** Short script to remember the python version of perl's diamond operator
* **es_cleaner.py:** Delete logstash indexes older than a given date from elasticsearch (See also: https://github.com/elasticsearch/curator)
* **es_janitor.py:** Delete logstash indexes older than N days from now from elasticsearch (this is for using in  cronjobs)
* **es_list_indexes.py:** List elasticsearch indexes
* **mysql_count_conns.sh:** Print the number of mysql connections opened
* **mysql_top_hosts.sh:** List number of mysql connections by hosts (Run on the server)
* **mysql_top_users.sh:** List number of mysql connections by users (Run on the server)
* **oom_lister.py:** List process ordered by oom score
* **utf8_checker.py:** Checks if a list of files is utf-8 encoded
* **mysql_processlist.py:** Prints to stdout as csv the output of mysql processlist command until a number of iterations is reached or a especified file is created
* **killer.c:** Launch N process that runs hdparm. This is a work in progress
* **punisher.py:** Program to saturate IO WIP
* **godmode.c:** Sleep a lot of seconds and ignore all the signals ignorable
* **delta_printer.py:** Print the time deltas between to log entries (the input needs to be filtered to only have start and end entries)
* **get_gh_org_repos.sh:** Get a JSON with the organization repos
* **image_in_dockerhub.sh:** Check if a image is in dockerhub

To compile
----------
```bash
cc -Wall -o executable executable.c
``` 
