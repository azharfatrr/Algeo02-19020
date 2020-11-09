from flask import Flask, request, render_template, jsonify
import sys
sys.path.insert(1, 'backend')
import main, read_doc, test_code

# init
app = Flask(__name__, static_folder='frontend/static', template_folder='frontend/views')

# router
@app.route('/')
def homepage():
  """ index """
  return render_template('index.html')
    
@app.route('/search', methods=['GET', 'POST'])
def search():
  """ api search """
  return "OK"