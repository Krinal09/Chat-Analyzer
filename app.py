import streamlit as st
import preprocessor
import help
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

upload_file = st.sidebar.file_uploader("Choose a file", key="file_uploader")

if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    df = preprocessor.preprocess(data)
    
    if 'user' in df.columns:
        user_list = df.loc[df['user'] != 'group_notification', 'user'].unique().tolist()
        user_list.sort()
        user_list.insert(0, "Overall")
    
    select_users = st.sidebar.selectbox("Show Analysis with respect to:", user_list, key="user_select")

    if st.sidebar.button("Show Analysis", key="show_button"):
        st.title('* Top Analysis based on Statistics')
        
        num_messages, words, num_media_msg, links = help.fetch_stats(select_users, df)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        
        with col2:
            st.header("Total Words")
            st.title(words)
        
        with col3:
            st.header("Total Media")
            st.title(num_media_msg)
        
        with col4:
            st.header("All Media Links")
            st.title(links)
            
        st.title('Monthly Timeline of Chat')
        monthly_timeline = help.monthly_timeline(select_users, df)
        fig, ax = plt.subplots()
        ax.plot(monthly_timeline['time'], monthly_timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        st.title('Daily Timeline of Chat')
        daily_timeline = help.daily_timeline(select_users, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = help.week_activity_map(select_users, df)
            busy_day_sorted = busy_day.sort_values(ascending=False)
            fig, ax = plt.subplots()
            ax.bar(busy_day_sorted.index, busy_day_sorted.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        with col2:
            st.header("Most Busy Month")
            busy_month = help.month_activity_map(select_users, df)
            busy_month_sorted = busy_month.sort_values(ascending=False)
            fig, ax = plt.subplots()
            ax.bar(busy_month_sorted.index, busy_month_sorted.values, color="orange")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        st.title("Weekly Activity Map")
        user_heatmap = help.activity_heatmap(select_users, df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heatmap, ax=ax)
        st.pyplot(fig)
        
        if select_users == "Overall":
            st.title("Most Busy User")
            x, new_df = help.fetch_most_busy(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            
            with col1:
                ax.bar(x.index, x.values, color="violet")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
                
            with col2:
                st.dataframe(new_df)
        
        st.title("WordCloud")
        df_wc = help.create_wordcloud(select_users, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        st.title('Most Common Words')
        most_common_df = help.most_common_words(select_users, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        st.title('Emojis that are Used')
        emoji_df = help.most_emojis(select_users, df)
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(emoji_df)
            
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
