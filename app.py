#!/usr/bin/env python
# coding: utf-8

# In[1]

# In[2]:


from flask import Flask,request,jsonify
from flask_cors import CORS
import recommendation1


# In[3]:


app = Flask(__name__)
CORS(app) 


# In[4]:


@app.route('/places', methods=['GET'])
def recommend_movies():
        res = recommendation1.results(request.args.get('name'))
        return jsonify(res)

if __name__=='__main__':
        app.run(port = 5000, debug = True)


# In[ ]:




