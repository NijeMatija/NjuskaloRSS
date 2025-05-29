#!/usr/bin/env python3
from flask import Flask, Response, send_file
import os
import subprocess
import threading
import time

app = Flask(__name__)

def run_rss_generator():
    """Pokreni RSS generator u pozadini"""
    while True:
        try:
            subprocess.run(['python', 'njuskalo-rssgen.py'], check=True)
            print("RSS generator uspješno pokrenut")
        except subprocess.CalledProcessError as e:
            print(f"Greška pri pokretanju RSS generatora: {e}")
        time.sleep(1800)  # Čekaj 30 minuta

@app.route('/')
def index():
    return '''
    <h1>Njuškalo RSS Generator</h1>
    <p>RSS feed za kuće u Krapinsko-zagorskoj županiji:</p>
    <a href="/rss">njuskalo-kuce.xml</a>
    '''

@app.route('/rss')
def rss_feed():
    """Serviraj RSS feed"""
    try:
        return send_file('njuskalo-kuce.xml', mimetype='application/rss+xml')
    except FileNotFoundError:
        return Response("RSS feed još nije generiran. Pokušajte kasnije.", status=404)

if __name__ == '__main__':
    # Pokreni RSS generator u pozadini
    rss_thread = threading.Thread(target=run_rss_generator, daemon=True)
    rss_thread.start()
    
    # Pokreni web server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 