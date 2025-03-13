#!/usr/bin/env python
# coding: utf-8

# In[102]:


import pandas as pd 
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns 


pd.options.display.max_columns = 100 
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina')

from scipy import stats

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize as WordTokenizer

nltk.download('punkt')
from nltk.probability import FreqDist


# In[103]:


yelp_business = pd.read_csv('yelp_business.csv')
yelp_business.head()


# In[104]:


yelp_review = pd.read_csv('yelp_review.csv')
yelp_review.head()


# In[105]:


df1 = yelp_business
df2 = yelp_review


# In[106]:


merge = pd.merge(df1, df2,on = 'business_id')
merge.shape


# In[107]:


merge.head()


# In[108]:


merge.isnull().sum()


# In[109]:


df = merge.dropna()


# In[110]:


df.head()


# In[111]:


df["state"].value_counts()


# In[112]:


df = df[(df["state"] == "NV")]
df.head()
#df.to_csv("yelp_NV.csv", index=None)


# In[113]:


df.shape


# In[114]:


df_sample = df.sample(frac=0.05)
#df_sample.to_csv("yelp_NV_sample.csv", index=None)


# In[115]:


df_sample.shape


# In[116]:


df = df_sample


# In[117]:


df.head()


# In[118]:


df['text'] = df['text'].astype('string')
df["text"].dtype


# In[119]:


rest = df[df.categories.str.contains("Restaurants") | df.categories.str.contains("Bars")]
rest.head()


# In[120]:


rest.shape


# In[121]:


#rest.to_csv("yelp_NV_sample_RestandBars.csv", index=None)


# In[154]:


df = rest
df['category']=pd.Series()
# Restaurants
df.loc[df.categories.str.contains('Fast Food'),'category'] = 'Fast Food'
df.loc[df.categories.str.contains('American'),'category'] = 'American'
df.loc[df.categories.str.contains('Mexican'), 'category'] = 'Mexican'
df.loc[df.categories.str.contains('Italian'), 'category'] = 'Italian'
df.loc[df.categories.str.contains('Japanese'), 'category'] = 'Japanese'
df.loc[df.categories.str.contains('Chinese'), 'category'] = 'Chinese'
df.loc[df.categories.str.contains('Thai'), 'category'] = 'Thai'
df.loc[df.categories.str.contains('Mediterranean'), 'category'] = 'Mediterranean'
df.loc[df.categories.str.contains('French'), 'category'] = 'French'
df.loc[df.categories.str.contains('Vietnamese'), 'category'] = 'Vietnamese'
df.loc[df.categories.str.contains('Greek'),'category'] = 'Greek'
df.loc[df.categories.str.contains('German'),'category'] = 'German'
df.loc[df.categories.str.contains('Indian'),'category'] = 'Indian'
df.loc[df.categories.str.contains('Korean'),'category'] = 'Korean'
df.loc[df.categories.str.contains('Hawaiian'),'category'] = 'Hawaiian'
df.loc[df.categories.str.contains('African'),'category'] = 'African'
df.loc[df.categories.str.contains('Spanish'),'category'] = 'Spanish'
df.loc[df.categories.str.contains('Coffee'),'category'] = 'Cafe'
df.loc[df.categories.str.contains('Cafes'),'category'] = 'Cafe'
df.loc[df.categories.str.contains('Bakeries'),'category'] = 'Bakery'
df.loc[df.categories.str.contains('Vegan'),'category'] = 'Vegan'
df.loc[df.categories.str.contains('Steak'),'category'] = 'Steakhouse'
df.loc[df.categories.str.contains('Steakhouses'),'category'] = 'Steakhouse'
df.loc[df.categories.str.contains('Seafood'),'category'] = 'Seafood'
df.loc[df.categories.str.contains('Acai'),'category'] = 'Juice Bar'
df.loc[df.categories.str.contains('Smoothie'),'category'] = 'Juice Bar'
df.loc[df.categories.str.contains('Bubble Tea'),'category'] = 'Juice Bar'
df.loc[df.categories.str.contains('Barbeque'),'category'] = 'Barbeque'
df.loc[df.categories.str.contains('Sushi'),'category'] = 'Sushi'
df.loc[df.categories.str.contains('Pizza'),'category'] = 'Pizza'
df.loc[df.categories.str.contains('Ice cream'),'category'] = 'Ice Cream Parlor'
df.loc[df.categories.str.contains('Buffets'),'category'] = 'Buffets'
df.loc[df.categories.str.contains('Breakfast & Brunch'),'category'] = 'Breakfast'
df.loc[df.categories.str.contains('Burgers'),'category'] = 'Burger'
df.loc[df.categories.str.contains('Brazilian'),'category'] = 'Brazilian'
df.loc[df.categories.str.contains('Vietnamese'), 'category'] = 'Vietnamese'
df.loc[df.categories.str.contains('Hot Dogs'), 'category'] = 'Hot Dogs'
df.loc[df.categories.str.contains('Cajun/Creole'), 'category'] = 'Cajun/Creole'
df.loc[df.categories.str.contains('Sandwiches'), 'category'] = 'Sandwich'
df.loc[df.categories.str.contains('Nightlife'), 'category'] = 'Nightlife'
df.loc[df.categories.str.contains('Bars'), 'category'] = 'Nightlife'
df.loc[df.categories.str.contains('Beer'), 'category'] = 'Nightlife'
df.loc[df.categories.str.contains('Wine Bars'), 'category'] = 'Nightlife'
df.loc[df.categories.str.contains('Shopping'), 'category'] = 'Shopping center Restaurant'
df.loc[df.categories.str.contains('Hotels'), 'category'] = 'Hotel'
df.loc[df.categories.str.contains('Food Trucks'), 'category'] = 'Food Trucks'
df.loc[df.categories.str.contains('Middle Eastern'), 'category'] = 'Middle Eastern'
df.loc[df.categories.str.contains('Halal'), 'category'] = 'Middle Eastern'
df.loc[df.categories.str.contains('Moroccan'), 'category'] = 'Middle Eastern'
df.loc[df.categories.str.contains('Filipino'), 'category'] = 'Filipino'
df.loc[df.categories.str.contains('Latin American'), 'category'] = 'Latin American'
df.loc[df.categories.str.contains('American (Traditional)'),'category'] = 'American'
df.loc[df.categories.str.contains('American (New)'),'category'] = 'American'
df.loc[df.categories.str.contains('Chicken Wings'),'category'] = 'Chicken Wings'
df.loc[df.categories.str.contains('Ethiopian'),'category'] = 'Ethiopian'


