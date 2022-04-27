#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[2]:


def get_data():
    places_data = pd.read_excel("tourist_places_data.xlsx")
    places_data['name'] = places_data['name'].str.lower()
    return places_data


# In[3]:


get_data()


# In[4]:


def combine_data(data):
    data_recommend = data
    data_recommend['combine'] = data_recommend[data_recommend.columns[0:4]].apply(
                                                                         lambda x: ','.join(x.dropna().astype(str)),axis=1)
    data_recommend = data.drop(columns = ['name','address','desc','image'])
    return data_recommend


# In[5]:


def transform_data(data_combine, data_plot):
        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(data_combine['combine'])

        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(data_plot['desc'])

        combine_sparse = sp.hstack([count_matrix, tfidf_matrix], format='csr')
        cosine_sim = cosine_similarity(combine_sparse, combine_sparse)
        
        return cosine_sim


# In[6]:


def recommend_places(title, data, combine, transform):
        indices = pd.Series(data.index, index = data['name'])
        index = indices[title]
        
        sim_scores = list(enumerate(transform[index]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[0:10]


        places_indices = [i[0] for i in sim_scores]

        places_title = data['name'].iloc[places_indices]
        places_desc = data['desc'].iloc[places_indices]
        places_add = data['address'].iloc[places_indices]
        places_image = data['image'].iloc[places_indices]

        recommendation_data = pd.DataFrame(columns=['Name', 'Description', 'Address', 'Image'])

        recommendation_data['Name'] = places_title
        recommendation_data['Description'] = places_desc
        recommendation_data['Address'] = places_add
        recommendation_data['Image'] = places_image

        return recommendation_data


# In[7]:


def results(place_name):
        place_name = place_name.lower()

        find_place = get_data()
        combine_result = combine_data(find_place)
        transform_result = transform_data(combine_result,find_place)

        if place_name not in find_place['name'].unique():
                return 'Place not in Database'

        else:
                recommendations = recommend_places(place_name, find_place, combine_result, transform_result)
                return recommendations.to_dict('records')


# In[8]:


results('panshet waterpark')


# In[ ]:




