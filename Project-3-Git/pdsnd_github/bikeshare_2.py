import sys
import time
import numpy as np
import pandas as pd
#I use a new library here, tabulate to make the arrangement nice for all columns.
from tabulate import tabulate

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

# This dictionary is used to convert the month from strength value to integer and vice-versa
months_name_and_numbers_dict = dict(
    [('January', 1), ('February', 2), ('March', 3), ('April', 4), ('May', 5), ('June', 6)])


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    city, month, day = None, None, None

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Would you like to see data for Chicago, New York, or Washington? \n').title()
            if city in ('Chicago', 'New York', 'Washington'):
                break
            else:
                print('please choose a valid city')
                continue
        except:
            print('please choose a valid city')
            continue

    # get user input for the filtering option [ month or day or not at all ]
    while True:
        try:
            # filtering_option will store what the user will chose to filter the data, either by month or day or not filtring data at all
            filtering_option = input('Would you like to filter the data by month, day, both, or not at all? \n').lower()

            if filtering_option == 'not at all':
                state = input('Would you like to start again or exit? \n').lower()
                if state == 'start again':
                    get_filters()
                else:
                    sys.exit()
            elif filtering_option in ('month', 'day', 'both'):
                break
            else:
                print('please choose a valid option')
                continue
        except:
            print('please choose a valid option')
            continue

    # get user input for month (all, january, february, ... , june)
    if filtering_option == 'month' or filtering_option == 'both':
        while True:
            try:
                month = input(
                    'Which month would you like to choose - January, February, March, April, May, or June? \n').title()
                if month in ('January', 'February', 'March', 'April', 'May', 'June'):
                    month = months_name_and_numbers_dict[month]
                    break
                else:
                    print('please choose a valid month')
                    continue
            except:
                print('please choose a valid month')
                continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filtering_option == 'day' or filtering_option == 'both':
        while True:
            try:
                day = input(
                    'Which day would you like to choose - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? \n').title()
                if day in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'):
                    break
                else:
                    print('please choose a valid day')
                    continue
            except:
                print('please choose a valid day')
                continue

    print('-' * 40)
    return city, month, day, filtering_option


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
    if city in ('Chicago', 'Washington'):
        df = pd.read_csv('{}.csv'.format(city.lower()), parse_dates=['Start Time', 'End Time'])
    else:
        df = pd.read_csv('new_york_city.csv', parse_dates=['Start Time', 'End Time'])

    if month is not None and day is not None:
        return df.loc[(df['Start Time'].dt.day_name() == day) & (df['Start Time'].dt.month == month)].reset_index(
            drop=True)
    elif month is not None:
        return df.loc[df['Start Time'].dt.month == month].reset_index(drop=True)
    else:
        return df.loc[df['Start Time'].dt.day_name() == day].reset_index(drop=True)


def time_stats(df, filtering_option):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Start Time'].dt.month.value_counts().nlargest(1)
    print('Most common month for traveling is: {}, Count: {}, Filter: {}'.format(
        [name for name, num in months_name_and_numbers_dict.items() if
         num == common_month.idxmax()][0], common_month.values[0], filtering_option))

    # display the most common day of week
    common_week = df['Start Time'].dt.day_name().value_counts().nlargest(1)
    print('Most common day of week for traveling: {}, Count: {}, Filter: {}'.format(
        common_week.idxmax(), common_week.values[0], filtering_option))

    # display the most common start hour
    common_hour = df['Start Time'].dt.hour.value_counts().nlargest(1)
    print('Most common start hour for traveling: {}, Count: {}, Filter: {}'.format(common_hour.idxmax(),
                                                                                   common_hour.values[0],
                                                                                   filtering_option))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df, filtering_option):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().nlargest(1)
    print('Most common used start station for traveling: {}, Count: {}, Filter: {}'.format(
        common_start_station.idxmax(), common_start_station.values[0], filtering_option))

    # display most commonly used end station
    common_end_station = df['End Station'].value_counts().nlargest(1)
    print('Most common used end station for traveling: {}, Count: {}, Filter: {}'.format(
        common_end_station.idxmax(), common_end_station.values[0], filtering_option))

    # display most frequent combination of start station and end station trip
    frequent_combination = df[['Start Station', 'End Station']].value_counts().nlargest(1)
    print('Most frequent combination of start station and end station trip: {}, Count: {}, Filter: {}'.format(
        frequent_combination.idxmax(), frequent_combination.values[0], filtering_option))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df, filtering_option):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time and mean travel time
    print('Total Duration: {}, Count: {}, Avg Duration: {}, Filter: {}'.format(df['Trip Duration'].sum(),
                                                                               df['Trip Duration'].count(),
                                                                               df['Trip Duration'].mean(),
                                                                               filtering_option))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city, filtering_option):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts().to_string().strip().split('\n')

    # I used for loop here because I assume that I have not seen the CSV file , as a result I don't know how many user type will be in the file
    [print('{}: {},'.format(user_counts[i].split()[0], user_counts[i].split()[1]), end=" ") for i in
     range(len(user_counts))]
    print('Filter: {}'.format(filtering_option))

     # Since the Washington file does not have any information about gender and birthdate, this Block will be Skipped if the user have chocen it nad go to the else statement

    if city != 'Washington':
        # Display counts of gender
        gender_counts = df['Gender'].value_counts().to_string().strip().split('\n')

        [print('{}: {},'.format(gender_counts[i].split()[0], gender_counts[i].split()[1]), end=" ") for i in
         range(len(gender_counts))]
        print('Filter: {}'.format(filtering_option))

        # Display earliest, most recent, and most common year of birth
        print(
            'Earliest year of birth: {}\nRecent year of birth: {}\nMost common year of birth: {}\n'.format(
                df['Birth Year'].min(),
                df['Birth Year'].max(),
                df['Birth Year'].value_counts().nlargest(1).idxmax()))
    else:
        print('Washington does not have any information about gender and birthdate')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    # This variable used to track the index of the printed raws
    i = 0
    while True:
        try:
            user_choice = input('Would you like to see the raw data? Enter yes or no\n').lower()
            if user_choice in ('yes', 'no'):
                if user_choice == 'yes':
                    print(tabulate(df.iloc[np.arange(0 + i, 5 + i)], headers="keys"))
                    i += 5
                    continue
                else:
                    break
            else:
                print('please choose a valid answer')
                continue
        except:
            print('please choose a valid answer')
            continue


def main():
    while True:
        city, month, day, filtering_option = get_filters()
        df = load_data(city, month, day)

        time_stats(df, filtering_option)
        station_stats(df, filtering_option)
        trip_duration_stats(df, filtering_option)
        user_stats(df, city, filtering_option)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no. \n')
        if restart.lower() != 'yes':
            sys.exit()


if __name__ == "__main__":
    main()
