from flask import Flask, render_template, jsonify, request, redirect
from backend import main

# init
app = Flask(__name__, static_folder='frontend/static', template_folder='frontend/views')

# router
@app.route('/')
def homepage():
  """ index """
  return render_template('index.html')

@app.route('/perihal')
def perihal():
  """ perihal """
  return render_template('perihal.html')
    
@app.route('/search', methods=['GET'])
def search():
  """ api search """
  if not request.args.get('querydoc') or not request.args.get('querytype') or not request.args.get('querysearch'):
    return redirect("/")
  if not(int(request.args.get('querydoc')) > 0 and int(request.args.get('querydoc')) <= 150):
    return redirect("/")
  if int(request.args.get('querytype')) != 1 and int(request.args.get('querytype')) != 0:
    return redirect("/")
  a = main.main(request.args.get('querysearch'), int(request.args.get('querydoc')), int(request.args.get('querytype')))
  b = request.args.get('querysearch')
  c = request.args.get('querydoc')
  d = request.args.get('querytype')
  return render_template('table.html', data=a, len=[len(a[0]), len(a[1]), len(a[1][0])], query=b, doc=int(c), type=int(d))
  #return jsonify(a)
