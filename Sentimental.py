#!/usr/bin/env python
# coding: utf-8

# In[75]:


from IPython.display import Image
Image(filename='beef36fd707d.jpg')


# ### Twitter Data Sentiment Analysis
# - 1) Twitter Data:- First step is to configure twitter API and gather twitter data
# - 2) Clean the data
# - 3) Sentiment:- To find out sentiments
# - 4) Analysis:- To do analysis

# In[47]:


import tweepy 
from textblob import TextBlob #sentimnts library
import pandas as pd
import matplotlib.pyplot as plt

from wordcloud import WordCloud
plt.style.use('fivethirtyeight')


# In[2]:


APIKey="W2XtGXNhNK9M03XcEA9LLVa17"
APISecretKey="J7wmwyKXxBfaOmn2LVtLloP28NJWcrUR6L2MQeqn8VFAjC6nQO"
accessToken="1387284148713234445-21fcTuPB6LTh6Zyi9Zxb5zxrxEIu8N"
accessTokenSecret="UK4vgiRYtjkev6c3JouvqXkv4Z0FQD3fsmbPYHPJFiItG"


# In[3]:


### Authenticate
authenticate= tweepy.OAuthHandler(APIKey,APISecretKey)
authenticate.set_access_token(accessToken,accessTokenSecret)
api=tweepy.API(authenticate)


# In[4]:


posts=api.user_timeline(screen_name='Trump',count=100,lang="en",tweet_mode='extended')
i=1
for tweet in posts[:10]:
    print(str(i)+')'+ tweet.full_text+'\n')
    i=i+1


# In[9]:


# Create a dataframe with a column called tweets
df=pd.DataFrame([tweet.full_text for tweet in posts],columns=['Tweets'])


# In[10]:


df


# In[31]:


def cleanTxt(text):
    text=re.sub('@[a-zA-Z0-9]*','',text)
    text=re.sub("#",'',text)
    text=re.sub('RT[\s]+','',text)
    text=re.sub('https?:\/\/\S+','',text)
    return text


# In[32]:


df['Tweets']=df['Tweets'].apply(cleanTxt)


# In[33]:


df


# In[43]:


analysis=TextBlob("Today was the beautiful day")


# In[44]:


analysis.sentiment


# In[34]:


# create a function to get the subjectivity of all the tweets
def getSubject(text):
    return TextBlob(text).sentiment.subjectivity
# create a function to get the Polarity of all the tweets
def getPolar(text):
    return TextBlob(text).sentiment.polarity

#create columns subj and polar
df['Subjectivity']=df['Tweets'].apply(getSubject)
df['Polarity']=df['Tweets'].apply(getPolar)


# In[48]:


df


# #  Do Analysis

# In[35]:


#WordCloud Visualization
allwords = ''.join([i for i in df['Tweets']])
Cloud=WordCloud(random_state=0,max_font_size=100,width=500,height=300).generate(allwords)
plt.imshow(Cloud)
plt.show()


# In[37]:


# Create a fucntion to compute negative neutral postive comments
def getAnalysis(score):
    if score<0:
        return 'negative'
    elif score==0:
        return 'Neutral'
    else:
        return 'Positive'
df['Analysis']=df['Polarity'].apply(getAnalysis)
df


# In[41]:


df[df['Analysis']=='negative']


# In[42]:


df['Analysis'].value_counts()


# In[53]:


## plotting scatter plot
for i in range(0,df.shape[0]):
    plt.scatter(df['Polarity'][i],df['Subjectivity'][i],color='Blue')
    
plt.title("Sentiment Analysis")
plt.xlim(-1,1)
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')
plt.figure(figsize=(8,6))


# In[59]:


df['Analysis'].value_counts().plot(kind='bar')

plt.title("Sentimental Analysis")
plt.xlabel('Polarity')
plt.ylabel('Count')
plt.show()


# ### Only Positive tweets

# In[65]:


i=1
postdf=df.sort_values(by=['Polarity'],ascending=False)
for j in range(0,postdf.shape[0]):
    if(postdf['Analysis'][j]=='Positive'):
        print(str(i)+')'+postdf['Tweets'][j])
        print()
        i=i+1


# ### Only Negative Comments

# In[67]:


i=1
postdf=df.sort_values(by=['Polarity'])
for j in range(0,postdf.shape[0]):
    if(postdf['Analysis'][j]=='negative'):
        print(str(i)+')'+postdf['Tweets'][j])
        print()
        i=i+1


# ### Neutral Comments

# In[69]:


i=1
postdf=df.sort_values(by=['Polarity'])
for j in range(0,postdf.shape[0]):
    if(postdf['Analysis'][j]=='Neutral'):
        print(str(i)+')'+postdf['Tweets'][j])
        print()
        i=i+1


# In[ ]:




