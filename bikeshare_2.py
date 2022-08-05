import time
import pandas as pd
import numpy as np


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Would you like to see data for Chicago, New York, or Washington?')
    city = input().title()
    while city not in ('Chicago', 'New York', 'Washington'):
        print('Invalid city!\nPlease type it again:')
        city = input().title()
    print('You have chosed {}.'.format(city))

    # get user input for month (all, january, february, ... , june)
    print('Would you like to filter the data by month, day, or not at all? Type \'none\' for no time filter.')
    time_filter = input().lower()
    while time_filter not in ('month', 'day', 'none'):
        print('Invalid input!\nPlease try again:')
        time_filter = input().lower()
    print('You have chosed {}.'.format(time_filter))

    if time_filter == 'month':
        day = 'all'
        print('Which month? January, February, March, April, May or June?')
        month = input().title()
        while month not in ('January', 'February', 'March', 'April', 'May', 'June'):
            print('Invalid month!\nPlease try again:')
            month = input().title()
        print('You have chosed {}.'.format(month))

    elif time_filter == 'day':
        month = 'all'
        print('Which day? Please type your response as an integer (e.g.: 0 = Monday, 1 = Tuesday...):')
        day = input()
        while day not in ('0', '1', '2', '3', '4', '5', '6'):
            print('Invalid day!\nPlease try again:')
            day = input()
        print('You have chosed {}.'.format(day))

    else:
        month = 'all'
        day = 'all'
    # get user input for day of week (all, monday, tuesday, ... sunday)

    print('-'*40)
    return city, month, day


CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }


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
    df['day_of_week'] = df['Start Time'].dt.day_of_week

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == int(day)]
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        most_common_month = df['month'].mode()[0]
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        most_common_month = months[most_common_month-1]
        print('Most common month:', most_common_month)

    # display the most common day of week
    if day == 'all':
        most_common_day = df['day_of_week'].mode()[0]
        daylist = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        most_common_day = daylist[most_common_day]
        print('Most common day of week:', most_common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:', common_end_station)

    # display most frequent combination of start station and end station trip
    df['combination'] = 'from ' + df['Start Station'] + ' to ' + df['End Station']
    common_combination = df['combination'].mode()[0]
    print('Most frequent combination of start station and end station trip:', common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['End Time'] = pd.to_datetime(df['End Time'])
    df['duration'] = (df['End Time'] - df['Start Time']).dt.seconds
    # display total travel time
    total_duration = df['duration'].sum()
    print('Total trip duration:', total_duration)
    # display mean travel time
    average_duration = df['duration'].mean()
    print('Average trip duration:', average_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    if city in ('Chicago', 'New York'):
        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print(gender_count)

        # Display earliest, most recent, and most common year of birth
        year_min = int(df['Birth Year'].min())
        year_max = int(df['Birth Year'].max())
        year_common = int(df['Birth Year'].mode()[0])
        print('earliest year of birth:', year_min)
        print('most recent year of birth:', year_max)
        print('most common year of birth:', year_common)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        # Display 5 rows of raw data each time if users want
        for i in range(0, len(df), 5):
            print('Would you like to see more raw data? Please type \'yes\' or \'no\'.')
            if input().lower() == 'yes':
                print(df.iloc[i:i+5])
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
