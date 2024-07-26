from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/birthday_wishes')
def birthday_wishes():
    return render_template('birthday_wishes.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/card')
def card():
    return render_template('card.html')

@app.route('/heart')
def heart():
    return render_template('love.html')

if __name__ == '__main__':
    app.run(debug=True)
