#!/usr/bin/env python
# coding: utf-8

# In[1]:


import import_ipynb


# In[2]:


from flask import Flask,request,jsonify
from flask_cors import CORS
import recommendation1


# In[3]:


app = Flask(__name__)
CORS(app) 


# In[ ]:


@app.route('/')
def recommend_tourists_places():
        return 'NO Places Found'

@app.route('/places', methods=['GET'])
def recommend_places():
        res = recommendation1.results(request.args.get('name'))
        return jsonify(res)

if __name__=='__main__':
        app.run(debug = True, use_reloader = False)


# In[ ]:




