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

1. Membuat *virtual environment* dengan perintah berikut
```
python3 -m venv [nama project]
```
Contoh: python3 -m venv **tubeshore**

2. Masuk ke direktori *virtual environment* tersebut lalu *clone* project ini dengan menggunakan git bash atau lainnya
``` 
git clone https://github.com/azharfatrr/Algeo02-19020.git
```
3. Masuk ke *virtual environment* tersebut via terminal
```
[nama project]\Scripts\activate
```
Contoh: **tubeshore**\Scripts\activate

3. *Install* semua *library* yang dibutuhkan dengan menjalankan perintah-perintah di bawah ini
```
pip install Flask
pip install pandas
pip install Sastrawi
pip install nltk
```
4. Setelah semua *library* ter-*install*, jalankan perintah-perintah di bawah ini
```
python3
import nltk
nltk.download('stopwords')
nltk.download('punkt')
exit()
```
5. Setelah semua langkah di atas berhasil, arahkan terminal ke direktori proyek ini dengan perintah di bawah ini
```
cd "Algeo02-19020/src"
```
6. Jalankan perintah-perintah ini di terminal
```
$env:FLASK_APP = "server.py"
flask run
```
7. Jika berhasil, terminal akan menampilkan URL dari proyek ini, salin URL tersebut dan buka di browser kesayangan, selamat mencoba!

## Tampilan Depan

![Tampilan Depan](https://image.prntscr.com/image/uS3RFPbUSrmoP2kRWNb3JQ.png)
