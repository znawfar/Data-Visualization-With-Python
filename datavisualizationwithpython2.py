
# -*- coding: utf-8 -*-
"""DataVisualizationWithPython2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dh4cy4h1U7rNtUisjn2hibIO5fW0KqQc

># **Data Visualization with Python (Part 2)**

- In this notebook I will plot maps with Markers.

- My dataset contains the data on police department incidents and its format is .csv. I've uploaded the dataset to Google Drive. 

*Let's get started!*
"""

!pip install -q -U watermark

# Commented out IPython magic to ensure Python compatibility.
# %reload_ext watermark
# %watermark -v -p numpy,pandas,matplotlib

# Commented out IPython magic to ensure Python compatibility.
#import os
import numpy as np
import pandas as pd
#from tqdm import tqdm
#import seaborn as sns
#from pylab import rcParams
# %matplotlib inline 
import matplotlib as mpl
import matplotlib.pyplot as plt
#from matplotlib import rc
#from scipy import stats

#import matplotlib.patches as mpatches
#from PIL import Image

import folium

from google.colab import drive
drive.mount('/content/gdrive')

!ls '/content/gdrive'

df = pd.read_csv('/content/gdrive/MyDrive/PoliceDepartmentIncidents.csv',encoding = "ISO-8859-1")
df.head(2)

""">***Just a Note***
- **IncidntNum:** Incident Number
- **Category:** Category of crime or incident
- **Descript:** Description of the crime or incident
- **DayOfWeek:** The day of week on which the incident occurred
- **Date:** The Date on which the incident occurred
- **Time:** The time of day on which the incident occurred
- **PdDistrict:** The police department district
- **Resolution:** The resolution of the crime in terms whether the perpetrator was arrested or not
- **Address:** The closest address to where the incident took place
- **X:** The longitude value of the crime location
- **Y:** The latitude value of the crime location
- **Location:** A tuple of the latitude and the longitude values
- **PdId:** The police department ID
"""

#finding out how many entries there are in our dataset.
df.shape

"""- I will work with the first 200 incidents in this dataset."""

# get the first 200 crimes in the df_incidents dataframe
limit = 200
df = df.iloc[0:limit, :]

df.shape

"""I want to visualize where these crimes took place in the city of San Francisco. I will use the default style, and we will initialize the zoom level to 10."""

# San Francisco latitude and longitude values
latitude = 37.77
longitude = -122.42

# I must create map and display it
SanFrancisco_map = folium.Map(location=[latitude, longitude], zoom_start=10)


SanFrancisco_map

"""- I will superimpose the locations of the crimes onto the map. The way to do that in Folium is to create a feature group with its own features and style and then add it to the Merced_map."""

# instantiate a feature group for the incidents in the dataframe
incidents = folium.map.FeatureGroup()

# loop through the 200 crimes and add each to the incidents feature group
for lat, lng, in zip(df.Y, df.X):
    incidents.add_child(
        folium.features.CircleMarker(
            [lat, lng],
            radius=5, # define how big you want the circle markers to be
            color='pink',
            fill=True,
            fill_color='red',
            fill_opacity=0.6
        )
    )

# add pop-up text to each marker on the map
latitudes = list(df.Y)
longitudes = list(df.X)
labels = list(df.Category)

for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker([lat, lng], popup=label).add_to(SanFrancisco_map)    
    

SanFrancisco_map.add_child(incidents)

"""- Now, I am able to know what crime category occurred at each marker.

- I will remove these location markers and just add the text to the circle markers themselves.  It helps me to figure out the main features better.
"""

# I will create map and display it
SanFrancisco_map = folium.Map(location=[latitude, longitude], zoom_start=10)


for lat, lng, label in zip(df.Y, df.X, df.Category):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5, # define how big I want the circle markers to be
        color='pink',
        fill=True,
        popup=label,
        fill_color='red',
        fill_opacity=0.6
    ).add_to(SanFrancisco_map)

SanFrancisco_map

"""- Now, I want to apply another proper remedy to group the markers into different clusters. I will represent each cluster by the number of crimes in each neighborhood. These clusters can be thought of as pockets of San Francisco which can be analyzed separately.

- I will do it by instantiating a MarkerCluster object and adding all the data points in the dataframe to this object. 
"""

from folium import plugins

# let's start again with a clean copy of the map of San Francisco
SanFrancisco_map = folium.Map(location = [latitude, longitude], zoom_start = 10)

# instantiate a mark cluster object for the incidents in the dataframe
incidents = plugins.MarkerCluster().add_to(SanFrancisco_map)

# loop through the dataframe and add each data point to the mark cluster
for lat, lng, label, in zip(df.Y, df.X, df.Category):
    folium.Marker(
        location=[lat, lng],
        icon=None,
        popup=label,
    ).add_to(incidents)

SanFrancisco_map
