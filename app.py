from flask import Flask, redirect, request, session, url_for, render_template
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Your Spotify app credentials
CLIENT_ID = '9d5dbc72aba7414f858c170fe3ca7bce'
CLIENT_SECRET = 'c1a28980d84944b4a3ba0e1d2370d74f'
REDIRECT_URI = 'http://localhost:5000/callback'
SCOPE = 'playlist-read-private user-library-read'

# Hard-coded playlist ID
PLAYLIST_ID = '1GSOX1PHYNDCRHFzMGlcY8'  # Replace with your actual playlist ID

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/songs')
def songs():
    if 'token' not in session:
        return redirect(url_for('login'))
    
    headers = {
        'Authorization': f'Bearer {session["token"]}'
    }
    response = requests.get(f'https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks', headers=headers)
    
    if response.status_code != 200:
        print("Error fetching playlist:", response.json())  # Log the error response
        return render_template('songs.html', songs=[])

    songs = response.json().get('items', [])
    print("Fetched songs:", songs)  # Log the fetched songs
    return render_template('songs.html', songs=songs)

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/card')
def card():
    return render_template('card.html')

@app.route('/heart')
def heart():
    return render_template('love.html')

@app.route('/login')
def login():
    auth_url = f'https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}'
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(token_url, {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    response_data = response.json()
    session['token'] = response_data['access_token']
    
    return redirect(url_for('songs'))  # Redirect to the songs route

if __name__ == '__main__':
    app.run(debug=True)
