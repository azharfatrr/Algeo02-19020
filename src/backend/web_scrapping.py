import requests
import os.path
from bs4 import BeautifulSoup

# Note : Mengambil berita dari kompas.com
link_doc = "https://news.kompas.com/"

# Buat request dapatkan halaman pencarian
r = requests.get(link_doc)

# Parse hasil menjadi html
parser = BeautifulSoup(r.content, 'html.parser')

# Retrieve all popular news links (Fig. 1)
all_link = []
for ref in parser.find('div', {'class':'most__wrap'}).find_all('a'): #Berkaitan dengan struktur data web
    link = ref['href']+'?page=all'
    if link not in all_link:
        all_link.append(link)                           #Biar pagenya ditampilkan semua
    
# # Dari setiap link, kita ambil dokumen di dalamnya
document = []
for link in all_link:
    # Dapatkan info dalam link
    r = requests.get(link)

    #Parse HTML
    parser = BeautifulSoup(r.content, 'html.parser')

    #Dapatkan tiap content paragraph
    content = []
    i = 0
    for p in parser.find('div', {'class':'read__content'}).find_all('p'):
        content.append(p.text)

    # Tambahkan ke dalam document
    document.append(' '.join(content))

# Simpan document
num = 1
for doc in document:
    # Inisialisasi
    path = "../../test/"
    number = str('%03d' %num)
    filename = "doc" + number +".txt"
    path += filename
    
    while (os.path.exists(path)): #Cek nama document sudah ada atau belum
        num += 1
        path = "../../test/"
        number = str('%03d' %num)
        filename = "doc" + number +".txt"
        path += filename
    
    # Tulis document ke dalam file
    file = open(path,'w')
    file.write(doc)
    file.close()
    num += 1
    
print("Berhasil mengambil data dari " + link_doc)