import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'ch': 'chicago.csv',
              'ny': 'new_york_city.csv',
              'wa': 'washington.csv' }
cities_symbols = ['ch', 'ny', 'wa']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday' 'Sunday']
months = ['all', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']



def get_filters():
    
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        try:
            city = str(input('Please enter the Symbol for the city you would to see data for i.e chicago: ch, new york city: ny, washington: wa: '))
            if city in cities_symbols:
                break
        except:
            print('None valid city Symbol!')
            

    while True:
        filter_type = str(input('Would you like to filter data by month, day or both? Type "none" for no Time filter: '))
        
        # Get user input for month and day
        if filter_type == 'month':
            month = months[int(input('Which month? Please type your response as integer (e.g, January=1, June=6): '))]
            if 13 > months.index(month) > 6:
                while 13 > months.index(month) > 6:
                    print('Data is Not available for {}'.format(month))
                    month = months[int(input('Please enter a valid month number from January=1 to June=6: '))]
                                    
            day = 'all'
            break
            
        elif filter_type == 'day':
            day = input('Which day to analyze?: ')      
            month = 'all'
            break
                
        elif filter_type == 'both':
            month = months[int(input('Which month? Please type your response as integer (e.g, January=1, June=6): '))]
            if 13 > months.index(month) > 6:
                while 13 > months.index(month) > 6:
                    print('Data is Not available for {}'.format(month))
                    month = months[int(input('Please enter a valid month number from January=1 to June=6: '))]
                    
            day = input('Which day to analyze?: ')        
            break
                
        elif filter_type == 'none':
            month = 'all'
            day = 'all'
            break
    
        else:
            print('This response is not a valid response!')
            
    print('-'*100)
    return city, month, day


def load_data(city, month, day):
        
    data = pd.read_csv(CITY_DATA[city])
    data['Start Time'] = pd.to_datetime(data['Start Time'])
    data['month'] = data['Start Time'].dt.month
    data['day'] = data['Start Time'].dt.weekday_name
    data['hour'] = data['Start Time'].dt.hour
    
    if month != 'all':
        month =  months.index(month)
        data = data[ data['month'] == month ]
            
    if day != 'all':
        data = data[ data['day'] == day.title() ]
        
    df = data
    return df



def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    most_common_month = df['month'].value_counts().idxmax()
    mode_month = months[most_common_month]
    print('most common month: {}'.format(mode_month))
    
    mode_day = df['day'].value_counts().idxmax()
    print('most common day: {}'.format(mode_day))


    # display the most common start hour
    mchour = df['hour'].value_counts().idxmax()
    print('most common hour: {}'.format(mchour))

    print("\nThis took {} seconds.".format(round((time.time() - start_time), 4)))
    print('-'*100)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    mcsstation = df['Start Station'].value_counts().idxmax()
    print('most commonly used start station: {}'.format(mcsstation))

    mcestation = df['End Station'].value_counts().idxmax()
    print('most commonly used end station: {}'.format(mcestation))

    
    # display most frequent combination of start station and end station trip
    df["stations"] = df['Start Station'].astype(str) +" to "+ df["End Station"]
    costations = df['stations'].value_counts().idxmax()
    print('most frequent start station and end station trip: {}'.format(costations))

    print("\nThis took {} seconds.".format(round((time.time() - start_time), 4)))
    print('-'*100)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    ttt = df['Trip Duration'].sum()
    print('Total travel time: {}'.format(round(ttt,2)))

    # display mean travel time
    mtt = df['Trip Duration'].mean()
    print('Average trip duration: {}'.format(round(mtt,2)))

    print("\nThis took {} seconds.".format(round((time.time() - start_time), 4)))
    print('-'*100)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types:\n{}'.format(user_types))

    # Display counts of gender # TO DO: Display earliest, most recent, and most common year of birth
    if ('Gender' not in df.columns) and ('Birth Year' not in df.columns):
        print ('\nGender and Birth Year data is not avaliable for Washington')
    else:
        gender_types = df['Gender'].value_counts(dropna=True)
        print('\nCounts of gender:\n{}'.format(gender_types))
        
        earliest_year = np.min(df['Birth Year'])
        most_recent = np.max(df['Birth Year'])
        mo_co_year = df['Birth Year'].value_counts().idxmax()
        print("\nThe most earliest birth year: {}".format(earliest_year))
        print("The most recent birth year: {}".format(most_recent))
        print("The most common birth year: {}".format(mo_co_year))


    print("\nThis took {} seconds.".format(round((time.time() - start_time), 4)))
    print('-'*100)

def view_data(df):
    question = input('Would you like to see a sample of trip data? "yes" or "no": ')
    if question.lower() == 'yes':
        i = 0
        j = 4
        print(df.iloc[i:j,:])
        question2 = input('Would you like to see more data? "yes" or "no": ')
        while question2 == 'yes':
            if question2.lower() != 'yes':
                break 
            elif question2.lower() == 'yes':
                while question2 == 'yes':
                    i += 5
                    j = i + 4
                    print(df.iloc[i:j,:])
                    question2 = input('Would you like to see more data? "yes" or "no": ')
                

                    
def main():
    while True:
        city, month, day = get_filters()                     
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
