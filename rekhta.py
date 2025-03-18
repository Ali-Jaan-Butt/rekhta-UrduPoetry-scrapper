#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from scrapy import Selector
import pandas as pd
from tqdm import tqdm


# In[5]:


name = input('Enter the name of poet: ').split()
file = input('Enter the file name: ')


# In[6]:


ghazal_url = []


# In[7]:


if len(name)==3:
    res = requests.get('https://www.rekhta.org/poets/'+name[0]+'-'+name[1]+'-'+name[2]+'?lang=ur')
else:
    res = requests.get('https://www.rekhta.org/poets/'+name[0]+'-'+name[1]+'?lang=ur')
sel = Selector(text=res.text)
full = sel.xpath('//div[@class="readFullBgBtn"]/a/@href').extract_first()
if full!=None:
    res = requests.get(full)
    sel = Selector(text=res.text)
    for i in sel.xpath('//div[@class="contentListItems nwPoetListBody"]/a/@href').extract():
        ghazal_url.append(i)
    load_more = sel.xpath('//div[@class="contentLoadMore"]/div/@data-url').extract()
    if load_more!=[]:
        load_more_url =['https://www.rekhta.org'+i for i in load_more]
        for j in load_more_url:
            res = requests.get(j)
            sel = Selector(text=res.text)
            for k in sel.xpath('//div[@class="contentListItems nwPoetListBody"]/a/@href').extract():
                ghazal_url.append(k)
    else:
        for k in sel.xpath('//div[@class="contentListItems nwPoetListBody"]/a/@href').extract():
            ghazal_url.append(k)
else:
    for k in sel.xpath('//div[@class="contentListItems nwPoetListBody"]/a/@href').extract():
        ghazal_url.append(k)


# In[8]:


lines = {'Shyr':[],'Name':[],'Emotion 1':[],'Emotion 2':[]}


# In[9]:


for gh in tqdm(ghazal_url):
    res = requests.get(gh)
    sel = Selector(text=res.text)
    poet_name = sel.xpath('//a[@class="ghazalAuthor"]/text()').extract_first()
    for l in sel.xpath('//div[@class="w"]'):
        one = l.xpath('./div/p/span/text()').extract()
        one = ' '.join(one)
        lines['Shyr'].append(one)
        lines['Name'].append(poet_name)
        lines['Emotion 1'].append(None)
        lines['Emotion 2'].append(None)


# In[10]:


df = pd.DataFrame(lines)
df.to_csv(file+'.csv', index=False, encoding='utf-8-sig')


# In[11]:


def is_urdu_text(txt):
    urdu_characters = [u'\u0600', u'\u06FF']
    urdu_count = sum(1 for char in txt if char >= urdu_characters[0] and char <= urdu_characters[1])
    return urdu_count / len(txt) > 0.5


# In[12]:


def remove_english_rows(csv_file):
    df = pd.read_csv(csv_file)
    df['Is_Urdu'] = df['Shyr'].apply(is_urdu_text)
    df = df[df['Is_Urdu'] == True]
    df.drop(columns=['Is_Urdu'], inplace=True)
    df.to_csv(file+'.csv', index=False, encoding='utf-8-sig')


# In[13]:


remove_english_rows(file+'.csv')

