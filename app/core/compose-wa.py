#!/usr/bin/env python
# coding: utf-8

# # compose-wa
# An prototype project for music exploration and composition.
# Contains application code for the COE 332 Final project. (I will add docstrings soon enough.)
# The element python file is the main file for now; to import routes, just do an `import element` and an `import musicpy` as necessary.
# If you need a python file, it has the same name...

# In[1]:


import element
import musicpy as mp


# In[2]:


cfr,_ = element.load('midi/Animenz_-_Crying_for_Rain.mid')


# In[3]:


x, data = element.plotAll(cfr)


# In[ ]:


mp.play(cfr)


# In[7]:


import numpy as np
np.sum(data,axis=0)


# In[6]:


cfr


# In[ ]:




