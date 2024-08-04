import streamlit as st
import re
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import preprocessor, helper
from wordcloud import WordCloud
from collections import Counter

def all_details(df, selected_user):
        st.title("All Details")
        col1, col2, col3 = st.columns(3)
        message_count = helper.get_message_count(selected_user, df)
        with col1:
            st.header("Total Messages")
            st.title(message_count)

        media_count = helper.get_media_count(selected_user, df)
        with col2:
            st.header("Media & Stickers")
            st.title(media_count)

        links_count = helper.get_links_count(selected_user, df)
        with col3:
            st.header("Links Shared")
            st.title(links_count)
def timeline(df, selected_user):
    st.title("Timeline")
    col1, col2, = st.columns(2)
    with col1:
        st.header("Monthly Timeline")
        usage = helper.get_monthly_usage(df, selected_user)
        fig, ax = plt.subplots()
        ax.plot(usage['time'], usage['Message'], color = "purple")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        st.header("Daily Timeline")
        usage = helper.get_daily_usage(df, selected_user)
        fig, ax = plt.subplots()
        ax.plot(usage['day'], usage['Message'])
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
def usage_chart(df, selected_user):
    st.title("Usage Chart")
    col1, col2 = st.columns(2)
    
    if selected_user != "All Users":
        df = df[df['User'] == selected_user]
    
    with col1:
        st.header("Active Days Bar Chart")
        
        busy_day = df['Day'].value_counts()
        fig, ax = plt.subplots()
        ax.bar(busy_day.index, busy_day.values, color="pink")
        ax.set_xlabel('Day')
        ax.set_ylabel('Message Count')
        ax.set_title('Messages per Day')
        st.pyplot(fig)
    
    with col2:
        st.header("Active Hours Bar Chart")
        
        busy_hours = df['Hour'].value_counts()

        fig, ax = plt.subplots()
        ax.bar(busy_hours.index, busy_hours.values, color = "teal")
        ax.set_xlabel('Hour')
        ax.set_ylabel('Message Count')
        ax.set_title('Messages per Hour')

        ax.set_xticks(range(24))

        st.pyplot(fig)
def find_frequent_users(df, selected_user):
    if selected_user == "All Users":
        st.title("Most Frequent Messages(Top 5 Users)")
        col1, col2 = st.columns(2)
        top_users = df['User'].value_counts().head()
        user_counts = df['User'].value_counts()
        user_percentage = round((user_counts / df.shape[0]) * 100, 2)
        top_users_percentage = user_percentage.head().reset_index()
        top_users_percentage.columns = ['User', 'Percentage']

        # Plotting
        fig, ax = plt.subplots()
        with col1:
            ax.bar(top_users.index, top_users.values, color="red")
            ax.set_xlabel("Users")
            ax.set_ylabel("Message Count")
            ax.set_title("Top 5 Users by Message Count")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        # Display the percentage data
        with col2:
            st.dataframe(top_users_percentage)
def create_wordcloud(df, selected_user):
    if selected_user != "All Users":
        df = df[df['User'] == selected_user]

    st.title("Word Cloud")

    # Filter out messages containing "Media omitted"
    df_filtered = df[~df['Message'].str.contains("Media omitted", case=False, na=False)]

    # Combine all messages into a single string
    combined_text = df_filtered['Message'].str.cat(sep=" ")

    # Check if the combined text is empty
    if not combined_text.strip():
        st.warning("No text available to generate a word cloud.")
        return

    # Generate word cloud
    wc = WordCloud(width=500, height=500, background_color='white').generate(combined_text)

    # Plot word cloud
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
def find_most_used(df, selected_user):
    if selected_user != "All Users":
        df = df[df['User'] == selected_user]
    else:
        df = df[df['User'] != 'WhatsApp']
    
    df_filtered = df[~df['Message'].str.contains("Media omitted", case=False, na=False)]
    all = []
    for message in df_filtered['Message']:
        all.extend(message.split())
    words , emojis = helper.remove_emojis(all)

    most_common_words = pd.DataFrame(Counter(words).most_common(50), columns=['Word', 'Count'])
    most_common_emojis = pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', 'Count'])

    col1, col2 = st.columns(2)
    with col1:
        st.header("Most Used Words")
        st.dataframe(most_common_words)
    with col2:
        st.header("Most Used Emojis")
        st.dataframe(most_common_emojis)
    
    st.title("Top 20 Most Used Words")
    most_common_words = most_common_words[0:20]
    fig_words, ax_words = plt.subplots()
    ax_words.barh(most_common_words['Word'], most_common_words['Count'], color='yellow')
    ax_words.set_xlabel('Count')
    ax_words.set_ylabel('Word')
    ax_words.set_title('Top 20 Most Common Words')
    ax_words.invert_yaxis()
    st.pyplot(fig_words)
def activity_map(df, selected_user):
    st.title("Activity map")
    if selected_user != "All Users":
        df = df[df['User'] == selected_user]
    
    heat_map = df.pivot_table(index='Day', columns='Period', values='Message', aggfunc='count').fillna(0)
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.heatmap(heat_map, cmap='YlGn', ax=ax)
    ax.set_xlabel('Period')
    ax.set_ylabel('Day')
    ax.set_title(f'Activity Map for {selected_user}')

    st.pyplot(fig)
def run_chat_analyser():
    st.sidebar.title("Chat Analyser")

    uploaded_file = st.sidebar.file_uploader("Upload a File")

    if uploaded_file is None:
        st.info("Please upload a file.")
        return
    file_name = uploaded_file.name
    match = re.search(r"WhatsApp Chat with (.+?)\.txt", file_name)
    if match:
        contact_name = match.group(1)
        st.title(f"Chat Name: {contact_name}")
    else:
        st.warning("Could not extract contact name from file name.")
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.processFile(data)

    users_list = df['User'].unique().tolist()
    users_list.remove('WhatsApp')
    users_list.sort()
    users_list.insert(0, "All Users")
    selected_user = st.sidebar.selectbox("Select User", users_list)

    
    if st.sidebar.button("Show User Analysis"):
        all_details(df, selected_user)
        timeline(df, selected_user)
        usage_chart(df, selected_user)
        activity_map(df, selected_user)
        find_frequent_users(df, selected_user)
        create_wordcloud(df, selected_user)
        find_most_used(df, selected_user)

if __name__ == "__main__":
    run_chat_analyser()
