from urlextract import URLExtract
import matplotlib.pyplot as plt
import app
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract() 

def fetch_stats(select_users,df):
    
    if select_users != "Overall":
        df = df[df['user'] == select_users]
        
    num_message = df.shape[0]
    
    words = []
    for message in df['message']:
            words.extend(message.split())
            
    # fetch number of messages
    num_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]


    # fetch numbers of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))



    return num_message,len(words), num_media_msg, len(links)

def fetch_most_busy(df):
    
    x = df['user'].value_counts().head()
    
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns = {'index' : 'name', 'user' : 'percent'})
    
    # name = X.index
    # count = X.values

    # plt.bar(name,count)
    # plt.xticks(rotation = 'vertical')
    # plt.show()

    return x, df

def create_wordcloud(select_users, df):
    
    if select_users != "Overall":
        df = df[df['user'] == select_users]
        
    with open('stop_hinglish-guj.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read()
    # print(stop_words) 
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != '<Media omitted>']
    
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        
        return " ".join(y)
        
        
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color = 'aqua')
    
    temp['message'] = temp['message'].apply(remove_stop_words)
    
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    
    return df_wc

def most_common_words(select_users,df):
    
    # this is for any english characters 
    # f = open('stop_hinglish.txt','r')
    # stop_words = f.read()
    # print(stop_words)

    # this is for also have gujarati stop words
    with open('stop_hinglish-guj.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read()
    # print(stop_words) 
    
    
    if select_users != "Overall":
        df = df[df['user'] == select_users]
        
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != '<Media omitted>']
    
    
    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.extend(message.split())
                
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    
    return most_common_df

def most_emojis(select_users,df):
    
    if select_users != "Overall":
        df = df[df['user'] == select_users]
        
        
    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
            
    return emoji_df    
        
def monthly_timeline(select_users,df):
    
    if select_users != "Overall":
        df = df[df['user'] == select_users]
        
    monthly_timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    
    time = []
    for i in range(monthly_timeline.shape[0]):
        time.append((monthly_timeline['month'][i] + "-" + str(monthly_timeline['year'][i])))    
    
    monthly_timeline['time'] = time
    
    return monthly_timeline
        
def daily_timeline(select_users, df):
    
    if select_users != "Overall":
        df = df[df['user'] == select_users]
    
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    
    plt.figure(figsize = (18,10))
    plt.plot(daily_timeline['only_date'], daily_timeline['message'])  
    
    return daily_timeline
    
    
def week_activity_map(select_users, df):
    
    if select_users != "Overall":
        df = df[df['user'] == select_users]
        
    return df['day_name'].value_counts()  
    
def month_activity_map(select_users, df):
        
    if select_users != "Overall":
        df = df[df['user'] == select_users]
        
    return df['month'].value_counts()  

def activity_heatmap(select_users, df):
    
    if select_users != "Overall":
        df = df[df['user'] == select_users]
        
        
    user_heatmap = df.pivot_table(index = 'day_name', columns = 'period', values = 'message', aggfunc='count').fillna(0)

    return user_heatmap
        
        
        
        
        
        








    
    # if select_users == "Overall":
        
    #     # 1. number of messages
    #     num_message = df.shape[0]
        
    #     # 2. number of words
    #     words = []
    #     for message in df['message']:
    #         words.extend(message.split())
        
    #     return num_message,len(words)
    
    # else:
        
    #     new_df = df[df['user'] == select_users]
    #     num_message = new_df.shape[0]
        
    #     words = []
    #     for message in new_df['message']:
    #         words.extend(message.split())
            
    #     return num_message, len(words)