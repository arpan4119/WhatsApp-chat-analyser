import re
import pandas as pd
from datetime import datetime

def extract_user(message):
    if ':' in message:
        return message.split(':', 1)[0].strip()
    else:
        return 'WhatsApp'

def parse_date(date_string):
    # Try parsing with the first format
    try:
        return datetime.strptime(date_string, '%d/%m/%Y, %I:%M %p - ')
    except ValueError:
        # If the first format fails, try the second format
        try:
            return datetime.strptime(date_string, '%d/%m/%y, %I:%M %p - ')
        except ValueError:
            # Handle any unrecognized formats
            print(f"Unrecognized date format: {date_string}")
            return None

def processFile(data):
    pattern = r'\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}\s?(?:am|pm)\s?-\s?|\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\s?(?:am|pm)\s?-\s?'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'User': messages, 'Message': messages, 'Time': dates})

    df['User'] = df['User'].apply(extract_user)
    df['Message'] = df['Message'].apply(lambda x: x.split(':', 1)[1].strip() if ':' in x else x.strip())

    # Use the custom parse_date function to handle different formats
    df['Time'] = df['Time'].apply(parse_date)

    df['Year'] = df['Time'].dt.year
    df['Month'] = df['Time'].dt.month_name()
    df['Month_num'] = df['Time'].dt.month
    df['Date'] = df['Time'].dt.day
    df['Hour'] = df['Time'].dt.hour
    df['Minute'] = df['Time'].dt.minute
    df['Day'] = df['Time'].dt.day_name()

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['Day'] = pd.Categorical(df['Day'], categories=day_order, ordered=True)
    df['Period'] = df['Hour'].apply(lambda x: f"{x:02d}-{(x + 1) % 24:02d}")
    return df
