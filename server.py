from flask import Flask, render_template, jsonify
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
  a = main.main(request.args.get('querysearch'), int(request.args.get('querydoc')), int(request.args.get('querytype')))
  return render_template('table.html', data=a, len=[len(a[0]), len(a[1])])
  #return jsonify(a)
