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
    Fungsi ini digunakan untuk membaca file dari database dan disimpan ke document \n
    Format penamaan document : doc<i>.txt (i = 1..End) \n
    Return list of string
    """
    # KAMUS LOKAL
    i = 1                                           # Nomor documents
    path = "Documents/" + "doc" + str(i) + ".txt"   # Alamat dan nama file document
    document = []    # List ini digunakan untuk menyimpan document dari database
    
    # ALGORITMA
    while(os.path.exists(path)):    # Cek apakah file ada, asumsi nama file terurut
        # Membaca file document
        file = open(path,'r')       
        doc = file.read()
        # Menambah data document dari file ke list
        document.append(doc)
        # Next instruction
        i += 1
        path = "Documents/" + "doc" + str(i) + ".txt"
        file.close()
        
    return document

def doc_cleaner(document,mode=0):
    """
    Membersihkan document dan disimpan pada list clean_doc \n
    Terdapat 2 mode, 0 : Fast Cleansing, 1 : Accurate Cleansing
    Return list of string
    """
    # KAMUS LOKAL
    # pass_doc : setiap document pada list document
    clean_doc = [] # document yang sedang dibersihkan
    
    for doc in document:
        # Membersihkan tiap document
        pass_doc = paragraph_cleaner(doc)
        if (mode!=0):
            pass_doc = stemmer.stem(pass_doc)
        # Menambah document bersih
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


    
    