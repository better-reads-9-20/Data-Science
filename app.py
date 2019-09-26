from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from model import Book

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///better_reads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(app)

@app.route('/')
def home():
    return "<h1>Welcome to Better Reads App</h1>"

@app.route('/books', methods=['GET', 'POST']) #allow POST requests
def query():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        title = request.form.get('title')
        book = DB.session.query(Book.title, Book.author, Book.rating, Book.webpage).filter(Book.title == title).one()
        #description = request.form['descrip']
        return f'{book[0]} is written by {book[1]} its rating {book[2]} the webpage is {book[3]}'

    return '''<form method="POST">
                  Title: <input type="text" name="title"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

if __name__ == '__main__':
    app.run(debug=True)
