'''
This Python notebook file is used to process data from the Canada dataset
and create a series of immigration models to be used by our virtual countries.
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# remove pd indexing warning
pd.options.mode.chained_assignment = None  

# read Excel file and store into a dataframe
df = pd.read_excel('Canada.xlsx',
                   sheet_name='Canada by Citizenship',
                   skiprows=range(20),
                   skipfooter=2)

# fill list of columns with every year in the dataset
columns = ['OdName']
for year in range(1980, 2014):
    columns.append(year)
df = df.filter(columns)

'''
dictionary of populations for each country we will be use, using 2004 data (in millions)

The 4 archetypes:
C1 = resource-rich, dense
C2 = resource-rich, sparse
C3 = resource-poor, dense
C4 = resource-poor, sparse
'''
populations = {
    "Singapore": ('C1', 4.167),
    "Netherlands": ('C1', 16.26),
    "United Kingdom": ('C1', 59.79),
    "Australia": ('C2', 20.13),
    "Sweden": ('C2', 8.976),
    "United States": ('C2', 292.8),
    "Lebanon": ('C3', 4.569),
    "India": ('C3', 1131),
    "Philippines": ('C3', 84.71),
    "Libya": ('C4', 5.71),
    "Bolivia": ('C4', 9.069),
    "Iran": ('C4', 68.95)
}

# create a dataframe of all 16 countries and immigration rates per million people
countries_df = pd.DataFrame()
for country in populations:
    archetype = populations[country][0]
    population = populations[country][1]

    country_df = df.loc[df["OdName"] == country]
    country_df['Arch'] = archetype
    for year in range(1980, 2014):

        # store immigration rate per million in population
        country_df[year] /= population

    countries_df = countries_df.append(country_df)

# create a more vertical dataframe where each row has a separate year
# intended to make it easier to fit into the model
countries = populations.keys()
df_collection = {}
for country in countries:
    country_df = pd.DataFrame(columns=['Year', 'Immigration'])
    for year in range(1980, 2014):
        year_df = pd.DataFrame({
            "Year": [year],
            "Immigration": countries_df[countries_df["OdName"] == country][year]
        })
        country_df = country_df.append(year_df, ignore_index=True)
    df_collection[country] = country_df

# create a dictionary of polynomial regression models for all 16 countries
models = {}
for country in df_collection:
    country_df = df_collection[country]
    x = country_df["Year"].astype("int")
    y = country_df["Immigration"].astype("float")

    # fit model with 5th-degree polynomial regression
    model = np.poly1d(np.polyfit(x, y, 5))
    models[country] = model