# -*- coding: utf-8 -*-
'''
Created on Sun Nov 17 00:59:21 2019

@author: Asmita Singh
'''
# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

# Read the data file
storm_df = pd.read_csv('C:/Users/Asmita Singh/Documents/GMU/AIT 580/Project Dataset/1950-2018_all_tornadoes.csv')
pd.set_option('display.max_columns', 500)

# Display records after reading the file
storm_df.head()

# Summary Statistics
storm_df.describe()

# Display the datatypes
storm_df.dtypes

# Converting the loss values for the years before 1996 into dollars
storm_df.loc[(storm_df.yr < 1996) & (storm_df.loss == 0), 'LossNew'] = 10
storm_df.loc[(storm_df.yr < 1996) & (storm_df.loss == 1), 'LossNew'] = 50
storm_df.loc[(storm_df.yr < 1996) & (storm_df.loss == 2), 'LossNew'] = 250
storm_df.loc[(storm_df.yr < 1996) & (storm_df.loss == 3), 'LossNew'] = 2750
storm_df.loc[(storm_df.yr < 1996) & (storm_df.loss == 4), 'LossNew'] = 27500
storm_df.loc[(storm_df.yr < 1996) & (storm_df.loss == 5), 'LossNew'] = 275000
storm_df.loc[(storm_df.yr < 1996) & (storm_df.loss == 6), 'LossNew'] = 2750000
storm_df.loc[(storm_df.yr < 1996) & (storm_df.loss == 7), 'LossNew'] = 27500000
storm_df.loc[(storm_df.yr < 1996) & (storm_df.loss == 8), 'LossNew'] = 275000000
storm_df.loc[(storm_df.yr < 1996) & (storm_df.loss == 9), 'LossNew'] = 500000000

# Converting loss from 1996 into million dollars
storm_df.loc[(storm_df.yr >= 1996), 'LossNew'] = storm_df.loss*1000000
storm_df.loc[(storm_df.yr > 2015) , 'LossNew'] = storm_df.loss

# Check for Loss counts
storm_df['LossNew'].value_counts()

# 2. Inspecting the loss caused before and after 1995.
# Losses Before 1996
storm_df[storm_df['yr'] < 1996].groupby(['yr'])[['LossNew']].sum().sort_values(['yr'],ascending=False).plot(kind='line',color='SteelBlue').grid(True)
plt.title('Total Loss 1950-1995', color='Black')
plt.xlabel('Year', color='Black')
plt.ylabel('Loss in million dollars', color='Black')

# After 1995
storm_df[storm_df['yr'] >= 1995].groupby(['yr'])[['LossNew']].sum().sort_values(['yr'],ascending=False).plot(kind='line',color='SteelBlue').grid(True)
plt.title('Total Loss 1995-2018', color='Black')
plt.xlabel('Year', color='Black')
plt.ylabel('Loss in million dollars', color='Black')

# Finding the number of storms based on severity (magnitude) over years.
# Number of storms based on severity
storm_df['mag'].value_counts().plot(kind='bar', color='Steelblue').grid(True)
plt.title('Number of storms based on Magnitude', color='Black')
plt.xlabel('Magnitude', color='Black')
plt.ylabel('Count', color='Black')
plt.show()

print('Number of storms based on Magnitude')
print(storm_df['mag'].value_counts())

# FC values based on the data
storm_df['fc'].value_counts().plot(kind='bar', color='Steelblue').grid(True)
plt.title('FC values in the data', color='Black')
plt.xlabel('FC', color='Black')
plt.ylabel('Count', color='Black')
plt.show()

print('FC values in the data')
print(storm_df['fc'].value_counts())

# Exploratory Analysis using Scatterplots
# Scatterplot for length
ax = sns.scatterplot(x='yr', y='len', data=storm_df)
ax.set(xlabel='Year', ylabel='Length (in miles)')
ax.set(title='Length of the storm')
plt.show()

# Scatterplot for Width
# Converting miles to yards
storm_df['width'] = storm_df['wid']*0.000568182
ax = sns.scatterplot(x='yr', y='width', data=storm_df)
ax.set(xlabel='Year', ylabel='Width (in miles)')
ax.set(title='Width of the storm')
plt.show()

# How many numbers of tornadoes came over the years?
storm_df.groupby(['yr'])['yr'].count().plot(kind='line',color='SteelBlue', marker='o').grid(True)
plt.title('Number of Tornadoes 1950-2018', color='Black')
plt.xlabel('Year', color='Black')
plt.ylabel('Count', color='Black')

print('Number of Tornadoes 1950-2018')
print(storm_df.groupby(['yr'])['yr'].count())

# What is the total loss suffered over the years?
#tornadoes_1996to2015 = storm_df[storm_df['yr'] >= 1996][['st','loss']]
#print('Total Loss sufferd by States: 1950-2018')
#print(tornadoes_1996to2015)

# How many numbers of fatalities are there by the state?
storm_df[storm_df['fat'] > 3].groupby(['st'])[['fat']].sum().sort_values(['fat'],ascending=False).plot(kind='bar',color='SteelBlue').grid(True)
plt.title('Number of fatalities by State', color='Black')
plt.xlabel('State', color='Black')
plt.ylabel('Number of fatalities', color='Black')

print('Number of fatalities by State')
print(storm_df[storm_df['fat'] > 3].groupby(['st'])[['fat']].sum().sort_values(['fat'],ascending=False))

# How many numbers of Tornado injuries caused by the magnitude of the storm?
sns.set(style='whitegrid')
ax = sns.boxplot(x='mag', y='inj', data=storm_df, width=0.5, palette='colorblind')
plt.title('Visualization for Tornado Injuries')
plt.xlabel('Magnitude', color='Black')
plt.ylabel('Injuries', color='Black')
plt.show()

# How the latitude and longitude of the tornado changing?
ax = sns.scatterplot(x='slon', y='slat', data=storm_df)
ax.set(xlabel='Starting Longitude', ylabel='Starting Latitude')
ax.set(title='Latitude and Longitude Change of the Storms')
plt.show()

