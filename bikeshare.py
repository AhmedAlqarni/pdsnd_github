#!/usr/bin/env python
# coding: utf-8

# # Welcome to Jupyter!

# This repo contains an introduction to [Jupyter](https://jupyter.org) and [IPython](https://ipython.org).
# 
# Outline of some basics:
# 
# * [Notebook Basics](../examples/Notebook/Notebook%20Basics.ipynb)
# * [IPython - beyond plain python](../examples/IPython%20Kernel/Beyond%20Plain%20Python.ipynb)
# * [Markdown Cells](../examples/Notebook/Working%20With%20Markdown%20Cells.ipynb)
# * [Rich Display System](../examples/IPython%20Kernel/Rich%20Output.ipynb)
# * [Custom Display logic](../examples/IPython%20Kernel/Custom%20Display%20Logic.ipynb)
# * [Running a Secure Public Notebook Server](../examples/Notebook/Running%20the%20Notebook%20Server.ipynb#Securing-the-notebook-server)
# * [How Jupyter works](../examples/Notebook/Multiple%20Languages%2C%20Frontends.ipynb) to run code in different languages.

# You can also get this tutorial and run it on your laptop:
# 
#     git clone https://github.com/ipython/ipython-in-depth
# 
# Install IPython and Jupyter:
# 
# with [conda](https://www.anaconda.com/download):
# 
#     conda install ipython jupyter
# 
# with pip:
# 
#     # first, always upgrade pip!
#     pip install --upgrade pip
#     pip install --upgrade ipython jupyter
# 
# Start the notebook in the tutorial directory:
# 
#     cd ipython-in-depth
#     jupyter notebook

# In[1]:


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# In[2]:


def read_input(inputStr,inputType):
    """
    Validates user input.
    inputStr: is the input of the user
    inputType: is the type of input: 1 = city, 2 = month, 3 = day
    """
    while True:
        inputRead=input(inputStr)
        try:
            if inputRead.lower() in ['chicago','new york city','washington'] and inputType == 1:
                break
            elif inputRead.lower() in ['january', 'february', 'march', 'april', 'may', 'june','all'] and inputType == 2:
                break
            elif inputRead.lower() in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'] and inputType == 3:
                break
            else:
                if inputType == 1:
                    print("Sorry, your input should be: chicago, new york city, or washington")
                if inputType == 2:
                    print("Sorry, your input should be: january,.... may, june or all")
                if inputType == 3:
                    print("Sorry, your input should be: sunday,.... friday, saturday or all")
        except ValueError:
            print("Sorry, your input is wrong")
    return inputRead


# In[3]:


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
  
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city = read_input("Would you like to see the data for chicago, new york city, or washington?",1)
    month = read_input("Which Month (all, january, .... june)?", 2)
    day = read_input("Which day? (all, monday,....saturday, sunday)", 3)
    print('-'*40)
    return city.lower(), month.lower(), day.lower()


# In[4]:



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


# In[5]:



def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    if month == 'all':
        popular_month = df['month'].mode()[0]
        print('Most Popular Month:', popular_month)
        
    if day == 'all':
        popular_day_of_week = df['day_of_week'].mode()[0]
        print('Most Popular Day Of the Week:', popular_day_of_week)

    popular_common_start_hour = df['hour'].mode()

    print('Most Common Start Hour:', popular_common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[6]:



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()

    print('Most Start Station:', popular_start_station)

    popular_end_station = df['End Station'].mode()

    print('Most End Station:', popular_end_station)

    group_field=df.groupby(['Start Station','End Station'])
    
    popular_combination_station = group_field.size().sort_values(ascending=False).head(1)
    
    print('Most frequent combination of Start Station and End Station trip:\n', popular_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[7]:



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    mean_travel_time = df['Trip Duration'].mean()

    print('Mean Travel Time:', mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[8]:



def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    print('User Type Stats:')
    print(df['User Type'].value_counts())
    if city != 'washington':

        print('Gender Stats:')
        print(df['Gender'].value_counts())

        print('Birth Year Stats:')
        most_common_year = df['Birth Year'].mode()
        print('Most Common Year:',most_common_year)
        most_recent_year = df['Birth Year'].max()
        print('Most Recent Year:',most_recent_year)
        earliest_year = df['Birth Year'].min()
        print('Earliest Year:',earliest_year)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nDo you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

