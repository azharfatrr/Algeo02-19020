import requests
import os.path
from bs4 import BeautifulSoup

# Note : hanya bisa menerima dari kompas, belum disesuaikan lagi
link_doc = "https://bola.kompas.com/"

# Make a request to the website
r = requests.get(link_doc)

# Create an object to parse the HTML format
soup = BeautifulSoup(r.content, 'html.parser')

# Retrieve all popular news links (Fig. 1)
link = []
for i in soup.find('div', {'class':'most__wrap'}).find_all('a'): #Berkaitan dengan struktur data web
    link.append(i['href']+'?page=all')                           #Biar pagenya ditampilkan semua
    
# For each link, we retrieve paragraphs from it, combine each paragraph as one string, 
# and save it to documents (Fig. 2)

document = []
for i in link:
    #Dapatkan info dalam link
    r = requests.get(i)
    
    #Parse HTML
    soup = BeautifulSoup(r.content, 'html.parser')
    
    #Dapatkan tiap paragraph
    sen = []
    for i in soup.find('div', {'class':'read__content'}).find_all('p'):
        sen.append(i.text)
    document.append(' '.join(sen))


# Simpan dokumen
j = 1
for doc in document:
    path = "./test/"
    number = str('%03d' %j)
    filename = "doc" + number +".txt"
    path += filename
    
    while (os.path.exists(path)): #Cek nama document sudah ada atau belum
        j += 1
        path = "./test/"
        number = str('%03d' %j)
        filename = "doc" + number +".txt"
        path += filename
    
    file = open(path,'w')
    file.write(doc)
    file.close()
    j += 1
    
print("Berhasil mengambil data dari " + link_doc)