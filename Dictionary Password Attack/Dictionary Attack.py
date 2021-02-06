import pandas as pd

data = pd.read_csv('Desktop/rockyou.txt', sep=",", header=None) 

import hashlib

hashed = list()
for d in data[0]:
    h = hashlib.sha512(d.encode('utf-8')).hexdigest()
    hashed.append(h)
    
import csv

with open('attack.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(data[0], hashed))
    
dict = pd.read_csv('attack.csv', sep=",", header=None)   
print(dict)

stolen = pd.read_csv('Desktop/megacorp.txt', sep=",", header=None) 
stolen_hashed = stolen[1]

# Alice's password
alice = ""
for i in range(len(hashed)):
    if stolen_hashed[1] == hashed[i]:
        alice = dict[0][i]
        
# Bob's password
bob = ""
for i in range(len(hashed)):
    if stolen_hashed[2] == hashed[i]:
        bob = dict[0][i]
        
# Charlie's password
charlie = ""
for i in range(len(hashed)):
    if stolen_hashed[3] == hashed[i]:
        charlie = dict[0][i]
        
print(alice)
print(bob)
print(charlie)

'''
# This part does not work on salted passwords
stolen_salty = pd.read_csv('Desktop/salty-megacorp.txt', sep=",", header=None) 
stolen_hashed_salty = stolen_salty[2]

# Dave's password
dave = ""
for i in range(len(hashed)):
    if stolen_hashed_salty[1] == hashed[i]:
        dave = dict[0][i]
        
# Elaine's password
elaine = ""
for i in range(len(hashed)):
    if stolen_hashed_salty[2] == hashed[i]:
        elaine = dict[0][i]
        
# Faith's password
faith = ""
for i in range(len(hashed)):
    if stolen_hashed_salty[3] == hashed[i]:
        faith = dict[0][i]
        
print(dave)
print(elaine)
print(faith)
'''

'''
# Dave's salty password
dave_salty = stolen_salty[2][1] + stolen_salty[1][1]

# Elaine's salty password
elaine_salty = stolen_salty[2][2] + stolen_salty[1][2]

# Faith's salty password
faith_salty = stolen_salty[2][3] + stolen_salty[1][3]
'''
stolen_salty = pd.read_csv('Desktop/salty-megacorp.txt', sep=",", header=None) 

daves_salt = stolen_salty[1][1]
elaines_salt = stolen_salty[1][2]
faiths_salt = stolen_salty[1][3]

# Dave's password
salt_hashed_dave = list()
for d in data[0]:
    d = d + daves_salt
    h = hashlib.sha512(d.encode('utf-8')).hexdigest() 
    salt_hashed_dave.append(h)
with open('attack1.csv', 'w') as f1:
    writer = csv.writer(f1)
    writer.writerows(zip(data[0], salt_hashed_dave))

dict_salt_dave = pd.read_csv('attack1.csv', sep=",", header=None)

dave_salty = stolen_salty[2][1] #+ daves_salt

dave = ""
for i in range(len(dict_salt_dave[0])):
    if dave_salty == dict_salt_dave[1][i]:
        dave = dict_salt_dave[0][i]
        
print(dave)

# Elaine's password
salt_hashed_elaine = list()
for d in data[0]:
    d = d + elaines_salt
    h = hashlib.sha512(d.encode('utf-8')).hexdigest()
    salt_hashed_elaine.append(h)
with open('attack1.csv', 'w') as f2:
    writer = csv.writer(f2)
    writer.writerows(zip(data[0], salt_hashed_elaine))
    
dict_salt_elaine = pd.read_csv('attack1.csv', sep=",", header=None)

elaine_salty = stolen_salty[2][2] #+ elaines_salt

elaine = ""
for i in range(len(dict_salt_elaine[0])):
    if elaine_salty == dict_salt_elaine[1][i]:
        elaine = dict_salt_elaine[0][i]
        
print(elaine)

# Faith's password
salt_hashed_faith = list()
for d in data[0]:
    d = d + faiths_salt
    h = hashlib.sha512(d.encode('utf-8')).hexdigest()
    salt_hashed_faith.append(h)
with open('attack3.csv', 'w') as f3:
    writer = csv.writer(f3)
    writer.writerows(zip(data[0], salt_hashed_faith))
    
dict_salt_faith = pd.read_csv('attack3.csv', sep=",", header=None)

faith_salty = stolen_salty[2][3] #+ faiths_salt

faith = ""
for i in range(len(dict_salt_faith[0])):
    if faith_salty == dict_salt_faith[1][i]:
        faith = dict_salt_faith[0][i]
        
print(faith)