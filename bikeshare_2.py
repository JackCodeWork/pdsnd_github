import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


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

    while True:
        city = input("Please enter city (Chicago, New York City, Washington) that you would like to see the data "
                     "from: \n").lower()
        if city == "chicago" or city == "new york city" or city == "washington":
            break
        else:
            print("Please enter city name in the options.")

    # get user input for month (all, january, february, ... , june)

    # generate month array
    months_ary = []
    for i in range(1, 13):
        months_ary.append(calendar.month_name[i].lower())

    while True:
        month = input("Please enter month (January, February, ... , June)  or all for no month filter: \n").lower()
        if month in months_ary or month.lower() == "all":
            break
        else:
            print("Please enter month in the options.")

    # get user input for day of week (all, monday, tuesday, ... sunday)

    # generate day of week array
    days_ary = []
    for i in range(0, 7):
        days_ary.append(calendar.day_name[i].lower())

    while True:
        day = input(
            "Please enter day of week (Monday, Tuesday, ... Sunday) or all for no day of week filter: \n").lower()
        if day in days_ary or day.lower() == "all":
            break
        else:
            print("Please enter day of week in the options.")

    print('-' * 40)
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

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    print('Most Frequent Start month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    print('Most Frequent Start day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    print('Most Commonly Used Start Station:', popular_start_station)
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    print('Most Commonly Used End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('\nMost Frequent Combination of Start Station and End Station Trip:', popular_combination[0], " and ",
          popular_combination[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("\nThe total travel time is:", total_time, 'seconds')

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("\nThe mean travel time is:", mean_time, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nDisplay counts of user types:\n")
    print(user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("\nDisplay counts of gender:\n")
        print(gender_counts)
    else:
        print("\nNo information for counts of gender")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()[0]
        print('\nEarliest year of birth:', int(earliest_birth))
        print('\nMost recent year of birth:', int(recent_birth))
        print('\nMost common year of birth:', int(common_birth))
    else:
        print("\nNo information for earliest, most recent, and most common year of birth")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    """Displays raw data on bikeshare upon users request."""

    start_time = time.time()
    range = 0

    while True:
        user_input = input("\nDo you wish to see 5 lines of raw data of bikeshare? YES/NO\n").lower()
        if user_input == "no":
            break
        elif user_input == "yes":
            data = df.iloc[range:range+5]
            print(data)
            range += 5
        else:
            print("Please enter YES/NO.")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
