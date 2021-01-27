#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Description
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

    fig_pie = go.Figure(data=[go.Pie(labels=['a','b'], values=[20,80])])
    ipdb.set_trace()

    entries = unpickle_df('title.basics')

    movies = entries.loc[(entries['titleType'] == 'movie') & (entries['isAdult'] == '0')]
    pd.set_option('display.max_rows', None)
    movies = movies.drop(columns=['titleType', 'endYear', 'isAdult'])
    print(f"{len(movies)} movies found")

    



    mdt = movies.loc[movies['primaryTitle'] != movies['originalTitle']]
    print(f"{len(mdt)} movies ({len(mdt)*100/len(movies):.2f}%) have a primaryTitle different from the originalTitle")
    mon = movies.loc[movies['primaryTitle'].str.contains(r'^[+-]?\d*\.?\d+$')]
    print(f"{len(mon)} movies ({len(mon)*100/len(movies):.2f}%) have only digits as primaryTitle")
    mwn = movies.loc[movies['primaryTitle'].str.contains(r'.*[0-9].*')]
    print(f"{len(mwn)} movies ({len(mwn)*100/len(movies):.2f}%) contain at least one number in the primaryTitle")
    mp2 = movies.loc[(movies['primaryTitle'].str.endswith(' 2')) | (movies['primaryTitle'].str.endswith(' II')) |
                     (movies['primaryTitle'].str.contains(r'\W[2|I]I?[:|-|\s-]\W.*'))]
    print(f"{len(mp2)} movies ({len(mp2)*100/len(movies):.2f}%) have a primaryTitle that indicates it's a second part")
    ipdb.set_trace()


if __name__ == '__main__':
    main()