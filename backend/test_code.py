import os.path
import re
import string
import numpy as np
import pandas as pd

# path = "./test/" + "doc" + str(1) + ".txt"
# print(os.path.exists(path))

documents = []

i = 1
path = "./test/" + "doc" + str(i) + ".txt"

while(os.path.exists(path) and i <= 15):
    file = open(path,'r')
    doc = file.read()
    documents.append(doc)
    file.close()
    i += 1
    path = "./test/" + "doc" + str(i) + ".txt"

# KAMUS LOKAL
documents_clean = []
for d in documents:
    # Remove Unicode
    document_test = re.sub(r'[^\x00-\x7F]+', ' ', d)
    # Remove Mentions
    document_test = re.sub(r'@\w+', '', document_test)
    # Lowercase the document
    document_test = document_test.lower()
    # Remove punctuations
    document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
    # Lowercase the numbers
    document_test = re.sub(r'[0-9]', '', document_test)
    # Remove the doubled space
    document_test = re.sub(r'\s{2,}', ' ', document_test)
    # Stemming kata dengan sastrawi
    # document_test = stemmer.stem(document_test)
    # print("berhasil")

    # Menambahkan dokumen bersih
    documents_clean.append(document_test)

# print(clean_documents)

'''
PENTING

df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), index=['a', 'b', 'c'])
print(df)

print(df.loc['a',1]) # Select data

print('d' in df.index) # Cek apakah indeks ada

df.loc['d',:] = int(2) # Menambah indeks

print(df)
'''

df = pd.DataFrame(np.array([]))

# df.loc['d',:] = 2 # Menambah indeks
# # print(df)
# df.loc[:,1] = 2 # Menambah kolom ke 1
# df.loc[:,2] = 3 # Menambah kolom ke 1
# print(df.loc[:,0])

temp = documents_clean[0].split(' ')
# print(temp)

for word in temp:
    if not((df.index == word).any()):
        df.loc[word,:] = 0
        df.loc[word,0] = 1
    else:
        df.loc[word,0] += 1
    
print(df)