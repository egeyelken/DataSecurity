#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

df = pd.read_csv('adult.csv')


# In[2]:


df = df[df.age.astype(str) != '?']
df = df[df.workclass.astype(str) != '?']
df = df[df.education.astype(str) != '?']
#df = df[df.marital_status.astype(str) != '?']
df = df[df.occupation.astype(str) != '?']
df = df[df.relationship.astype(str) != '?']
df = df[df.race.astype(str) != '?']
df = df[df.gender.astype(str) != '?']
df = df[df.income.astype(str) != '?']

# some column names gave an error so I tried another method
indexMarital = df[df['marital-status'].astype(str) == '?'].index
df.drop(indexMarital, inplace=True)
indexHours = df[df['hours-per-week'].astype(str) == '?'].index
df.drop(indexHours, inplace=True)
indexNative = df[df['native-country'].astype(str) == '?'].index
df.drop(indexNative, inplace=True)


# In[3]:


import random
import math

def laplace_noise(mean, scale, epsilon):
    #x = random.randint(-10, 10)
    x = 1 / epsilon
    out = (1 / (2 * scale)) * math.exp(- abs(x - mean) / scale)
    return out 


# In[4]:


#Original Histogram
dfedu = df[df.income.astype(str) == '>50K']
dfedu = dfedu.education
dfedu.hist(figsize = (80,50), xlabelsize = 50, ylabelsize = 50, bins = 50)


# In[5]:


#Generate a neighboring dataset
df_n = df.drop(random.randint(0, 45222)) 
#Only keep the ones with high income and the education column
dfedu = df_n[df_n.income.astype(str) == '>50K']
dfedu = dfedu.education
#dfedu.hist(figsize = (80,50), xlabelsize = 50, ylabelsize = 50, bins = 50)

#Generate a dictionary before adding noise
dfedu = list(dfedu)
setd = set(dfedu)
dgrs = dict()
for i in range(len(dfedu)):
    if (dfedu[i] not in dgrs.keys()):
        dgrs[dfedu[i]] = 0
    else:
        dgrs[dfedu[i]] = dgrs[dfedu[i]] + 1  

dgrs


# In[6]:


#Adding the noise with mean = 0, scale = 10 and epsilon = 0.01
dgrs1 = dict()
for d in dgrs:
    dgrs1[d] = dgrs[d] + laplace_noise(0, 10, 0.01)

dgrs1


# In[7]:


import matplotlib.pyplot as plt


plt.bar(range(len(dgrs1)), list(dgrs1.values()), align='center')
plt.xticks(range(len(dgrs1)), list(dgrs1.keys()))
plt.rcParams["figure.figsize"] = [80,50]
plt.show()

#Histograms are very similar because the added noise is very small


# In[8]:


def err(d1, d2):
    sum = 0
    for i in d1:
        
        sum = sum + abs(d1[i] - d2[i])
    return sum/len(d1)      


# In[9]:


print("Average error with epsilon = 0.01 is:", err(dgrs, dgrs1))


# In[10]:


#for 0.05, 0.1, 0.5, 1.0
dgrs2 = dict()
for d in dgrs:
    dgrs2[d] = dgrs[d] + laplace_noise(0, 10, 0.05)
print("Average error with epsilon = 0.05 is:", err(dgrs, dgrs2))

dgrs3 = dict()
for d in dgrs:
    dgrs3[d] = dgrs[d] + laplace_noise(0, 10, 0.1)
print("Average error with epsilon = 0.1 is:", err(dgrs, dgrs3))

dgrs4 = dict()
for d in dgrs:
    dgrs4[d] = dgrs[d] + laplace_noise(0, 10, 0.5)
print("Average error with epsilon = 0.5 is:", err(dgrs, dgrs4))

dgrs5 = dict()
for d in dgrs:
    dgrs5[d] = dgrs[d] + laplace_noise(0, 10, 1.0)
print("Average error with epsilon = 1.0 is:", err(dgrs, dgrs5))

#As the epsilon grows, noise and thus the error grows proportionally by definition.


