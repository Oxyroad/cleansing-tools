#!/usr/bin/env python3

import json
import sqlite3
import sys


class Entry:
    header = '"x","y","line"'

    def __init__(self, x, y, line):
        self.x = float(x)
        self.y = float(y)
        self.line = int(line)

    def __str__(self):
        return '{},{},{}'.format(self.x, self.y, self.line)


def string_to_Entries(raw):
    entries = list()
    try:
        result = json.loads(raw)['result']
        for line in result:
            lon = line['Lon']
            lat = line['Lat']
            tram_lines = line['Lines'].strip()
            for tram_line in tram_lines.split(','):
                tram_line = tram_line.strip()
                entries.append(Entry(lon, lat, tram_line))
    except Exception:
        pass  # invalid response, ignore
    return entries


def sqlite_to_Entries(filename):
    cursor = sqlite3.connect(filename).cursor()
    cursor.execute('select dump from tramwaje')
    entries = list()
    for row in cursor.fetchall():
        entries.extend(string_to_Entries(row[0]))
    return entries


def usage():
    return '{} SQLITE_DB'.format(sys.argv[0])


def is_tram_filter(entry):
    return entry.line != 'M'


def is_in_Warsaw_filter(entry):
    return 20 < entry.x < 21 and 51 < entry.y < 53


def is_typical_line_filter(entry):
    return entry.line < 50


def main():
    if len(sys.argv) != 2:
        print(usage())
        sys.exit(1)

    entries = sqlite_to_Entries(sys.argv[1])
    print(Entry.header)
    for entry in entries:
        if is_tram_filter(entry):
            if is_in_Warsaw_filter(entry):
                if is_typical_line_filter(entry):
                    print(entry)


if __name__ == '__main__':
    main()
