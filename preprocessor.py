import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s?(?:am|pm)\s?-\s'

    messages = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)
    dates = [date.replace("\u202f", " ") for date in dates]

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # converting msg_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')
    df['message_date'] = df['message_date'].dt.strftime('%d/%m/%Y, %I:%M %p')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'(^[\w\s~+.\d()]+?):\s', message, maxsplit=1)  # Updated regex

        if len(entry) > 2:  # If a username is detected
            if "joined using this group's invite link" in entry[2] or "You joined a group" in entry[1]:
                users.append("group_notification")  # Correct classification
                messages.append(entry[1] + entry[2])
            else:
                users.append(entry[1])  # Extract name or number
                messages.append(entry[2])  # Extract message
        else:
            users.append("group_notification")  # Ensure all unknown cases fall under group notifications
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)



    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %I:%M %p')

    df['year'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %I:%M %p').dt.year

    df['only_date'] = df['date'].dt.date
    df['date'] = df['date'].dt.strftime('%d/%m/%Y, %I:%M %p')

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %I:%M %p')

    df['month'] = df['date'].dt.month_name()

    df['month_num'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.strftime('%I')
    df['minute'] = df['date'].dt.strftime('%M')
    df['am_pm'] = df['date'].dt.strftime('%p')
    df['date'] = df['date'].dt.strftime('%d/%m/%Y, %I:%M %p')

    period = []
    for hour in df[['day_name', 'hour']]['hour']:  # Correcting column selection
        hour = int(hour)  # Ensure it's an integer

        start_hour = hour % 12
        start_hour = 12 if start_hour == 0 else start_hour  # Convert 0 to 12
        end_hour = (hour + 1) % 12
        end_hour = 12 if end_hour == 0 else end_hour  # Convert 0 to 12

        am_pm_start = "AM" if hour < 12 else "PM"
        am_pm_end = "AM" if (hour + 1) < 12 else "PM"

        period.append(f"{start_hour}{am_pm_start}-{end_hour}{am_pm_end}")

    df['period'] = period

    return df