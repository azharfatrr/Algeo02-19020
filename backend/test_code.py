import os

dir = "./test/"
    
list_File = os.listdir(dir)
allFile = []    # Alamat dan nama file document

for file_name in list_File:
    allFile.append(dir+file_name)   
    
documents = []    # List ini digunakan untuk menyimpan documents dari database
i = 1
# ALGORITMA
for path in allFile:
    # Membaca file documents
    file = open(path,'r')       
    doc = file.read()
    file.close()
    # Next instruction
    new_name = str('%03d' %i)
    
    new_file = dir + "doc" + new_name + ".txt"
    
    # file = open(new_file,'w')
    # file.write(doc)
    # file.close()
    
    i += 1


     