# In[123]:


df["category"].value_counts()


# In[124]:


df.isnull().sum()


# In[156]:


df_categorized = df.dropna(axis=0, subset=['category'])
df_categorized.shape


# In[157]:


del df_categorized['categories']


# In[127]:


df_categorized=df_categorized.reset_index(drop=True)
df_categorized.head(10)


# In[128]:


df_categorized.columns


# In[129]:


df_categorized.to_csv('Yelp_NV_categorized.csv')


# In[130]:


df_categorized.isnull().sum()


# In[158]:


plt.figure(figsize=(15,10))
grouped = df_categorized.category.value_counts()
plt.xlabel('Number of businesses', fontsize=14, labelpad=10)
plt.ylabel('Category', fontsize=14)
plt.title('Count of businesses by Category in NV', fontsize=15)
plt.tick_params(labelsize=14)
sns.countplot(y='category',data=df_categorized, 
              order = grouped.index, palette= sns.color_palette("Set2", len(grouped)))


# In[132]:


df_categorized.head()


# In[133]:


df = df_categorized


# In[134]:


from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina')


# In[135]:


fig, ax = plt.subplots(dpi=200)
sns.countplot(data=df, y='stars_x',palette= sns.color_palette("Set2"))


# In[136]:


fig, ax = plt.subplots(dpi=200)
sns.countplot(data=df_categorized, y='stars_y',palette= sns.color_palette("Set2"))


# In[137]:


df['business_id'].value_counts


# In[138]:


fig, ax = plt.subplots(dpi=200)
sns.countplot(data=df, y='stars_y',palette= sns.color_palette("Set2"))


# In[139]:


v1 = pd.pivot_table(data=df, index=['business_id'], values='stars_x',aggfunc='mean').reset_index()

plt.figure(figsize=[10,5])
img = sns.barplot(data=v1, x='business_id', y='stars_x')


# In[140]:


df['name'].value_counts()


# In[141]:


busi5 = ['Hash House A Go Go','Bacchanal Buffet','Mon Ami Gabi','Wicked Spoon',
         'Gordon Ramsay BurGR']


# In[142]:


plt.figure(figsize=[20,10])
sns.barplot(data=df, x='name', y='stars_x', order=busi5, palette= sns.color_palette("Set2"))


# In[143]:


df['stars_x'].describe()


# In[144]:


df[df['stars_x'] < 3].count()


# In[145]:


df.groupby('stars_x').count()


# In[153]:


df['city'].value_counts(100)


# In[148]:


fig, ax = plt.subplots(dpi=200)
sns.countplot(data=df, y='city',palette= sns.color_palette("Set2"))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




