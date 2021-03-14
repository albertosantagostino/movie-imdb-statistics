#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IMDB Statistics and graphs generator
"""

import pandas as pd

from utils_download import check_data
from utils import unpickle_df

import plotly.graph_objects as go

import ipdb


def main():
    """Entrypoint"""

    # Uncomment to download most recent data
    # check_data()

    entries = unpickle_df('title.basics')
    movies = entries.loc[(entries['titleType'] == 'movie')
                         & (entries['isAdult'] == '0')].drop(columns=['titleType', 'endYear', 'isAdult'])
    nm = len(movies)
    print(f"{(nm)} movies loaded")

    #pd.set_option('display.max_rows', None)

    # Statistics
    mdt = sum(movies['primaryTitle'] != movies['originalTitle'])
    # TODO: Time vs mdt = movies.loc[movies['primaryTitle'] != movies['originalTitle']]
    print(f"{mdt} movies ({mdt*100/nm:.2f}%) have a primaryTitle different from the originalTitle")

    mon = sum(movies['primaryTitle'].str.contains(r'^[+-]?\d*\.?\d+$'))
    print(f"{mon} movies ({mon*100/nm:.2f}%) have only digits as primaryTitle")

    movies_with_numbers = movies.loc[movies['primaryTitle'].str.contains(r'.*[0-9].*')]
    mwn = len(movies_with_numbers)
    print(f"{mwn} movies ({mwn*100/nm:.2f}%) contain at least one number in the primaryTitle")

    mp2 = sum(movies['primaryTitle'].str.endswith(' 2') | movies['primaryTitle'].str.endswith(' II')
              | movies['primaryTitle'].str.contains(r'\W[2|I]I?[:|-|\s-]\W.*'))
    print(f"{mp2} movies ({mp2*100/nm:.2f}%) have a primaryTitle that indicates it's a second part")

    ipdb.set_trace()

    # Graphs / Plots
    entries_by_type = {}
    for entry_type in entries['titleType'].unique():
        if (nn := sum(entries['titleType'] == entry_type)) > 100:
            entries_by_type[entry_type] = nn
    fig_entries_by_type = go.Figure(
        data=[go.Pie(labels=[*entries_by_type.keys()], values=[*entries_by_type.values()], textfont_size=20)])

    ipdb.set_trace()


if __name__ == '__main__':
    main()