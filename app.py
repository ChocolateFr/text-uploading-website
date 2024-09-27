from flask import *
from string import ascii_lowercase
from watchdict import WatchDict
from random import choice

app = Flask(__name__)
db = WatchDict('data.json')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/send', methods=['post', 'get'])
def send():
    if request.method == 'POST':
        keys = list(db['uploads'].keys())
        key  = ''.join([choice(ascii_lowercase) for i in range(7)])
        while key in keys:
            key  = ''.join([choice(ascii_lowercase) for i in range(7)])
        db['uploads'][key] = request.form.get('text')
        db.save_state()
        return render_template('success.html', title='Upload url', text=f'{db["__domain__"]}/get/{key}')
    else:
        return render_template('index.html')
    
@app.route('/get/<item>')
def get_item(item):
    if item in db['uploads']:
        return render_template('success.html', title='Text', text=db['uploads'][item])
    return "404"
    
