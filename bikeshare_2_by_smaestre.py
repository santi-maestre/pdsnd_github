import time, calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = list(CITY_DATA.keys())
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    while True:
        city = str(input('\nWhich city would you like to see data: Chicago, New York or Washington?\n')).lower()
        if city in cities:
            break
        else:
            print('\nThis is not a valid city name!')

    # get user input for month (all, january, february, ... , june)
    month = str(input('\nWould you like to filter data by month?\nIf so, please, type a month among these ones:\nJanuary, February, March, April, May or June.\nIf you don\'t want to filter by month type "all"\n')).lower()
    while True:
        if month in months or (month == 'all'):
            break
        else:
            print('\nThis is not a valid name for month filter!')
            month = str(input('\nIf you\'d like to filter data by month, please, type a month among these ones:\nJanuary, February, March, April, May or June.\nIf you don\'t want to filter by month type "all"\n')).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = str(input('\nWould you like to filter data by day of week?\nIf so, please, type the name of the day or type "all" if you don\'t want to filter data by day\n')).lower()
    while True:
        if day in days or (day == 'all'):
            break
        else:
            print('\nThis is not a valid name for day of week filter!')
            day = str(input('\nIf you\'d like to filter data by day of week, please, type the name of the day or type "all" if you don\'t want to filter data by day\n')).lower()

    print('-'*40)
    return city, month, day


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day = days.index(day)
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month or else print month filter
    df['month'] = df['Start Time'].dt.month
    if month == 'all':
        popular_month = calendar.month_name[df['month'].mode()[0]]
        print('\nThe most frequent month is:\n{}\n'.format(popular_month))
    else:
        print('\nMonth filter applied:\n{}\n'.format(month))

    # display the most common day of week or else print day of week filter
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    if day == 'all':
        popular_day_of_week = calendar.day_name[df['day_of_week'].mode()[0]]
        print('\nThe most frequent day of the week is:\n{}\n'.format(popular_day_of_week))
    else:
        print('\nDay of week filter applied:\n{}\n'.format(day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\nThe most frequent start hour is:\n{}\n'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_used_start_station = df['Start Station'].mode()[0]
    print('\nThe most commonly used start station is:\n{}\n'.format(most_used_start_station))

    # display most commonly used end station
    most_used_end_station = df['End Station'].mode()[0]
    print('\nThe most commonly used end station is:\n{}\n'.format(most_used_end_station))

    # display most frequent combination of start station and end station trip
    df['Trip'] = "from " + df['Start Station'] + ' station to ' + df['End Station'] + ' station'
    most_frequent_trip = df['Trip'].mode()[0]
    print("\nThe most frequent trip is:\n{}\n".format(most_frequent_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = int(df['Trip Duration'].sum())
    print('\nThe total trip duration is\n{}\n'.format(total_trip_duration))

    # display mean travel time
    mean_trip_duration = int(df['Trip Duration'].mean())
    print('\nThe average trip duration is\n{}\n'.format(mean_trip_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = dict(df['User Type'].value_counts())
    user_types = list(user_types_counts)
    print('\nSplit between user types:\n{}: {}\n{}: {}\n'.format(user_types[0], user_types_counts[user_types[0]], user_types[1], user_types_counts[user_types[1]]))

    # Because not all city data files contain Gender info I must assure gender statistics are only calculated when that column is present
    df_columns = list(df.columns)
    if 'Gender' in df_columns:
        # Display counts of gender
        user_gender_counts = dict(df['Gender'].value_counts())
        genders = list(user_gender_counts)
        print('\nSplit between genders is:\n{}: {}\n{}: {}\n'.format(genders[0], user_gender_counts[genders[0]], genders[1], user_gender_counts[genders[1]]))

    # Same applies for Birth Year statistics, i.e., not al city data files contain Birth Year info
    if 'Birth Year' in df_columns:
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print('\nThe users oldest year of birth is:\n{}\n'.format(earliest_birth_year))
        print('\nThe users youngest year of birth is:\n{}\n'.format(most_recent_birth_year))
        print('\nThe users most popular year of birth is:\n{}\n'.format(most_common_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #Asks the user if she/he wants to see raw data on a 5 lines basis
        see_raw_data = input('\nWould you like to see 5 lines of raw data? Type yes or no.\n')
        if see_raw_data == 'yes':
            raw_data = pd.read_csv(CITY_DATA[city])
            size = 5
            counter = 0
            while (counter + size) < len(raw_data):
                for i in range(counter, (counter + size)):
                    print(dict(raw_data.loc[i]))
                counter += size
                see_raw_data = input('\nWould you like to see another 5 lines of raw data? Type yes or no.\n')
                if see_raw_data != 'yes':
                    break

        #Asks the user to restart or not the program
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
