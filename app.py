from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from decouple import config
import pandas as pd


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(app)

df = pd.read_csv('thirty_k_imputed.csv')

class Book(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    webpage = DB.Column(DB.BigInteger)
    title = DB.Column(DB.String(300))
    author = DB.Column(DB.String(100))
    descrip = DB.Column(DB.String(25000))
    rating = DB.Column(DB.Float)
    num_ratings = DB.Column(DB.String(30))
    num_reviews = DB.Column(DB.String(30))
    isbn = DB.Column(DB.String(110))
    isbn13 = DB.Column(DB.String(110))
    binding = DB.Column(DB.String(100))
    edition = DB.Column(DB.String(125))
    num_pages = DB.Column(DB.String(100))
    published_on = DB.Column(DB.String(150))
    genres = DB.Column(DB.String(300))

    def __repr__(self):
        return f'Book: {self.title} writtien by {self.author}'


@app.route('/api/description', methods=['POST'])
def api():
    if request.method == 'POST':
        try:
            title = request.get_json('title')
            book = DB.session.query(Book.author,
                                    Book.rating, 
                                    Book.isbn, 
                                    Book.isbn13).filter(Book.title==title).all()[0]
            return f'''{title} is written by {book[0]}
                    it has a rating of {book[1]}, the 
                    isbn is {book[2], book[3]}'''
        except Exception:
            return f"That book is made up! {title} {type(title)}"
    return '''<form method="POST">
                  Title: <input type="text" name="title"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

if __name__ == '__main__':
    app.run(debug=True)