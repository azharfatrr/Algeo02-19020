import os.path
import re
import string
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords 

# Module Initialization
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# KAMUS FUNGSI DAN PROSEDUR

def get_doc(N=15):
    """
    Fungsi ini digunakan untuk membaca file dari database sebanyak N dan disimpan ke documents \n
    Return document[0] : document, document[1] : namafile
    """
    # KAMUS LOKAL
    dir = "../test/"
    
    list_File = os.listdir(dir)
    allFile = []    # Alamat dan nama file document
    
    for file_name in list_File:
        allFile.append(dir+file_name)   

    documents = []    # List ini digunakan untuk menyimpan documents dari database
    i = 0
    # ALGORITMA
    for path in allFile:
        if (i<N):
            # Membaca file documents
            file = open(path,encoding='latin1')       
            doc = file.read()
            # Menambah data documents dari file ke list
            filename = path.replace("./test/","")
            temp = [filename,doc]
            documents.append(temp)
            file.close()
            # Next instruction
            i += 1
        else:
            break
    
    return documents

def getSpecDoc(docName,mode):
    ''' fungsi menerima nama dokumen tanpa ekstensi .txt dan mode penghapusannya, jika tidak ingin dihapus modenya -1, selain itu akan dihapus sesuai dengan paragraf cleaner  '''
    path = "../test/" + docName + ".txt"
    file = open(path, encoding="latin1")
    doc = file.read()
    if (mode != -1):
        doc = paragraph_cleaner(doc,mode)
    return doc
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
        pass_doc = paragraph_cleaner(doc[1],mode)
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
    
    ''' INI ADA TAMBAHAN '''
    stop_words = set(stopwords.words('indonesian'))


    i = 0   # Dokumen pertama
    for doc in clean_documents: # Iterasi tiap document
        df.loc[:,i] = 0         # Inisialisasi nilai kolom dengan nol
        split_word = doc.split(' ') # Split menjadi setiap kata
        
        ''' INI ADA TAMBAHAN '''
        split_word = [w for w in split_word if not w in stop_words]
                    
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
    ''' INI ADA TAMBAHAN '''
    split_word = [w for w in split_word if not w in stop_words]
    
    df.loc[:,'query'] = 0
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
    
    # Pembentukan vector disesuaikan dengan kamus kata
    col_df = df.columns
    row_df = df.index
    
    # Normal query
    sum = 0
    for row in row_df:
        sum += (df.loc[row,'query'])**2
    norm_query = sum**(1/2)
    
    # Normal doc & Dot product
    for col in col_df:
        if (col != 'query'):
            sum_norm = 0
            sum_dot = 0
            for row in row_df:
                sum_norm += (df.loc[row,col])**2
                sum_dot += df.loc[row,col]*df.loc[row,'query']
                
            norm_doc.append(sum_norm**(1/2))
            dot_doc.append(sum_dot)
      
    cos_sim = [0 for i in range(len(col_df)-1)]
    for i in range(len(col_df)-1):  # Kurangi query
        if ((norm_doc[i])!=0):
            cos_sim[i] = dot_doc[i]/(norm_query*norm_doc[i])    
     
    return cos_sim

def dataToList(df,documents):
    '''
    Mengubah dataframe menjadi list
    '''
    #list_data = []
    
    # Hapus term yang tidak diquery
    idx = (df['query'] != 0)     # Cari kata yang tidak nol di query
    df_new = df.loc[idx,:]
    
    # Ubah urutan query pada kolom df simpan di df_new
    col = df_new.columns.tolist()
    col = col[-1:] + col[:-1]
    df_new = df_new[col].astype(int)
    
    # Ubah nama kolom
    new_name = ['query']
    for i in range(len(documents)):
        # new_name.append(documents[i][0])    # Pake nama file
        new_name.append(i+1)    # Pake semi nama file
    df_new.columns = new_name
    
    # Jadikan list
    col_name = [['term']+df_new.columns.tolist()]
    list_data = col_name + df_new.reset_index().values.tolist()
    
    return list_data

def fsDocs(documents):
    fsd = []
    for docs in range(len(documents)):
        s = documents[docs][1]
        clear = re.sub(r'[^\x00-\x7F]+', ' ', s)    #hapus dulu unicode biar ganteng, kadang di kalimat pertama udah ada unicodenya
        idx = clear.find('. ')                      #kalimat pertama diakhiri tanda titik "." dan spasi selanjutnya, kalau cuma titik nanti bisa berhenti di KOMPAS.com
        temp = clear[0:idx]
        temp = temp + '.'                           #tambahin titik yang ikutan kehapus
        fsd.append(temp)
    return fsd

def sumWord(clean_doc):
    sumW = []
    for docs in range(len(clean_doc)):
        s = clean_doc[docs]
        temp = len(s.split())
        sumW.append(temp)
    return sumW


def main(query="master wiwid panutan kita",N=15,mode=0):
    '''
    query = query document yang paling sesuai \n
    N = banyaknya document \n
    mode = 0 (standart, fast, default), 1 (dilakukan stemming) \n
    return : list document dan cos_sim, dan list tf dari query
    '''
    # Inisialisasi
    documents = []          #document[i][0] : nama_file, document[i][1] : document
    clean_docs = []
    list_term = []
    
    # Dapatkan dokumen dan bersihkan
    documents = get_doc(N)
    firstSentence = fsDocs(documents)           #simpan kalimat pertama
    clean_docs = doc_cleaner(documents,mode)    # Udah disesuaikan
    wordSum = sumWord(clean_docs)               #hitung banyak kata tiap dokumen
    # Buat dataframe dengan pandas dan numpy
    df = tf_docs(clean_docs,query,mode)         # NOTE : Urutan dataframe sesuai dengan urutan dokumen
    # Hitung cosine simiarity dari tiap dokumen
    sim = cos_similiarity(df)
    # List term yang diquery
    list_term = dataToList(df,documents)
    
    # Gabungkan cosine similiarity dan document kedalam satu array
    sim_doc = []
    for i in range(len(documents)):
        documents[i][0] = paragraph_cleaner(documents[i][0],0,False)  # Bersihkan sedikit dokuments
        temp = [sim[i],documents[i][0],documents[i][1]]
        sim_doc.append(temp)
    
    # Urutkan berdasarkan cosine similiarity
    sim_doc.sort(reverse=True)
           
    return sim_doc, list_term, firstSentence, wordSum


# Testing
# query = "pemilu pilpres amerika"
# sim_doc,list_term = main(query,15,0)
# Buat nampilin aja
# print(list_term)
# documents = get_doc()
temp = getSpecDoc("doc001", -1)
print(temp)
# for i in range(len(sim_doc)):
#     if (sim_doc[i][0]>0):
#         print("Cosine simiarity : ",sim_doc[i][0])
#         print(sim_doc[i][1])    # Nama_File
#         print(sim_doc[i][2])    # Dokument
#         print()



    
    