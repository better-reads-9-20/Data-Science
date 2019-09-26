from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///better_reads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(app)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Better Reads Database</h1><p>This site is a prototype API for Better Reads.</p>"

@app.route('/api/v1/description', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        description = request.form.get('description')

app.run()
