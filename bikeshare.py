#!/usr/bin/env python
# coding: utf-8

# In[18]:


import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
# In[19]:


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York, or Washington?")
    while not (city.lower() in CITY_DATA.keys()): 
        print("It's not a valid city name")
        city = input("Would you like to see data for Chicago, New York, or Washington?")
    print('-'*40) 

    # TO DO: get user input for month (all, january, february, ... , june)
    valid_month = ['all','january','february','march','april','may','june'] 
    month = input("Which month? all, january, february, ... , june?")
    while not (month.lower() in valid_month): 
        print("It's not a valid month name")
        city = input("Which month? all, january, february, ... , june?")
    print('-'*40)
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    valid_day = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    day = input("Which day? all, monday, tuesday, ... sunday?")
    while not (day.lower() in valid_day): 
        print("It's not a valid day name")
        city = input("Which day? all, monday, tuesday, ... sunday?")
    print('-'*40)
    
    return city, month, day


# In[20]:


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
    
    for city_name in CITY_DATA.keys():
        if city.lower() == city_name:
            df = pd.read_csv(CITY_DATA[city_name])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


# In[21]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    start_time = time.time()

    # TO DO: display the most common month
    print("\nThe Most Common Month: %s.\n" % (months[(df['month'].mode()[0])-1].title()))

    # TO DO: display the most common day of week
    print("\nThe Most Common day of week: %s. \n" % (df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('\nMost Popular Start Hour: %s. \n' % (df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[22]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("\nThe Most Commonly Used Start Station: %s.\n" % (df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print("\nThe Most Commonly Used End Station: %s.\n" % (df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    df['Combined Stations'] = df['Start Station'] + " and " + df['End Station']
    print("\nThe Most Frequent Combination of Start Station and End Station trip: %s.\n" % (df['Combined Stations'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[23]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['End Time'] = pd.to_datetime(df['End Time'])
    # TO DO: display total travel time
    print("\nTotal Travel Time: %s.\n" % ((df['End Time'] - df['Start Time']).sum()))

    # TO DO: display mean travel time
    print("\nMean Travel Time: %s.\n" % ((df['End Time'] - df['Start Time']).mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[24]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('\nThe Counts of User Types\n')
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    print('\nThe Counts of Gender\n')
    
    try : 
        print(df['Gender'].value_counts())
    except KeyError:
        print("Sorry, There is not Gender Information")

    # TO DO: Display earliest, most recent, and most common year of birth
    column_name = df.columns.values.tolist()
    if 'Birth Year' in column_name:
        print('\nThe earliest year of birth: %s.\n' % (int(df['Birth Year'].min())))
        print('\nThe most recent year of birth: %s.\n' % (int(df['Birth Year'].max())))
        print('\nThe most common year of birth: %s.\n' % (int(df['Birth Year'].mode()[0])))
    else:
        print('No Birth Year Data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[25]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


# In[ ]:


if __name__ == "__main__":
	main()


# In[ ]:





# In[ ]:




