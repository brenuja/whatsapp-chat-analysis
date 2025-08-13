import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
from imojify import imojify

extractor = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the no. of messages
    num_messages = df.shape[0]

    # fetch the total no. of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch no. of media message
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch links
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].isin(["<Media omitted>\n", "This message was deleted\n"])]

    x = temp['user'].value_counts().head()
    df = temp['user'].value_counts(normalize=True).mul(100).round(2).reset_index()
    df.columns = ['name', 'percentage%']
    
    return x, df

def create_wordcloud(selected_user, df):

     if selected_user != 'Overall':
         df = df[df['user'] == selected_user]

     wc = WordCloud(width = 500, height=500, min_font_size=10, background_color='white')
     df_wc = wc.generate(df['message'].str.cat(sep=" "))
     return df_wc


def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

#new func
def emoji_helper_with_imojify(selected_user, df):
    """
    Enhanced emoji helper function that works better with imojify
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        # Extract emojis from message
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    if not emojis:
        return pd.DataFrame(columns=[0, 1])  # Return empty DataFrame with correct columns
    
    emoji_counts = Counter(emojis)
    
    # Filter out emojis that might not be supported by imojify
    supported_emojis = {}
    for emoji_char, count in emoji_counts.items():
        try:
            # Test if imojify can handle this emoji
            img_path = imojify.get_img_path(emoji_char)
            if img_path:
                supported_emojis[emoji_char] = count
        except:
            # Skip emojis that imojify can't handle
            continue
    
    if not supported_emojis:
        return pd.DataFrame(columns=[0, 1])
    
    emoji_df = pd.DataFrame(list(supported_emojis.items()), columns=[0, 1])
    emoji_df = emoji_df.sort_values(by=1, ascending=False).reset_index(drop=True)
    
    return emoji_df


def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def weak_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    heatmap_data = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return heatmap_data


