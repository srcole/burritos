# coding: utf-8
# Prepare spreadsheet that contains geographical locations and
# average burrito statistics for each taco shop

import numpy as np
import scipy as sp
import pandas as pd
import geocoder
import util

# Load data
df, dfRestaurants, _ = util.load_burritos()

# Process restaurant data
dfRestaurants = dfRestaurants.reset_index().drop('index', axis=1)

# Compute average feature values for each restaurant
dfAvg = df.groupby('Location').agg({'Cost': np.mean, 'Volume': np.mean, 'Hunger': np.mean,
                                    'Tortilla': np.mean, 'Temp': np.mean, 'Meat': np.mean,
                                    'Fillings': np.mean, 'Meat:filling': np.mean, 'Uniformity': np.mean,
                                    'Salsa': np.mean, 'Synergy': np.mean, 'Wrap': np.mean,
                                    'overall': np.mean, 'Location': np.size})
dfAvg.rename(columns={'Location': 'N'}, inplace=True)
dfAvg['Location'] = list(dfAvg.index)

# Calculate latitutude and longitude for each city
addresses = dfRestaurants['Address'] + ', ' + \
    dfRestaurants['Neighborhood'] + ', San Diego, CA'
lats = np.zeros(len(addresses))
longs = np.zeros(len(addresses))
for i, address in enumerate(addresses):
    g = geocoder.google(address)
    Ntries = 1
    while g.latlng == []:
        g = geocoder.google(address)
        Ntries += 1
        print('try again: ' + address)
        if Ntries >= 5:
            if 'Marshall College' in address:
                address = '9500 Gilman Drive, La Jolla, CA'
                g = geocoder.google(address)
                Ntries = 1
                while g.latlng == []:
                    g = geocoder.google(address)
                    Ntries += 1
                    print('try again: ' + address)
                    if Ntries >= 5:
                        raise ValueError('Address not found: ' + address)
            else:
                raise ValueError('Address not found: ' + address)
    lats[i], longs[i] = g.latlng

# Check for nonsense lats and longs
if sum(np.logical_or(lats > 34, lats < 32)):
    raise ValueError('Address not in san diego')
if sum(np.logical_or(longs < -118, longs > -117)):
    raise ValueError('Address not in san diego')

# Incorporate lats and longs into restaurants data
dfRestaurants['Latitude'] = lats
dfRestaurants['Longitude'] = longs

# Merge restaurant data with burrito data and save to csv
dfTableau = pd.merge(dfRestaurants, dfAvg, on='Location')
dfTableau.to_csv('df_burrito_tableau.csv')
