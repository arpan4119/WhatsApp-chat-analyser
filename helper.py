import emoji
from urlextract import URLExtract
extract = URLExtract()
def get_message_count(selected_user, df):
    if selected_user == "All Users":
        return df.shape[0]
    else:
        return df[df['User'] == selected_user].shape[0]
def get_media_count(selected_user, df):
    if selected_user == "All Users":
        return df[df['Message'] == '<Media omitted>'].shape[0]
    else:
        return df[(df['User'] == selected_user) & (df['Message'] == '<Media omitted>')].shape[0]
def get_links_count(selected_user, df):
    links = []
    if selected_user == "All Users":
        for message in df['Message']:
            links.extend(extract.find_urls(message))
    else:
        user_message = df[df['User'] == selected_user]['Message']
        for message in user_message:
            links.extend(extract.find_urls(message))
    return len(links)
def remove_emojis(all):
    words = []
    emojis = []

    for word in all:
        word_emoji = ''.join(c for c in word if c in emoji.EMOJI_DATA)
        word_text = ''.join(c for c in word if c not in emoji.EMOJI_DATA)

        if word_emoji:
            emojis.append(word_emoji)
        if word_text:
            words.append(word_text)

    return words, emojis
def get_monthly_usage(df, selected_user):
    if selected_user != "All Users":
        df = df[df['User'] == selected_user]
    
    timeline = df.groupby(['Year', 'Month_num', 'Month']).count()['Message'].reset_index()
    
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['time'] = time;
    return timeline
def get_daily_usage(df, selected_user):
    if selected_user != "All Users":
        df = df[df['User'] == selected_user]
    
    daily_usage = df.groupby(['Year', 'Month_num', 'Date']).count()['Message'].reset_index()
    
    day = []
    for i in range(daily_usage.shape[0]):
        day.append(str(daily_usage['Date'][i]) + "-" + str(daily_usage['Month_num'][i]) + "-" + str(daily_usage['Year'][i]))
    
    daily_usage['day'] = day;

    return daily_usage
def weekly_usage(df, selected_user):
    if selected_user != "All Users":
        df = df[df['User'] == selected_user]
    
    return df['Day'].value_counts()