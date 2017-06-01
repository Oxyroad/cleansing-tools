#!/bin/bash

./db2csv.py database.db > trams_with_duplicates.csv

# We want to leave header at the first line, hence the subshell
(head -n1 trams_with_duplicates.csv ; tail -n +2 trams_with_duplicates.csv | sort | uniq) > trams.csv
rm trams_with_duplicates.csv
