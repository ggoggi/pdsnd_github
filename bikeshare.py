import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months    = [ 1, 2, 3, 4, 5, 6 ]
days      = [ 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday' ]

def get_filters():
    '''Handles and store user inputs into variables for the upcoming analysys'''
#The function stores the city input in the variable city,
#then stores the filters input in the variable get_filters.
#This allows to manage each of the 4 possible scenarios separately
    print('\nHello! Let\'s explore some US bikeshare data!')

    city = input("Would you like to see data from Chicago, New York City or Washington? ").lower()
    while city not in CITY_DATA:
        print('\nPlease enter a valid city name.' )
        city = input("\nWould you like to see data from Chicago, New York or Washington? ").lower()

    filters = input("\nWould you like to apply a time filter? Choose month, day, both or none: ").lower()
    while filters not in ['month','day','both','none']:
        print('\ninvalid input :(')
        filters = input("\nChoose month, day, both or none: ").lower()

    if filters == 'month':
        month = int(input("Choose the month to filter by (1 to 6): "))
        day = 'all'
        while month not in months:
            print('\nInvalid input :(')
            month = int(input("Choose a month from 1 to 6: "))

    elif filters == 'day':
        day = input("Choose the day of week to filter by (monday to sunday): ")
        mont = 'all'
        while day not in days:
            print('\nInvalid input :(')
            day = input("Choose a day from monday to sunday")

    elif filters == 'both':
        month = int(input("Number of the month to filter by (1 to 6): "))
        while month not in months:
            print('\nInvalid input :(')
            month = int(input("Choose a month from 1 to 6: "))
        day = input("Choose the day of week to filter by (monday to sunday): ")
        while day not in days:
            print('\nInvalid input :(')
            day = input("Choose a day from monday to sunday: ")

    elif filters == 'none':
        month = 'all'
        day = 'all'

    print ('Current filters: {} as city, {} as month(s) {} as day(s)'.format(city, month, day))
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    '''Use the user inputs to load the correct data'''
    df = pd.read_csv(CITY_DATA.get(city))

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    '''Displays statistics on the most frequent times of travel.'''

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('\nMost common month: {}'.format(popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('\nMost common day: {}'.format(popular_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\nMost common hour: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nMost popular start station: {}'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost popular end station: {}'.format(popular_end_station))

    # display most frequent trip (ordered pair of start station and end station)
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['trip'].mode()[0]
    print('\nMost popular trip: {}'.format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    tot_travel_time = df['Trip Duration'].sum()/3600
    print('\nTotal travel time in hours: {}'.format(tot_travel_time))
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()/60
    print('\nMean travel time in minutes: {}'.format(mean_travel_time))
    # display longest trip
    longest_trip = df['Trip Duration'].max()/60
    print('\nLongest trip in minutes: {}'.format(longest_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\n count of users by type:\n')
    print(df['User Type'].value_counts())

    # Display counts of gender (except Washington)
    try:
        print('\n count of users by gender:\n')
        print(df['Gender'].value_counts())
    except:
        print ('Gender datas are unavailable for this city')


    # Display earliest, most recent, and most common year of birth (except Washington)
    try:
        print('\nEarliest year of birth: {}'.format(df['Birth Year'].min()))
        print('Most recent year of birth: {}'.format(df['Birth Year'].max()))
        print('Average year of birth: {}'.format(df['Birth Year'].avg()))
    except:
        print ('Birth year datas are unavailable for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw(df):
    '''Asks the user if to show raw data'''
    i=0
    while input('would you like to see individual trip datas? yes/no ') == 'yes':
        print(df[i:i+5])
        i=i+5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
