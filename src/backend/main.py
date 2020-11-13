
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
    dir = "../test/"        # Untuk Server
    #dir = "../../test/"    # Untuk Testing
    
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
            filename = path.replace("../test/","")
            temp = [filename,doc]
            documents.append(temp)
            file.close()
            # Next instruction
            i += 1
        else:
            break
    
    return documents

def getSpecDoc(docName,mode):
    ''' fungsi menerima nama dokumen tanpa ekstensi .txt dan mode penghapusannya, \n
    jika tidak ingin dihapus modenya -1, selain itu akan dihapus sesuai dengan paragraf cleaner  '''
    
    path = "../test/" + docName + ".txt"        # Untuk Server
    #path = "../../test/" + docName + ".txt"    # Untuk Testing
    file = open(path, encoding="latin1")
    doc = file.read()
    if (mode != -1):
        doc = text_cleaner(doc,mode)
    return doc
    
def doc_cleaner(documents,mode=0):
    """
    Membersihkan documents dan disimpan pada list clean_doc \n
    Terdapat 2 mode, 0 : Fast Cleansing, 1 : Accurate Cleansing
    Return documents yang sudah dibersihkan
    """
    
    # KAMUS LOKAL
    # pass_doc : setiap documents pada list documents
    clean_doc = [] # documents yang sedang dibersihkan
    
    for doc in documents:
        # Membersihkan tiap documents
        pass_doc = text_cleaner(doc[1],mode)
        # Menambah documents bersih
        clean_doc.append(pass_doc)
    
    return clean_doc
      
def text_cleaner(text,mode=0,clear=True):
    """
    Membersihkan text dari karakter yang tidak diingikan
    """
    
    # KAMUS LOKAL
    clear_text = []
    
    # ALGORITMA
    # Membersihkan unicode ASCII yang tidak terpakai
    clear_text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # Membersihkan mention
    clear_text = re.sub(r'@\w+', '', clear_text)
    # Mode tidak terlalu membersihkan, tidak digunakan jika hanya ingin merapikan
    if clear:
        # Membuat semua huruf lower case
        clear_text = clear_text.lower()
        # Membersihkan punctuation
        clear_text = re.sub(r'[%s]' %re.escape(string.punctuation), ' ', clear_text)
        # Menghilangkan angka 
        clear_text = re.sub(r'[0-9]', '', clear_text)
        # Membersihkan single alphabet
        clear_text = re.sub(r'\b[a-zA-Z]\b', '', clear_text)
    # Menghilangkan space berlebihan
    clear_text = re.sub(r'\s+', ' ', clear_text)
    
    # Mode stemming
    if (mode!=0):
        # Ini bagian yang tidak efisien dan menyebabkan program lambat
        clear_text = stemmer.stem(clear_text)  
        
    return clear_text

def tf_docs(clean_documents,query,mode):
    """
    Mengubah document bersih menjadi dataframe menggunakan pandas dan metode Term Frequency \n
    Return dataframe documents
    """
    # Inisialisasi dataframe
    df = pd.DataFrame([], columns=[0])  
    
    # Kamus stopwords
    stop_words = set(stopwords.words('indonesian'))
    
    i = 0   # Dokumen pertama
    for doc in clean_documents:         # Iterasi tiap document
        df.loc[:,i] = 0                 # Inisialisasi nilai kolom dengan nol
        split_word = doc.split(' ')     # Split menjadi setiap kata
        
        # Menghilangkan Stopwords
        split_word = [w for w in split_word if not w in stop_words]   
        
        # Vektorisasi setiap kata dalam dokumen   
        for word in split_word: 
            # Ini bagian yang tidak efisien dan menyebabkan program lambat
            if not(word in df.index):   # Apakah baris sudah ada?
                df.loc[word,:] = 0      # Jika belum, maka tambahkan baris baru dan inisialisasi semua dengan nol
                df.loc[word,i] = 1      # Lalu baris itu tambah 1
            else:
                df.loc[word,i] += 1     # Kalau udah ada tinggal increment
            
        i += 1      # Indeks dokumen
    
    """
    Menambah query menjadi vector dataframe
    """
    query_clean = text_cleaner(query,mode)
    split_word = query_clean.split(' ')
    
    # Menghilangkan Stopwords
    split_word = [w for w in split_word if not w in stop_words]
    
    df.loc[:,'query'] = 0   # Inisialisasi nilai kolom dengan nol
    
    # Vektorisasi setiap kata dalam query
    for word in split_word:
        if not(word in df.index):       # Apakah baris sudah ada?
            df.loc[word,:] = 0          # Jika belum, maka tambahkan baris baru dan inisialisasi semua dengan nol
            df.loc[word,'query'] = 1    # Lalu baris itu tambah 1
        else:
            df.loc[word,'query'] += 1   # Kalau udah ada tinggal increment
     
    # Merapikan data frame        
    # df.sort_index(inplace=True)       # Sort Index, tidak terlalu perlu
    if ((df.index == '').any()):
        df = df.drop([''])              # Hapus Index kosong         
    
    return df

