#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os
import re
import collections

# 1) Reading Inputs
def read_data(filename):
    return pd.read_csv(filename)
    
def read_DGHS(directory):
    dghs = []
    for file in os.listdir(directory):
        dghs.append(file)
    return dghs

data = read_data('adult.csv')
dghs = read_DGHS('DGHs')

data
dghs


# In[2]:


# 2) Data Pre-processing
data.shape   #(48842, 11) before cleaning

data = data[['education', 'gender', 'marital-status', 'native-country', 'occupation', 'relationship', 'workclass', 'income']]

data = data[data.education.astype(str) != '?']
data = data[data.gender.astype(str) != '?']
data = data[data.occupation.astype(str) != '?']
data = data[data.relationship.astype(str) != '?']
data = data[data.workclass.astype(str) != '?']
data = data[data.income.astype(str) != '?']

indexMarital = data[data['marital-status'].astype(str) == '?'].index
data.drop(indexMarital, inplace=True)
indexNative = data[data['native-country'].astype(str) == '?'].index
data.drop(indexNative, inplace=True)

data.shape   #(45222, 8) after cleaning 
data = data.reset_index(drop=True)
data


# In[3]:


# Auxiliary methods for Cost Measurement
def _recurse_tree(parent, depth, source, arr):
    last_line = source.readline().rstrip()
    while last_line:
        tabs = last_line.count('\t')
        if tabs < depth:
            break
        node = last_line.strip()
        if tabs >= depth:
            if parent is not None:
                #print("%s: %s" %(parent, node))
                t = parent + ":" + node
                arr.append(t)
            last_line = _recurse_tree(node, tabs+1, source, arr)
    return last_line

def calc_depth(actual, anon, DGHs):
    count = 0
    
    while actual != anon: 
        for i in range(len(DGHs)):
            exp = "[a-zA-Z]+:" + actual +"$"
            x = re.search(exp, DGHs[i])
            if x:
                count = count + 1
                actual = DGHs[i][:-(len(actual) + 1)]  
    return count

def total_leaves(DGH):
    count = 0
    children = []
    parents = []
    for i in range(len(DGH)):
        index = DGH[i].index(':')
        #print(index)
        child = DGH[i][index + 1:]
        #print(child)
        children.append(child)
        parent = DGH[i][:index]
        #print(parent)
        parents.append(parent)
    res = set(children).difference(parents)
    count = len(res)
    return(count)

def descendent_leaves(node, DGH):
    count = 0
    children = []
    parents = []
    for i in range(len(DGH)):
        index = DGH[i].index(':')
        child = DGH[i][index + 1:]
        children.append(child)
        parent = DGH[i][:index]
        parents.append(parent)
        
    leaves = set(children).difference(parents)
        
    for i in range(len(DGH)):
        if(DGH[i][:len(node)]==node):
            if node in leaves:
                count = count + 1
            else:
                parent = (DGH[i][len(node)+1:])
                
                for i in range(len(DGH)):
                    if(DGH[i][:len(parent)]==parent):
                        if DGH[i][len(parent)+1:] in leaves:
                            count = count + 1              
    return count


# In[4]:


#tests
#m = []
#_recurse_tree(None, 0, open('DGHs/' + dghs[1]), m)

#print("Given 'Divorced' as actual and 'Any' as anonymized, depth cost is: ", calc_depth('Divorced', 'Any', m))
#print("Number of descendent leaves of the node 'Married' is: ",descendent_leaves('Married', m))
print('######################################################################################################')

for i in range(1, len(dghs)):
    arr = []
    _recurse_tree(None, 0, open('DGHs/' + dghs[i]), arr)
    
    print("\nparent-child tuples of ", dghs[i], ": \n")
    print(arr,"\n")
    print("Total leaves in", dghs[i], " = ", total_leaves(arr),"\n")
    
    print('######################################################################################################')


# In[5]:


# 3) Cost Measurement
def cost_MD(actual_dataset, anonymized_dataset, DGHs):
    cost = 0
    for i in range(len(actual_dataset)):
        if actual_dataset[i] != anonymized_dataset[i]:
            diff = calc_depth(actual_dataset[i], anonymized_dataset[i], DGHs)
            cost += diff
    return cost

