# Algeo02-19020
Tugas Besar 2 Algeo (Mesin Pencari Sederhana Menggunakan Algoritma *Cosine Similarity*)

Link Laporan :
https://docs.google.com/document/d/14HeyY722pe1jDHskdt7BWtCvsoYdLkpFYQoZiFbJgdg/edit#

## Anggota:
1. Muhammad Azhar Faturahman (K-4) 13519020
2. Widya Anugrah Putra (K-1) 13519105
3. Rezda Abdullah Fachrezzi (K-2) 13519194

## Struktur Direktori:
1. **doc** -> lokasi penyimpanan laporan tugas besar.
2. **src** -> lokasi penyimpanan program.
3. **test** -> lokasi penyimpanan filefile yang merupakan dokumen uji (\*.txt).

## Spesifikasi Program:
1. *Backend* menggunakan *framework* **Flask** dengan bahasa **Python3**.
2. *Fronend* menggunakan *template* dari [Semantic UI](https://semantic-ui.com).

## Cara Menjalankan Program:

### a. Sistem Operasi Windows dengan Terminal Powershell

Pastikan bahwa [Python3](https://www.python.org/download/releases/3.0/) sudah ter-*install*.

1. Buat suatu folder baru, lalu di dalam folder tersebut, tekan **Shift + Klik Kanan**, terdapat pilihan **Open Powershell Window here**, pilih.

![Terminal](https://image.prntscr.com/image/IQzjuc0rQlm4ouwlWdv5Ew.png)

![Terminal](https://image.prntscr.com/image/f7qbe7TPQkCyxR2mplRbDQ.png)

2. Setelah terminal terbuka, buat *virtual environment* dengan perintah berikut
```
python3 -m venv [nama project]
```
Contoh: python3 -m venv **algeo**

Jika berhasil, di dalam folder tersebut akan ada folder bernama **algeo**.

![Terminal](https://image.prntscr.com/image/T0qEB9ZmTjahFSiJeDSO0g.png)

3. Masuk ke direktori *virtual environment* tersebut lalu *clone* project ini dengan menggunakan git bash atau lainnya
``` 
git clone https://github.com/azharfatrr/Algeo02-19020.git
```

![Terminal](https://image.prntscr.com/image/N8oGUWazTwiiVgOrF-eBZA.png)

4. Arahkan terminal ke folder tersebut dan masuk ke *virtual environment* tersebut via terminal dengan perintah di bawah ini.
```
cd algeo
Scripts/activate
```

![Terminal](https://image.prntscr.com/image/kxNU43EyQFKY0NBXS7FRNw.png)

5. *Install* semua *library* yang dibutuhkan dengan menjalankan perintah-perintah di bawah ini
```
pip install Flask
pip install pandas
pip install Sastrawi
pip install nltk
```

![Terminal](https://image.prntscr.com/image/3mQFKx5gTuubHBsPrSEGyg.png)

6. Setelah semua *library* ter-*install*, jalankan perintah di bawah ini
```
python3
```

![Terminal](https://image.prntscr.com/image/pFOS7A6BR0yYjpeC-OgV7w.png)

Setelah itu, jalankan perintah-perintah di bawah ini **(tanpa 3 karakter dan spasi di depannya)**.
```
>>> import nltk
>>> nltk.download('stopwords')
>>> nltk.download('punkt')
>>> exit()
```

![Terminal](https://image.prntscr.com/image/VERmkR_YS_e4gnWe8e-2fQ.png)

7. Setelah semua langkah di atas berhasil, arahkan terminal ke direktori proyek ini dengan perintah di bawah ini
```
cd "Algeo02-19020/src"
```

![Terminal](https://image.prntscr.com/image/fhMgAwLxQAGMbjg5FGqgtQ.png)

8. Jalankan perintah-perintah ini di terminal
```
$env:FLASK_APP = "server.py"
flask run
```

Jika berhasil, terminal akan menampilkan URL dari proyek ini, salin URL tersebut dan buka di browser kesayangan, selamat mencoba!

## Tampilan Terminal Ketika Berhasil

![Terminal](https://image.prntscr.com/image/VPo9QamSRx2eCrN10dg-rQ.png)

## Tampilan Depan

![Tampilan Depan](https://image.prntscr.com/image/uS3RFPbUSrmoP2kRWNb3JQ.png)
