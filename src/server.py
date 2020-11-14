from flask import Flask, render_template, request, redirect
from backend import main
from time import time

# init
app = Flask(__name__, static_folder='frontend/static', template_folder='frontend/views')

# router
@app.route('/')
def homepage():
  """ halaman depan """
  return render_template('index.html')

@app.route('/perihal')
def perihal():
  """ halaman untuk perihal """
  return render_template('perihal.html')
    
@app.route('/search', methods=['GET'])
def search():
  """
  halaman untuk mendapatkan hasil pencarian berdasarkan tiga paramater
  querysearch = kata kunci pencarian
  querytype = tipe pencarian (cepat atau akurat [lambat, dilakukan stemming])
  querydoc = jumlah dokumen yang akan dicari
  """
  doc = 160 # jumlah dokumen
  timebefore = time() # waktu (detik) sebelum dimulai pencarian, digunakan untuk menghitung lamanya pencarian

  # validasi request
  if not request.args.get('querydoc') or not request.args.get('querytype') or not request.args.get('querysearch'):
    return redirect("/")
  if not(int(request.args.get('querydoc')) > 0 and int(request.args.get('querydoc')) <= doc):
    return redirect("/")
  if int(request.args.get('querytype')) != 1 and int(request.args.get('querytype')) != 0:
    return redirect("/")

  # melewati validasi
  # mengembalikan data hasil pencarian dan parameter ke table.html untuk di-render
  a = main.main(request.args.get('querysearch'), int(request.args.get('querydoc')), int(request.args.get('querytype')))
  b = request.args.get('querysearch')
  c = request.args.get('querydoc')
  d = request.args.get('querytype')
  
  return render_template('table.html', data=a, len=[len(a[0]), len(a[1]), len(a[1][0])], query=b, doc=int(c), type=int(d), sec="%.2f"%(time()-timebefore))

@app.route('/doc/<path:path>')
def send_txt(path):
  '''
  Mengirim dokumen dengan judul path
  '''
  try:
    return render_template('doc.html', data=main.getSpecDoc(path, -1), judul=path)
  except FileNotFoundError:
    return redirect("/")

@app.errorhandler(404) 
def invalid_route(e):
  """
  mengatasi eror router tidak ditemukan dengan mengarahkan ke halaman utama
  """
  return redirect("/")
