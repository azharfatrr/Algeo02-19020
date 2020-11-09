import os.path
import re
import string
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Module Initialization
factory = StemmerFactory()
stemmer = factory.create_stemmer()
vectorizer = TfidfVectorizer() 

# KAMUS FUNGSI DAN PROSEDUR

def get_doc():
    """
    Fungsi ini digunakan untuk membaca file dari database dan disimpan ke documents \n
    Format penamaan document : doc<i>.txt (i = 1..End) \n
    Return list of string
    """
    # KAMUS LOKAL
    i = 1                                           # Nomor documents
    path = "./test/" + "doc" + str(i) + ".txt"   # Alamat dan nama file document
    documents = []    # List ini digunakan untuk menyimpan documents dari database
    
    # ALGORITMA
    while(os.path.exists(path)):    # Cek apakah file ada, asumsi nama file terurut
        # Membaca file documents
        file = open(path,'r')       
        doc = file.read()
        # Menambah data documents dari file ke list
        documents.append(doc)
        # Next instruction
        i += 1
        path = "./test/" + "doc" + str(i) + ".txt"
        file.close()
        
    return documents

def doc_cleaner(documents,mode=0):
    """
    Membersihkan documents dan disimpan pada list clean_doc \n
    Terdapat 2 mode, 0 : Fast Cleansing, 1 : Accurate Cleansing
    Return list of string
    """
    # KAMUS LOKAL
    # pass_doc : setiap documents pada list documents
    clean_doc = [] # documents yang sedang dibersihkan
    
    for doc in documents:
        # Membersihkan tiap documents
        pass_doc = paragraph_cleaner(doc)
        if (mode!=0):
            pass_doc = stemmer.stem(pass_doc)
        # Menambah documents bersih
        clean_doc.append(pass_doc)
    
    return clean_doc
      
def paragraph_cleaner(paragraph):
    """
    Membersihkan paragraph
    """
    # KAMUS LOKAL
    clear_paragraph = []
    
    # ALGORITMA
    # Membersihkan unicode ASCII yang tidak terpakai
    clear_paragraph = re.sub(r'[^\x00-\x7F]+', ' ', paragraph)
    # Membersihkan mention
    clear_paragraph = re.sub(r'@\w+', '', clear_paragraph)
    # Membuat semua huruf lower case
    clear_paragraph = clear_paragraph.lower()
    # Membersihkan punctuation
    clear_paragraph = re.sub(r'[%s]' %re.escape(string.punctuation), ' ', clear_paragraph)
    # Menghilangkan angka
    clear_paragraph = re.sub(r'[0-9]', '', clear_paragraph)
    # Menghilangkan double space
    clear_paragraph = re.sub(r'\s{2,}', ' ', clear_paragraph)
    
    return clear_paragraph

def tfidf_doc(clean_documents):
    """
    Mengubah document bersih menjadi dataframe menggunakan pandas dan metode TFIDF \n
    Return dataframe documents
    """
    # # Memberikan nilai pada setiap kata dalam dokumen dengan metode TFIDF
    # temp = vectorizer.fit_transform(clean_documents)
    # # Mengubah documents menjadi bentuk matriks
    # temp = temp.T.toarray()
    # # Membuat dataframe dengan pandas, baris : komponen kata, kolom : dokumen ke-(x-1), elemen adalah nilai TFID kata tersebut dalam dokumen
    # df = pd.DataFrame(temp, index=vectorizer.get_feature_names())
    # df = pd.DataFrame([], index='test')
    # for doc in clean_documents:
        
    
    # # return df

def tfidf_query(query,df):
    """
    Mengubah query menjadi vector dataframe, df adalah dataframe acuan
    Return dataframe query
    """
    clean_query = paragraph_cleaner(query)
    clean_query = [clean_query] #Ubah jadi array
    vector_query = vectorizer.transform(clean_query).toarray(df.shape[0])
    
    return vector_query



    
    