#!/usr/bin/env python
# coding: utf-8

# In[1]:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


# In[2]:


pd.options.mode.chained_assignment = None  # remove pd indexing warning


# In[3]:


df = pd.read_excel('../datasets/Canada.xlsx',
                   sheet_name='Canada by Citizenship',
                   skiprows=range(20),
                   skipfooter=2)


# In[4]:


columns = ['OdName']
for year in range(1980, 2014):
    columns.append(year)
df = df.filter(columns)


# In[5]:


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


# In[6]:


'''
Plan: 

Use supervised learning to predict immigration levels into Atlantis

Have 2 developed countries: Atlantis & 
Other 3 countries are developing

We need a system using our current interfaces to build a turn-based game

Need a way to implement part 1 into an instance of a player, and also
include a game manager.
'''


# In[7]:


countries_df = pd.DataFrame()


# In[8]:


for country in populations:
    archetype = populations[country][0]
    population = populations[country][1]

    country_df = df.loc[df["OdName"] == country]
    country_df['Arch'] = archetype
    for year in range(1980, 2014):
        country_df[year] /= population

    countries_df = countries_df.append(country_df)


# In[9]:


# Instead of 16 countries, choosing 4 countries for consistency
countries = ["Sweden", "Libya", "India", "United States"]
df_collection = {}


# In[10]:


for country in countries:
    country_df = pd.DataFrame(columns=['Year', 'Immigration'])
    for year in range(1980, 2014):
        year_df = pd.DataFrame({
            "Year": [year],
            "Immigration": countries_df[countries_df["OdName"] == country][year]
        })
        country_df = country_df.append(year_df, ignore_index=True)
    df_collection[country] = country_df


# In[11]:


models = {}


# In[12]:


for country in df_collection:
    country_df = df_collection[country]
    x = country_df["Year"].astype("int")
    y = country_df["Immigration"].astype("float")
    model = np.poly1d(np.polyfit(x, y, 5))
    line = np.linspace(1980, 2013)
    # print("Country: ", country)
    # print("R2 Score: ")
    # print(r2_score(y, model(x)))
    # plt.scatter(x,y)
    # plt.plot(line, model(line))
    # plt.show()
    models[country] = model


# In[13]:


# Includes predictions for years beyond 2013
# for year in range(1980, 2030):
    # print("Year: ", year)
    # for country in models:
    # print(country, ": ", models[country](year))

    # In[ ]:
