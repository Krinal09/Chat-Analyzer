import streamlit as st
import preprocessor
import help
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer") 

upload_file = st.sidebar.file_uploader("Choose a file")

if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    
    df = preprocessor.preprocess(data)
    
    # fetch unique users
    # user_list = df['user'].unique().tolist()
    
    # user_list.remove('group_notification')
    # user_list.sort()
    # user_list.insert(0, "Overall")
    
    
    if 'user' in df.columns:
    
        user_list = df.loc[df['user'] != 'group_notification', 'user'].unique().tolist()
    
        user_list.sort()
        
        user_list.insert(0, "Overall")
    
    
    select_users = st.sidebar.selectbox("Show Analysis with respect to:", user_list)
    
    if st.sidebar.button("Show"):
        
        st.title('* Top Analysis based on statastics')
        
        num_messages, words, num_media_msg, links = help.fetch_stats(select_users,df)
        
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
            st.header("All Media links")
            st.title(links)
            
        # monthly timeline
        
        monthly_timeline = help.monthly_timeline(select_users, df)
        
        st.title('Monthly Timeline of chat')
        
        fig, ax = plt.subplots()
        
        ax.plot(monthly_timeline['time'], monthly_timeline['message'], color='green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        
        
        # daily timeline
        
        daily_timeline = help.daily_timeline(select_users, df)
        
        st.title('Daily Timeline of chat')
        
        fig, ax = plt.subplots()
        
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        
        #### activity map 
        
        # st.title('Activity Map')
        
        # col1, col2 = st.columns(2)
        
        # with col1:
            # st.header("Most busy day")
            # busy_day = help.week_activity_map(select_users, df)
            
            # fig, ax = plt.subplots()
            # ax.bar(busy_day.index, busy_day.sort_values)
            # st.pyplot(fig)
            
            
        st.title('Activity Map')

        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = help.week_activity_map(select_users, df)  # Assuming this returns a Series or DataFrame with index as days and values as counts
            
            # Ensure busy_day is sorted by values
            busy_day_sorted = busy_day.sort_values(ascending=False)
            
            fig, ax = plt.subplots()
            ax.bar(busy_day_sorted.index, busy_day_sorted.values)
            plt.xticks(rotation='vertical')
            # plt.xlabel('Days')
            # plt.ylabel('Frequency')
            # plt.title('Most Busy Days')
            st.pyplot(fig)    
            
        with col2:
            
            st.header("Most Busy Month")
            busy_month = help.month_activity_map(select_users, df)  # Assuming this returns a Series or DataFrame with index as days and values as counts
            
            busy_day_sorted = busy_month.sort_values(ascending=False)
            
            fig, ax = plt.subplots()
            ax.bar(busy_day_sorted.index, busy_day_sorted.values, color = "orange")
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)    
            
            
        # activity heatmap
        st.title("Weekly activity Map")
        user_heatmap = help.activity_heatmap(select_users, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
            
        
        
        
        
            
        # find busiest user in the group (only in group level)
        if select_users == "Overall":
            st.title("Most busy user")
            
            x,new_df = help.fetch_most_busy(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)
            
            
            with col1:
                ax.bar(x.index, x.values, color="violet")
                plt.xticks(rotation = "vertical")
                
                st.title('Most Common Words')
                st.pyplot(fig)
                
            with col2:
                st.dataframe(new_df)
            
            
        # wordcloud
        st.title("WordCloud")
        df_wc = help.create_wordcloud(select_users, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        
        # most common words
        
        most_common_df =  help.most_common_words(select_users,df)
        
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation = 'vertical')
        
        st.title('Most common words')
        st.pyplot(fig)
        
        # st.dataframe(most_common_df)
        
        
        # emojis analysis
        
        emoji_df = help.most_emojis(select_users,df)
        
        st.title('Emojis that are used')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(emoji_df)
            
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)