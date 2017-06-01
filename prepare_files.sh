#!/bin/bash

./db2csv.py database.db > trams.csv

# We want to leave header at the first line, hence the subshell
(head -n1 trams.csv ; tail -n +2 trams.csv | sort | uniq) > trams.csv.clean
mv trams.csv.clean trams.csv

(echo '"x","y"' ; cut -d ',' -f6,14 tree_groups.csv | tail -n +2) > tree_groups.csv.clean
mv tree_groups.csv.clean tree_groups.csv

