#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Description
"""

import os
import sys

import pandas as pd


def unpickle_df(filename):
    return pd.read_pickle(f'data/{filename}.pickle')
