"""
util.py
Functions for loading and processing burrito data
"""

import numpy as np
import scipy as sp
import pandas as pd
import re


def load_burritos(delete_unreliable=True, delete_nonSD=True,
                  delete_extra_columns=True):
    """Load burrito rating data from Google Sheets

    Parameters
    ----------
    delete_unreliable : bool
        if True, delete ratings from the database marked as unreliable
    delete_nonSD : bool
        if True, delete ratings from the database from outside of San Diego
    delete_extra_columns : bool
        if True, remove columns of data that are generally unused

    Returns
    -------
    df : pandas.DataFrame
        information about each burrito consumed
    df_shops : pandas.DataFrame
        information about each taco shop in the database
    df_ingredients : pandas.DataFrame
        information about the ingredients in each burrito in 'df'
    """

    # Load all data
    url = 'https://docs.google.com/spreadsheet/ccc?key=18HkrklYz1bKpDLeL-kaMrGjAhUM6LeJMIACwEljCgaw&output=csv'
    df = pd.read_csv(url)

    # Remove capitalization and excess spaces from location and reviewer
    df.Location = df.Location.str.lower()
    df.Location = df.Location.str.strip()
    df.Reviewer = df.Reviewer.str.strip()

    # Delete unreliable ratings
    if delete_unreliable:
        df = df[(df.Unreliable != 'x') & (df.Unreliable != 'X')]

    # Delete ratings outside of San Diego
    if delete_nonSD:
        df = df[(df.NonSD != 'x') & (df.NonSD != 'X')]

    # Get restaurant info
    i_address = []
    for n in df.index:
        if df.loc[n].Neighborhood is not np.nan:
            i_address.append(n)
    df_shops = df.loc[i_address][['Location', 'Neighborhood',
                                  'Address', 'URL', 'Yelp', 'Google', 'Chips']]

    # Binarize free chips data
    df_shops.Chips = df_shops.Chips.map({'x': True, 'X': True, 1: True})
    df_shops.Chips = df_shops.Chips.fillna(False)

    # Separate ingredient info from burrito info
    df_ingredients = df[df.keys()[np.where(df.keys() == 'Beef')[0][0]:]]
    df = df[df.keys()[:np.where(df.keys() == 'Beef')[0][0]]]
    df = df.drop(['Neighborhood', 'Address', 'URL', 'Yelp',
                  'Google', 'Chips', 'Unreliable', 'NonSD'], axis=1)

    # Ignore rows with no info about the taco shop
    df_shops.dropna(inplace=True)

    return df, df_shops, df_ingredients


def burritotypes(burrito_names, types=None):
    """
    Classify each burrito name into discrete categories

    Parameters
    ----------
    burrito_names : array-like (1d)
        names of each burrito
    types : dict
        keys indicate the burrito category
        values indicate the string needed to be in a burrito name in order to fall in that category

    Returns
    -------
    burrito_category : array-like (1d)
        category of each burrito
    """

    # Determine the categories that burritos can fall into
    if types is None:
        types = {'California': 'cali', 'Carnitas': 'carnita', 'Carne asada': 'carne asada',
                 'Chicken': 'chicken', 'Surf & Turf': 'surf.*turf', 'Adobada': 'adobad', 'Al Pastor': 'pastor'}
    T = len(types)

    # For each burrito name, assign it a category
    categories = types.keys()
    N_burritos = len(burrito_names)
    burrito_category = ['']*N_burritos
    for i, b in enumerate(burrito_names):
        matched = False
        for t in types.keys():
            re4str = re.compile('.*' + types[t] + '.*', re.IGNORECASE)
            if np.logical_and(re4str.match(b) is not None, matched is False):
                burrito_category[i] = t
                matched = True
        if matched is False:
            burrito_category[i] = 'other'
    return burrito_category
