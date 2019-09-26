from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from model import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///betterreads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(app)

@app.route('/api/description', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        book = DB.session.query(Book.author,
                                Book.rating, 
                                Book.isbn, 
                                Book.isbn13).filter(Book.title==title).all()[0]
        return f'''{title} is written by {book[0]}
                it has a rating of {book[1]}, the 
                isbn is {book[2], book[3]}'''
    return '''<form method="POST">
                  Title: <input type="text" name="title"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

if __name__ == '__main__':
    app.run(debug=True)