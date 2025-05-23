import streamlit as st
import matplotlib.pyplot as plt
from sympy import rotations
import matplotlib.font_manager as fm
import seaborn as sns
import preprocessor, helper

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a File")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    #extract unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        # stats area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        st.title('Top Statistics')

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total no. of messages")
            st.title(num_messages)
        with col2:
            st.header("Total no. of Words")
            st.title(words)
        with col3:
            st.header("Total no. of Media shared")
            st.title(num_media_messages)
        with col4:
            st.header("Total no. of Links shared")
            st.title(num_links)

        #monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.weak_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        # activity heatmap
        st.title("Weekly activity map")
        heatmap_data = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(heatmap_data)
        st.pyplot(fig)


        # finding the active users in group
        if selected_user == 'Overall':
            st.title('Most active users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color = 'red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


        # word cloud
        st.title("WORD CLOUD")

        df['message'] = df['message'].replace('<Media omitted>\n' , "", regex=True)
        df['message'] = df['message'].replace('This message was deleted' , "", regex=True)

        group_notifications = [
            "added", "removed", "left", "joined", "changed the subject",
            "changed this group's icon", "created group"
        ]
        df = df[~df['message'].str.contains('|'.join(group_notifications), na=False, case=False)]

        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        #most common words
        st.title('Most common words')
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        # plt.xticks(rotation = 'vertical')

        st.pyplot(fig)


        #emoji analysis

        st.title('Emoji Analysis')
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:

            plt.rcParams['font.family'] = 'Segoe UI Emoji'
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct = '%0.2f')
            st.pyplot(fig)