def cos_similiarity(df):
    '''
    Fungsi ini digunakan untuk menghitung cosine similiarity dari dataframe \n 
    dokumen dan query yang sudah dibersihkan
    '''
    # cos_sim = []      # Indeks menyatakan urutan dokumen
    norm_doc = []       # Indeks menyatakan urutan dokumen
    norm_query = 0      # Inisialisasi
    dot_doc = []        # Indeks menyatakan urutan dokumen
    
    # Pembentukan vektor disesuaikan dengan kamus kata
    col_df = df.columns     # List nama kolom
    row_df = df.index       # List nama index
    
    # Normalisasi Vektor dari Query
    sum = 0
    for row in row_df:
        sum += (df.loc[row,'query'])**2
    norm_query = sum**(1/2)
    
    # Normalisasi Vektor dan menghitung Dot Product dari Dokumen
    for col in col_df:
        if (col != 'query'):    # Biar cuma dokumen doang
            sum_norm = 0
            sum_dot = 0
            for row in row_df:
                # Normalisasi Vektor
                sum_norm += (df.loc[row,col])**2
                # Dot Product
                sum_dot += df.loc[row,col] * df.loc[row,'query']
                
            norm_doc.append(sum_norm**(1/2))    # Jangan lupa diakarkan
            dot_doc.append(sum_dot)
      
    # Inisialisasi nilai cos_sim
    cos_sim = [0 for i in range(len(col_df)-1)]
    # Hitung nilai cos_sim
    for i in range(len(col_df)-1):  # Kolom query tidak termasuk
        if ((norm_doc[i])!=0):      # Hati-hati ada norma vektor yang nol
            cos_sim[i] = dot_doc[i]/(norm_query*norm_doc[i])    
     
    return cos_sim

def dataToList(df):
    '''
    Mengubah dataframe menjadi list
    '''
    #list_data = []
    
    # Hapus term yang tidak diquery
    idx = (df['query'] != 0)   # Cari term yang tidak nol pada kolom query
    df_new = df.loc[idx,:]     # Bentuk dataframe baru
    
    # Ubah urutan kolom query pada dataframe lama lalu simpan di dataframe baru
    col = df_new.columns.tolist()
    col = col[-1:] + col[:-1]
    df_new = df_new[col].astype(int)    # Ubah tipe data jadi integer
    
    # Mengubah nama kolom
    new_name = ['query']
    for i in range(len(col) - 1):        # Kurangi 1 karena ada query
        new_name.append(i+1)                # Pake urutan nama file
    df_new.columns = new_name
    
    # Jadikan list
    col_name = [['term']+df_new.columns.tolist()]
    list_data = col_name + df_new.reset_index().values.tolist()     #Menambah setiap baris
    
    return list_data

def fsDocs(documents):
    fsd = []
    for docs in range(len(documents)):
        s = documents[docs][1]
        # hapus dulu unicode biar ganteng, kadang di kalimat pertama udah ada unicodenya
        clear = re.sub(r'[^\x00-\x7F]+', ' ', s)  
        # kalimat pertama diakhiri tanda titik "." dan spasi selanjutnya,
        # kalau cuma titik nanti bisa berhenti di KOMPAS.com   
        idx = clear.find('. ')                      
        temp = clear[0:idx]
        # tambahin titik yang ikutan kehapus                         
        temp = temp + '.'                           
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
    PROGRAM UTAMA
    query = query document yang paling sesuai \n
    N = banyaknya document \n
    mode = 0 (standart, fast, default), 1 (dilakukan stemming) \n
    return : list document dan cos_sim, dan list term yang di-query
    '''
    # Inisialisasi
    documents = []          #document[i][0] : nama_file, document[i][1] : text dokumen, 
    clean_docs = []         #document[i][2] : kalimat pertama, document[i][3] : banyak kata
    list_term = []
    
    # Dapatkan dokumen dan bersihkan
    documents = get_doc(N)
    firstSentence = fsDocs(documents)           # simpan kalimat pertama
    clean_docs = doc_cleaner(documents,mode)    # bersihkan dokumen
    wordSum = sumWord(clean_docs)               # hitung banyak kata tiap dokumen
    # Buat dataframe dengan pandas
    df = tf_docs(clean_docs,query,mode)         # note : Urutan dataframe sesuai dengan urutan dokumen
    # Hitung cosine simiarity dari tiap dokumen
    sim = cos_similiarity(df)
    # List term yang diquery
    list_term = dataToList(df)
    
    # Gabungkan cosine similiarity dan document kedalam satu array
    sim_doc = []
    for i in range(len(documents)):
        documents[i][1] = text_cleaner(documents[i][1],0,False)  # Bersihkan sedikit dokuments
        temp = [sim[i],documents[i][0],documents[i][1],firstSentence[i],wordSum[i]]
        sim_doc.append(temp)
    
    # Urutkan berdasarkan cosine similiarity
    sim_doc.sort(reverse=True)
           
    return sim_doc, list_term


# Testing
# query = "amerika"
# sim_doc,list_term = main(query,15,0)
# # Buat nampilin aja
# # print(list_term)
# # documents = get_doc()
# # # temp = getSpecDoc("doc001", -1)
# # # print(temp)
# for i in range(len(sim_doc)):
#    if (sim_doc[i][0]>=0):
#        print("Cosine simiarity : ",sim_doc[i][0])
#        print(sim_doc[i][1])    # Nama_File
#        print(sim_doc[i][2])    # Dokument
#        print(sim_doc[i][3])    # First sentence
#        print(sim_doc[i][4])    # Jumlah kata
#        print()
