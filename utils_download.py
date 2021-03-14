#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities to download, extract, pickle and unpickle compressed IMDB datasets

Data source: https://datasets.imdbws.com/
"""

import gzip
import pandas as pd
import requests

from pathlib import Path


def download_dataset(url, filename):
    print(f"Downloading {url}...")
    with requests.Session() as session:
        ret = session.get(url)
        with open(f'data/{filename}.tsv.gz', 'wb') as fp:
            fp.write(ret.content)
    print("Done!")


def unzip_dataset(filename):
    print(f"Extracting {filename}.tsv...")
    with gzip.open(f'data/{filename}.tsv.gz', 'rb') as gz, open(f'data/{filename}.tsv', 'wb') as fp:
        fp.write(gz.read())
    print("Done!")


def pickle_pd_dataframe(filename):
    df = pd.read_csv(f'data/{filename}.tsv', delimiter='\t', na_values=r'\N', dtype='object')
    if 'tconst' in df.columns:
        df.set_index('tconst', inplace=True)
    elif 'nconst' in df.columns:
        df.set_index('nconst', inplace=True)
    df.to_pickle(f'data/{filename}.pickle')


def get_url(filename):
    return f'https://datasets.imdbws.com/{filename}.tsv.gz'


def get_dataset_size(url):
    with requests.Session() as session:
        return session.get(url, stream=True).headers['Content-length']


def check_data():
    datasets = {'title.basics': {}, 'title.crew': {}, 'title.principals': {}, 'name.basics': {}}

    needed = outdated = 0
    datasets_to_download = []
    for kk, vv in datasets.items():
        if Path(f'data/{kk}.tsv.gz').exists():
            vv['localsize'] = float(Path(f'data/{kk}.tsv.gz').stat().st_size) / 1048576
        else:
            vv['localsize'] = 0
        vv['onlinesize'] = float(get_dataset_size(get_url(kk))) / 1048576
        if not vv['localsize']:
            needed += vv['onlinesize']
            datasets_to_download.append(kk)
        elif vv['localsize'] < vv['onlinesize']:
            outdated += vv['onlinesize']
            datasets_to_download.append(kk)
    if needed:
        print(f'Some datasets are missing, need to download {needed:.2f} MB')
    if outdated:
        print(f'Some datasets are out-of date, need to download {outdated:.2f} MB')
    if needed or outdated:
        print(f"Continue and download {outdated+needed:.2f} MB? (Y/n)")
        ans = input().lower()
        if ans == 'y' or ans == '':
            for kk in datasets_to_download:
                download_dataset(get_url(kk), kk)
                unzip_dataset(kk)
                pickle_pd_dataframe(kk)