from ztm_scraper import line_to_last_stops

import pandas as pd

line_to_coords = dict()


def format_coords(x, y):
    return {'lng': x, 'lat': y}


stations = pd.read_csv('stations.csv', converters={'lines': lambda x: x.split('|')})
for line, last_stops in line_to_last_stops.items():
    start, end = last_stops
    first = stations.loc[(stations.name.str.lower() == start.lower()) & stations.apply(lambda x: str(line) in x.lines, axis=1)].iloc[0]
    last = stations.loc[(stations.name.str.lower() == end.lower()) & stations.apply(lambda x: str(line) in x.lines, axis=1)].iloc[0]
    line_stations = stations.loc[stations.apply(lambda x: str(1) in x.lines, axis=1)].sample(2)
    line_stations = [format_coords(x[1].x, x[1].y) for x in line_stations.iterrows()]
    result = [format_coords(first.x, first.y)] + line_stations + [format_coords(last.x, last.y)]
    line_to_coords[line] = result
