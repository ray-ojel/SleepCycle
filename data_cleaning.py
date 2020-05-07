def sleep_cleaning(dataset):
    # Import all the relvant libraries and read in the file
    import re
    import numpy as np
    import pandas as pd

    # The value separating the columns is a (;) not a comma
    sleep = pd.read_csv(dataset, delimiter = ';')

    # Change the Start, End and Time in bed columns to datetime objects
    sleep['Start'] = pd.to_datetime(arg = sleep['Start'], format = '%Y/%m/%d %H:%M:%S')
    sleep['End'] = pd.to_datetime(arg = sleep['End'], format = '%Y/%m/%d %H:%M:%S')

    # Change time from HH:MM to total hours with decimals
    def hour(time):
        time = time.split(':')
        hour = int(time[0])
        minute = int(time[1])
        time = round(hour + (minute/60), 2)
        return time

    sleep['Time in bed'] = sleep['Time in bed'].apply(hour)
    sleep.rename(columns = {'Time in bed':'Time in bed (hr)'}, inplace = True)

    # Change sleep quality column to an integer column and rename
    sleep['Sleep quality'] = sleep['Sleep quality'].str.replace('%', '').astype(int)
    sleep.rename(columns = {'Sleep quality':'Sleep quality (%)'}, inplace = True)

    # Create New columns for Start and End times and dates
    sleep.insert(1, 'End Time', sleep['End'].dt.time)
    sleep.insert(1, 'End Date', sleep['End'].dt.date)
    sleep.insert(1, 'Start Time', sleep['Start'].dt.time)
    sleep.insert(1, 'Start Date', sleep['Start'].dt.date)

    # Drop Start, End and Heart rate columns as they'r not needed anymore
    sleep = sleep.drop(columns = ['Start','End', 'Heart rate'])

    # Change the values in mood column to easier to read values
    def moods(mood):
        if pd.isnull(mood):
            return np.nan
        elif mood == ':)':
            return mood.replace(':)', 'Good')
        elif mood == ':|':
            return mood.replace(':|', 'Neutral')
        elif mood == ':(':
            return mood.replace(':(', 'Bad')
    sleep['Wake up'] = sleep['Wake up'].apply(moods)

    # Create a new stimulant column (cofee, tea or nicotine)
    pattern = r'(coffee|tea|smoked?)'
    sleep['Stimulant'] = (sleep['Sleep Notes']
                          .str.contains(pattern, flags=re.I)
                         )

    # Create a new stressful day column
    pattern2 = r'stressful'
    sleep['Stressful Day?'] = (sleep['Sleep Notes']
                               .str.contains(pattern2, flags = re.I)
                              )

    # Create a new column for naps
    sleep['Nap?'] = sleep['Time in bed (hr)'].apply(lambda x: True if x <= 3.00 else False)

    return sleep