def cost_LM(actual_dataset, anonymized_dataset, DGHs):
    cost = 0
    size = len(np.unique(actual_dataset))
    weight = 1 / size
    t_leaves = total_leaves(DGHs) - 1
    for i in range(len(actual_dataset)):
        if actual_dataset[i] != anonymized_dataset[i]:
            node = actual_dataset[i]            
            val = descendent_leaves(node, DGHs) - 1
            val = val/t_leaves
            cost = val * weight
    return abs(cost)


# In[6]:


# Auxiliary methods for Top-Down Anonymization

def removeDuplicates(lst):      
    return [[a, b] for i, [a, b] in enumerate(lst)  
    if not any(c == b for _, c in lst[:i])] 

def get_dict(DGH):
    dct = list()
    for i in range(len(DGH)):
        #print(DGH[i])
        children = []
        saved_parents = []
        index = DGH[i].index(':')
        child = DGH[i][index + 1:]        
        parent = DGH[i][:index]
        #print(parent, child)
        children.append(child)
        for j in range(len(DGH)):
            index = DGH[j].index(':')
            if DGH[j][:index] == parent:
                children.append(DGH[j][index + 1:])
        children = list(dict.fromkeys(children))
        #print(parent, "'s children: ",  children)
        #print(sorted(children))
        t = (parent, sorted(children))
        dct.append(t)
        
        """if not parent in saved_parents:
            saved_parents.append(parent)
            dct.append(t)"""
        
    return(sorted(removeDuplicates(dct)))

def find_index_of_key(dct, st):
    ind = 0
    for i in range(len(dct)):
        if dct[i][0] != st:
            ind = ind + 1
        else:
            return ind
    return ind

def downgrade_column(dct, col, curr_anon):
    check_children = dct[find_index_of_key(dct, curr_anon)][1]
    keys = []
    for i in range(len(col)):
        #print(col[i])   #11th
        
        for j in range(len(dct)):
            children = dct[j][1]
            
            if col[i] in children:
                key = dct[j][0]
                #print(key) #first parent
                while not key in check_children:
                    for k in range(len(dct)):
                        if key in dct[k][1]:
                            key = dct[k][0]           
                else:
                    keys.append(key)   
    return keys


# In[7]:


# Test
#downgrade_column(d, data['education'], 'Any')


# In[8]:


# 4) Top-Down Anonymization
def anonymize(actual_dataset, dgh, k):
    full_anon = pd.DataFrame(index=actual_dataset.index, columns=actual_dataset.columns)
    full_anon = full_anon.fillna('Any')
    
    col = actual_dataset[dgh] #to be de-anonymized
    anoncol = full_anon[dgh]
    anoncol_undo = anoncol
    
    arr = []
    _recurse_tree(None, 0, open('DGHs/' + dgh + '.txt'), arr)
    dct = get_dict(arr)
     
    full_anon[dgh] = downgrade_column(dct, col, 'Any')
    anoncol = full_anon[dgh]
    
    unique = np.unique(anoncol)
    C =collections.Counter(anoncol)
        #min_value = None
    minimum = min(C, key=C.get)
    if C[minimum] < k:
        full_anon[dgh] = anoncol_undo
            
    print("MD Cost given k = ", k, "for anonymizing ", dgh, "once:", cost_MD(col, anoncol, arr))
    print("LM Cost given k = ", k, "for anonymizing ", dgh, "once:", cost_LM(col, anoncol, arr))
    
    return full_anon


# In[9]:


anonymize(data, 'education', 2)


# In[ ]:


k_set = [2, 10, 25, 50, 75, 100, 200]

for i in range(1, len(dghs)):
    dgh = dghs[i][:-4]
    for k in k_set:
        anonymize(data, dgh, k)
        
# I attempted to calculate loss for each k in k_set but since the computational complexity of my code is 
# extremely high, I could not get an output even though I have waited for more than 30 minutes.
# My aim was to calculate loss at each recursion and advance accordingly, but I could not test my code
# so I had to change my anonymization algorithm such that it only anonymize once, updates the 'Any' cells
# in order to have a code that compiles. If it did, I was planning to recursively check the children of 'Any'
# until the k limit is reached.


# In[ ]:




