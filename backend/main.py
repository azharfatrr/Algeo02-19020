import os.path
import re
import string
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Module Initialization
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# KAMUS FUNGSI DAN PROSEDUR

def get_doc(N=15):
    """
    Fungsi ini digunakan untuk membaca file dari database sebanyak N dan disimpan ke documents \n
    Format penamaan document : doc<i>.txt (i = 1..End) \n
    Return list of string
    """
    # KAMUS LOKAL
    dir = "./test/"
    
    list_File = os.listdir(dir)
    allFile = []    # Alamat dan nama file document
    
    for file_name in list_File:
        allFile.append(dir+file_name)   
        
    documents = []    # List ini digunakan untuk menyimpan documents dari database
    i = 0
    # ALGORITMA
    for path in allFile:
        # Membaca file documents
        file = open(path,'r')       
        doc = file.read()
        # Menambah data documents dari file ke list
        documents.append(doc)
        file.close()
        # Next instruction
        if (i<N):
            i += 1
        else:
            break
        
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
        pass_doc = paragraph_cleaner(doc,mode)
        # Menambah documents bersih
        clean_doc.append(pass_doc)
    
    return clean_doc
      
def paragraph_cleaner(paragraph,mode=0,clear=True):
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
    # Membersihkan punctuation
    if clear:
        clear_paragraph = clear_paragraph.lower()
        # Menghilangkan angka
        clear_paragraph = re.sub(r'[%s]' %re.escape(string.punctuation), ' ', clear_paragraph)
        # Membuat semua huruf lower case
        clear_paragraph = re.sub(r'[0-9]', '', clear_paragraph)
        # Membersihkan single alphabet
        clear_paragraph = re.sub(r'\b[a-zA-Z]\b', '', clear_paragraph)
    # Menghilangkan double space
    clear_paragraph = re.sub(r'\s{2,}', ' ', clear_paragraph)
    if (mode!=0):
        clear_paragraph = stemmer.stem(clear_paragraph)
    return clear_paragraph

def tf_docs(clean_documents,query,mode):
    """
    Mengubah document bersih menjadi dataframe menggunakan pandas dan metode TFIDF \n
    Return dataframe documents
    """
    df = pd.DataFrame([], columns=[0])  # Inisialisasi dataframe

    i = 0   # Dokumen pertama
    for doc in clean_documents: # Iterasi tiap document
        df.loc[:,i] = 0         # Inisialisasi nilai kolom dengan nol
        split_word = doc.split(' ') # Split menjadi setiap kata
                    
        for word in split_word: # Setiap kata cek
            if not((df.index == word).any()):   # Apakah baris sudah ada?
                df.loc[word,:] = 0              # Jika belum, maka tambahkan baris baru dan inisialisasi semua dengan nol
                df.loc[word,i] = 1              # Lalu baris itu tambah 1
            else:
                df.loc[word,i] += 1             # Kalau udah ada tinggal increment
        i += 1 # Indeks dokumen
        
    df.sort_index(inplace=True)         # Sort Index
    if ((df.index == '').any()):
        df = df.drop([''])              # Drop Index kosong
    
    """
    Menambah query menjadi vector dataframe
    """
    
    query_clean = paragraph_cleaner(query,mode)
    split_word = query_clean.split(' ')
    
    #df.loc[:,'query'] = 0
    df = df.assign(query=0)
    
    for word in split_word: # Setiap kata cek
        if not((df.index == word).any()):   # Apakah baris sudah ada?
            df.loc[word,:] = 0              # Jika belum, maka tambahkan baris baru dan inisialisasi semua dengan nol
            df.loc[word,'query'] = 1              # Lalu baris itu tambah 1
        else:
            df.loc[word,'query'] += 1             # Kalau udah ada tinggal increment
    return df

def cos_similiarity(df):
    # cos_sim = []    # Indeks menyatakan urutan dokumen
    norm_doc = []   # Indeks menyatakan urutan dokumen
    norm_query = 0  # Inisialisasi
    dot_doc = []    # Indeks menyatakan urutan dokumen
    
    # Pembentukan vector disesuaikan dengan term pada query
    idx = (df['query'] != 0)     # Cari kata yang tidak nol di query
    df_new = df.loc[idx,:]
    
    col_df = df_new.columns
    row_df = df_new.index
    
    # Normal query
    sum = 0
    for row in row_df:
        sum += (df_new.loc[row,'query'])**2
    norm_query = sum**(1/2)
    
    # Normal doc & Dot product
    for col in col_df:
        if (col != 'query'):
            sum_norm = 0
            sum_dot = 0
            for row in row_df:
                sum_norm += (df_new.loc[row,col])**2
                sum_dot += df_new.loc[row,col]*df_new.loc[row,'query']
                
            norm_doc.append(sum_norm**(1/2))
            dot_doc.append(sum_dot)
      
    cos_sim = [0 for i in range(len(col_df)-1)]
    for i in range(len(col_df)-1):  # Kurangi query
        if ((norm_doc[i])!=0):
            cos_sim[i] = dot_doc[i]/(norm_query*norm_doc[i])    
      
    return cos_sim

def main(query="master wiwid panutan kita",N=15,mode=0):
    '''
    query = query document yang paling sesuai \n
    N = banyaknya document \n
    mode = 0 (standart, fast, default), 1 (dilakukan stemming)
    '''
    # Inisialisasi
    documents = []
    clean_docs = []
    
    # Dapatkan dokumen dan bersihkan
    documents = get_doc(N)
    clean_docs = doc_cleaner(documents,mode)
    
    # Buat dataframe dengan pandas dan numpy
    df = tf_docs(clean_docs,query,mode)
    # Hitung cosine simiarity dari tiap dokumen
    sim = cos_similiarity(df)
    
    # Gabungkan cosine similiarity dan document kedalam satu array
    sim_doc = []
    for i in range(len(documents)):
        documents[i] = paragraph_cleaner(documents[i],0,False)  # Bersihkan sedikit dokuments
        temp = [sim[i],documents[i]]
        sim_doc.append(temp)
    
    # Urutkan berdasarkan cosine similiarity
    sim_doc.sort(reverse=True)
           
    return sim_doc


query = "pemilu amerika"
sim_doc = main(query,15,0)

# Buat nampilin aja
for i in range(len(sim_doc)):
    if (sim_doc[i][0]>0):
        print("Cosine simiarity : ",sim_doc[i][0])
        print(sim_doc[i][1])


    
    