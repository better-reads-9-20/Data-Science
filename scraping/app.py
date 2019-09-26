from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///better_reads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        description = request.form.get('description')
        return description
    return '''<form method="POST">
                  Title: <input type="text" name="title"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

@app.route('/api/v1/description', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        description = request.form.get('description')
        
@app.route('/json-example', methods=['POST'])
def sample_json():
    req_data = request.get_json()

    language = req_data['language']
    framework = req_data['framework']
    python_version = req_data['version_info']['python']
    example = req_data['examples'][0]
    boolean_test = req_data['boolean_test']
    
    return f'''
            The language is: {language}

            The framework is: {framework}

            The Python version is: {python_version}

            The item at index 0 in the example list is: {example}

            The boolean value is {boolean_test}
            '''
if __name__ == '__main__':
    app.run(debug=True)