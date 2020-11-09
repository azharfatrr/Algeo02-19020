for word in split_word: # Setiap kata cek
    #     if not((df.index == word).any()):   # Apakah baris sudah ada?
    #         df.loc[word,:] = 0              # Jika belum, maka tambahkan baris baru dan inisialisasi semua dengan nol
    #         df.loc[word,i] = 1              # Lalu baris itu tambah 1
    #     else:
    #         df.loc[word,i] += 1             # Kalau udah ada tinggal increment