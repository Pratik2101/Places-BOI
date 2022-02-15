#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[9]:


def get_data():
    movie_data = pd.read_excel("data_places.xlsx")
    movie_data['name'] = movie_data['name'].str.lower()
    return movie_data


# In[10]:


get_data()


# In[11]:


def combine_data(data):
    data_recommend = data
    data_recommend['combine'] = data_recommend[data_recommend.columns[0:4]].apply(
                                                                         lambda x: ','.join(x.dropna().astype(str)),axis=1)
    data_recommend = data.drop(columns = ['name','address','desc','image'])
    return data_recommend


# In[12]:


def transform_data(data_combine, data_plot):
        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(data_combine['combine'])

        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(data_plot['desc'])

        combine_sparse = sp.hstack([count_matrix, tfidf_matrix], format='csr')
        cosine_sim = cosine_similarity(combine_sparse, combine_sparse)
        
        return cosine_sim


# In[13]:


def recommend_movies(title, data, combine, transform):
        indices = pd.Series(data.index, index = data['name'])
        index = indices[title]
        
        sim_scores = list(enumerate(transform[index]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:21]


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


# In[16]:


def results(place_name):
        place_name = place_name.lower()

        find_place = get_data()
        combine_result = combine_data(find_place)
        transform_result = transform_data(combine_result,find_place)

        if place_name not in find_place['name'].unique():
                return 'Place not in Database'

        else:
                recommendations = recommend_movies(place_name, find_place, combine_result, transform_result)
                return recommendations.to_dict('records')


# In[17]:


results('osho ashram')


# In[ ]:




