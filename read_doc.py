import os.path
import re
import string
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Inisialisasi
# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Membaca dokumen
documents = []

# Format penamaan file "doc<no>.txt"
i = 1
path = "Documents/" + "doc" + str(i) + ".txt"

while(os.path.exists(path)):
    file = open(path,'r')
    doc = file.read()
    documents.append(doc)
    file.close()
    i += 1
    path = "Documents/" + "doc" + str(i) + ".txt"
    
# Documents cleansing
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
  
# Instantiate a TfidfVectorizer object
vectorizer = TfidfVectorizer()  
# It fits the data and transform it as a vector
X = vectorizer.fit_transform(documents_clean)
# Convert the X as transposed matrix
X = X.T.toarray()
# Create a DataFrame and set the vocabulary as the index
df = pd.DataFrame(X, index=vectorizer.get_feature_names())

# print(df)

q = ["krisis"]
q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
sim = []

# for i in range(20):
#     sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)

n_doc = len(df.columns) #banyaknya documents
norm2 = np.linalg.norm(q_vec)

for i in range(n_doc):
    # print(df.loc[:,i].values) #entire row in doc 4, row : text, column : doc
    dot = np.dot(df.loc[:,i].values,q_vec)
    norm1 = np.linalg.norm(df.loc[:,i])
    if (norm1*norm2!=0):
        cos_sim = dot/(norm1*norm2) 
        if (cos_sim!=0):
            to_add = [cos_sim,i]
            sim.append(to_add)

sim.sort(reverse=True)  

for doc in sim:
    if doc[0] > 0.1:
        print("Nilai Similaritas:", doc[0])
        print(documents[doc[1]])
        print()

