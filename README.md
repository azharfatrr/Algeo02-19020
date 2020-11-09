# Algeo02-19020
Tubes 2 Algeo

Link Laporan :
https://docs.google.com/document/d/14HeyY722pe1jDHskdt7BWtCvsoYdLkpFYQoZiFbJgdg/edit#

Cara run (windows, terminal = powershell):
1. Bikin virtual environment
```
python3 -m venv [nama project]
```
2. Masuk ke direktori virtual env tsb lalu clone project ini menggunakan git bash atau lainnya
``` 
git clone https://github.com/azharfatrr/Algeo02-19020.git
```
3. Masuk ke venv via terminal
```
[nama project]\Scripts\activate
```
3. Install semua modul yang ada di requirements.txt
```
pip install [nama modul]
```
4. Setelah semua modul terinstall, arahkan ke folder project
```
cd Algeo02-19020
```
5. Jalanin ini di terminal
```
$env:FLASK_APP = "server.py"
flask run
```
3. Cek url di log terminal, terus buka, done, hf
