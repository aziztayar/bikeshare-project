import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    
    while True:
        city = input("\nWhat city would you like to view?\n").lower()
        if city in ['chicago', 'new york', 'washington']:
            break
        else:
            print('Selected city is not found, Try a different city!')

    # TO DO: get user input for month (all, january, february, ... , june)
    
    while True:
        month = input('\nPlease enter a month:\n').lower()
        if month in ["january", "february", "march", "april", "may", "june"]:
            break
        else:
            print('\nInvalid input, try again!\n')


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    
    while True:
        day = input('\nPlease enter a day\n').lower()
        if day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]:
            break
        else:
            print('\nInvalid input, try again!\n')

   
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
    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name)
    
    df['Start Time'] = pd.to_datetime(arg = df['Start Time'], format = '%Y-%m-%d %H:%M:%S')
    
    if month != 'all':
        df['month'] = df['Start Time'].dt.month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        df = df.loc[df['month'] == month]
        
    if day != 'all':
        df['day_of_week'] = df['Start Time'].dt.weekday_name
        
        df = df.loc[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
   
    common_month = df['month'].mode()[0]
    print('Most Common Month:', common_month)



    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most Common day:', most_common_day)


    # TO DO: display the most common start hour
    
    df['hour'] = df['Start Time'].dt.hour
    max_hour = df['hour'].mode()[0]
    print('Most Common Hour:', max_hour)

          
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('\nMost common start station: {}\n'.format(
    df['Start Station'].mode().values[0]))

    # TO DO: display most commonly used end station

    print('\nMost common end station:{}\n'.format(
        df['End Station'].mode().values[0]))
    # TO DO: display most frequent combination of start station and end station trip
    combine_trip = df['Start End'] = df['Start Station'].map(str) + ' to ' + df['End Station']
    common_start_end_trip = combine_trip.value_counts().idxmax()
    print('\nMost frequent start and end combination trip:{}\n'.format(common_start_end_trip))
  


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    
    total_time = df['Trip Duration'].sum()
    print('\nTotal travel time:', total_time/86400, " Days")

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_time/60, " Minutes")

    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    
    # TO DO: Display counts of gender
    if('Gender' in df):
        m_gender = df['Gender'].str.count('Male').sum()
        f_gender = df['Gender'].str.count('Female').sum()
        print('\nMale users are:{}\n'.format(int(m_gender)))
        print('\nFemale users are: {}\n'.format(int(f_gender)))

    # TO DO: Display earliest, most recent, and most common year of birth
   
    if('Birth Year' in df):
        earliest_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()
        print('\nOldest birth year: {}\nYoungest birth year: {}\nMost popular birth year: {}\n'.format(int(earliest_birth),int(recent_birth),int(most_common_birth)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
   
def display_data(df):

    row_length = df.shape[0]

    for i in range(0, row_length, 5):
        
        yes = input('\nDo you want to see the raw data of user trip? Type Yes or No\n ')
        if yes.lower() != 'yes':
            break
            
        row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in row_data:
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)

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


if __name__ == "__main__":
    main()