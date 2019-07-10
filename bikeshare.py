import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
week_days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_valid_input(message, valid_values, accept_all=False):
    ''' Prompts user with a message for input until entry is valid

        Args:
            (str) message - Message to display to user
            (list) valid_values - the accepted values
            (boolean) accept_all - True/False for allowing "All" to be input

        Returns:
            the valid input from the user
    '''
    not_valid = True
    while not_valid:
        user_input = input("\n" + message +"\n").lower()
        if (user_input not in valid_values and user_input != 'all') or (user_input == 'all' and accept_all == False):
            print("That input is not recognized.")
        else:
            not_valid = False #user entered valid input
    return user_input

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
    city = get_valid_input("Enter the city to explore (Chicago, New York City, Washington):", CITY_DATA.keys(), False)

    # get user input for month (all, january, february, ... , june)
    month = get_valid_input("Enter the month (January, February, March, April, May, June, or All):", months, True)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_valid_input("Enter the day of week (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All):", week_days, True)

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
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # some final data manipulation needed for statistics
    df['st_hour'] = df['Start Time'].dt.hour
    df['station_combo'] = df['Start Station'] + " to " + df['End Station']

    return df

def see_data(df):
    ''' Prompts user if he wants to display the first 5 records of original data filtered to their selections
        If enters 'yes', the records are displayed. '''

    see_data = get_valid_input("Would you like to see the first 5 records of data? Enter yes or no.",["yes","no"], False)
    if see_data == 'yes':
        print(df.iloc[:,:-4].head())

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most Common Month:  {}".format(months[df['month'].mode()[0]-1].title()))

    # display the most common day of week
    print("Most Common Weekday:  {}".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print("Most Common Hour of Day:  {}".format(df['st_hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most Common Starting Station:  {}".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("Most Common Ending Station:  {}".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print("Most Common Station Combination:  {}".format(df['station_combo'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def split_seconds(ttl_seconds):
    ''' Breaks down seconds into number of hours, minutes and remaining seconds
        Args: Total amount of seconds
        Returns: Hours, Minutes, Seconds
    '''
    hours = ttl_seconds//3600
    minutes = (ttl_seconds//60) - (hours * 60)
    seconds = ttl_seconds%60
    return hours, minutes, seconds

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    ttl_time = df['Trip Duration'].sum()
    h, m, s = split_seconds(ttl_time)
    print("Total Travel Time: {} hours, {} minutes, and {} seconds".format(h,m,s))

    # display mean travel time
    avg_time = df['Trip Duration'].mean()
    h, m, s = split_seconds(avg_time)
    print("Average Travel Time: {} hours, {} minutes, and {} seconds".format(h,m,s))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_cnt_dict(cnt_dict, header=""):
    ''' Prints key and values in dictionary, formatted for easier reading
        Args: the dictionary, optional header
        Returns: Does not return, only prints
    '''
    print(header)
    for key,value in cnt_dict.items():
        print("    {}\t: {}".format(key,value))

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    type_cnts = dict(df['User Type'].value_counts())
    print_cnt_dict(type_cnts, "User Type Counts")

    # Display counts of gender
    try:
        gender_cnts = dict(df['Gender'].value_counts())
        print_cnt_dict(gender_cnts, "Gender Counts")
    except:
        print("Selected ity does not have gender data.")

    # Display earliest, most recent, and most common year of birth
    try:
        print("Earliest User Birth Year:  {}".format(int(df['Birth Year'].min())))
        print("Most Recent User Birth Year:  {}".format(int(df['Birth Year'].max())))
        print("Most Common User Birth Year:  {}".format(int(df['Birth Year'].mode()[0])))
    except:
        print("Selected city does not have birth year data.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        see_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
