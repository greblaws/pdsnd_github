import time
import pandas as pd
import numpy as np
import collections as coll
import statistics 
from statistics import mean
import os


os.chdir("C:/Users/grebl_000/Documents/00 - Personal/Career/Udacity")


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    if city != 'all':
        #Read Single city csv
        df = pd.read_csv(CITY_DATA[city])
    else:
        # read all city datasets
        chi = pd.read_csv('chicago.csv')
        nyc = pd.read_csv('new_york_city.csv')
        wash = pd.read_csv('washington.csv')
        frames = [chi, nyc, wash]
        df = pd.concat(frames, sort=True)
        #concat information from Python reference - expects a list

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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

#testdata = load_data("chicago","march","monday")

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
    valid_city = ['chicago', 'new york city', 'washington', 'all']
    while True:
        try:
           in_city = input("Enter City (Chicago, New York City, Washington, or All): ")
           city = in_city.lower()
           #creating an in_city then translating to a lower case city column just to kep straight...
        except ValueError:
           print("I dont understand that")
           continue
        if city not in valid_city:
           print("That is not a valid city choice")
           continue
        else:
           #print(city)         
           break
    
 # TO DO: get user input for month (all, january, february, ... , june)
    valid_mon = ['january', 'february', 'march', 'april','may','june','all']
    while True:
        try:
           in_month = input("Enter Month of interest (All, January, February, ... , June): ")
           month = in_month.lower()
        except ValueError:
           print("I dont understand that")
           continue
        if month not in valid_mon:
           print("That is not a valid month choice - please reenter")
           continue
        else:
           #print(month)         
           break
    
 # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    valid_day = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday', 'all']
    while True:
        try:
           in_day = input("Enter day of week (all, monday, tuesday, ... sunday): ")
           day = in_day.lower()
        except ValueError:
            print("I dont understand that")
            continue
        if day not in valid_day:
           print("That is not a valid day of week choice")
           continue
        else:
          #print(day)         
           break
    
    print('-'*40)
    return city, month, day


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    
    print('For Data Selected...')
    # display the most common month
    # learned of collections package, with Counter and most_common from Stackexchange
    c = coll.Counter(df['month'])
    mc_month = months[(c.most_common(1)[0][0])-1]
    #decided not to stack it all in the print command for clarity
    print('Most Common Month :  ',mc_month.title())
        
    # display the most common day of week
    c = coll.Counter(df['day_of_week'])
    print('Most Common Day of Week:  ',c.most_common(1)[0][0])
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    c_hour = coll.Counter(df['hour'])
    #print(c_hour)
    print('Most Common Hour:  ',c_hour.most_common(1)[0][0])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    c = coll.Counter(df['Start Station'])
    print('Most commonly used Start Station:  ',c.most_common(1)[0][0])

    # display most commonly used end station
    c = coll.Counter(df['End Station'])
    print('Most commonly used End Station:  ',c.most_common(1)[0][0])

    # display most frequent combination of start station and end station trip
    df['Start_End_Station'] = df['Start Station']+ ' / ' + df['End Station']
    c = coll.Counter(df['Start_End_Station'])
    print('Most commonly used Start Station/End Station Trip:  ',c.most_common(1)[0][0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    #format statement information from Pandas documentation and stackexchange
    print('Total Travel Time:   ', '% 6.2f' % sum(df['Trip Duration']) )

    # display mean travel time
    print('Average Total Travel Time in seconds:   ', '% 6.2f' % mean(df['Trip Duration']))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    #some datasets do not have Gender and Birth Year...
    #Stack overflow and python reference to find this...
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    if 'User Type' in df.columns:
        # Display counts of user types
        print('Counts by User Types:  ')
        #changed data type using to_frame to print more cleanly - without the extra line from value_counts
        #value_counts creates a separate line - and the data type is class 'pandas.core.series.Series
        #within that class there is an additional row of information with "Name: User Type, dtype: int64"
        print(df['User Type'].value_counts().to_frame())
    else:
        print("*** Cannot report on User Types since not in this data file ***")
    
    if 'Gender' in df.columns:
        # Display counts of gender
        print('Counts by Gender:  ')
        print(df['Gender'].value_counts().to_frame())
    else:
        print("*** Cannot report on Gender since not in this data file ***")
    
    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        print('Earliest Year of Birth:  ', '% 6.0f' % df['Birth Year'].min())
        print('Most Recent Year of Birth:  ', '% 6.0f' % df['Birth Year'].max())
        x = df['Birth Year']
        x = x.dropna()
        c = coll.Counter(x)
        print('Most Common Birth Year (excluding missing):  ','% 6.0f' % c.most_common(1)[0][0])
    else: 
        print("*** Cannot report on Birth Year since not in this data file ***")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        recnum = 0
        while True:
            try:
               # making the choice simple... yes means yes, anything else means no..
               in_yn = input("Would you like to see 5 lines of raw data? Enter yes if you do... anything else if you don't ")
               yn = in_yn.lower()
               
            except ValueError:
               print("I dont understand that")
               continue
            if yn == 'yes':
               print("Here are 5 sample records:")
               print(df.iloc(recnum, (recnum+5)))
               recnum = recnum + 5
               continue
            else:
               #print(city)         
               break
           
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        # again... making the choice simple... yes means yes, anything else means no..
        restart = input('\nWould you like to restart? Enter yes if you do....\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
