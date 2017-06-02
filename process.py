#!/usr/bin/env python3

from collections import namedtuple
import json

import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

from const import line_to_length
from ztm2line_coords import line_to_coords

RADIUS = 0.0004
GREEN_SAMPLE_FRAC = 1
TRAM_SAMPLE_FRAC = 0.01
JSON_GREEN_SAMPLE_FRAC = 1

RGB = namedtuple('RGB', ['r', 'g', 'b'])

COLOR1 = RGB(255, 0, 0)
COLOR2 = RGB(0, 255, 0)


def blend_colors(color1, color2, how_much):
    """
    Choose color between color1 and color2.

    For how_much equal 0, return color1.
    For how_much equal 1, return color2.
    For how_much between 0 and 1, blend colors.

    :param color1: RGB, first color
    :param color2: RGB, second color
    :param how_much: float between 0 and 1 (inclusive)
    :returns: RGB
    """
    if how_much < 0 or 1 < how_much:
        raise TypeError
    r = int(((1 - how_much) * color1.r**2 + how_much * color2.r**2)**0.5)
    g = int(((1 - how_much) * color1.g**2 + how_much * color2.g**2)**0.5)
    b = int(((1 - how_much) * color1.b**2 + how_much * color2.b**2)**0.5)
    return RGB(r, g, b)


trams = pd.read_csv('trams.csv', dtype={'x': float, 'y': float, 'line': int})

tree_groups = pd.read_csv(
    'tree_groups.csv',
    usecols=['x_wgs84', 'y_wgs84'],
    dtype={'x_wgs84': float, 'y_wgs84': float}
)
tree_groups.rename(columns={'x_wgs84': 'x', 'y_wgs84': 'y'}, inplace=True)

# it's not a typo, one column is ill-named
trees = pd.read_csv(
    'trees.csv',
    usecols=['﻿x_wgs84', 'y_wgs84'],
    dtype={'﻿x_wgs84': float, 'y_wgs84': float}
)
trees.rename(columns={'﻿x_wgs84': 'x', 'y_wgs84': 'y'}, inplace=True)

greens = pd.concat([tree_groups, trees]).sample(frac=GREEN_SAMPLE_FRAC)

line_to_details = dict()
for t in trams.groupby('line'):
    line = t[0]
    df = t[1].loc[:, ['x', 'y']].sample(frac=TRAM_SAMPLE_FRAC)
    close_points = cdist(df, greens.loc[:, ['x', 'y']]) <= RADIUS
    close_greens_indices = np.any(close_points, axis=0)
    close_greens_count = np.sum(close_greens_indices)
    close_greens = greens.loc[close_greens_indices, :]
    green_index = close_greens_count/line_to_length[line]
    '''
    print('Line {} has got {} green-likes around. Green index: {}.'.format(
        line, close_greens_count, green_index
    ))
    '''
    green_waypoints = list()
    for _, row in close_greens.sample(frac=JSON_GREEN_SAMPLE_FRAC).iterrows():
        green_waypoints.append({'lng': row[0], 'lat': row[1]})
    route = line_to_coords[line]
    line_to_details[str(line)] = {
        'color': None,
        'green_index': green_index,
        'green_index_normalized': None,
        'green_waypoints': green_waypoints,
        'route': route,
    }

best_green_index = max(d['green_index'] for d in line_to_details.values())

for line, d in line_to_details.items():
    d['green_index_normalized'] = d['green_index'] / best_green_index
    d['color'] = blend_colors(COLOR1, COLOR2, d['green_index_normalized'])

print(json.dumps(line_to_details))
