## API pseudo code
from .app import app, DB
## receive post request of string

## put string through the model wrangle

## get model output

## send back books that backend pulls from website, jsonified

# Create model
class Book(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    webpage = DB.Column(DB.String(40))
    title = DB.Column(DB.String(40))
    author = DB.Column(DB.String(40))
    descrip = DB.Column(DB.String(1500))
    rating = DB.Column(DB.Float)
    num_ratings = DB.Column(DB.String(30))
    num_reviews = DB.Column(DB.String(30))
    isbn = DB.Column(DB.String(15))
    isbn13 = DB.Column(DB.String(15))
    binding = DB.Column(DB.String(15))
    edition = DB.Column(DB.String(50))
    num_pages = DB.Column(DB.String(15))
    published_on = DB.Column(DB.String(150))
    genres = DB.Column(DB.String(1000))
