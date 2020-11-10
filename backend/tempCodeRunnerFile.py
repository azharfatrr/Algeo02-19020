print(list_term)

for i in range(len(sim_doc)):
    if (sim_doc[i][0]>0):
        print("Cosine simiarity : ",sim_doc[i][0])
        print(sim_doc[i][1])    # Nama_File
        print(sim_doc[i][2])    # Dokument
        print()