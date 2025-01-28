import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime
from flask import Flask, render_template, send_file
import io
from flask_cors import CORS  # Importiere Flask-CORS

app = Flask(__name__)
CORS(app)  # Aktiviere CORS für die gesamte App

def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    return data

def calculate_moving_average(data, window):
    return data['Close'].rolling(window=window).mean()

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot/<ticker>')
def plot(ticker):
    # Daten laden
    start_date = '2020-01-01'
    end_date = datetime.today().strftime('%Y-%m-%d')
    stock_data = load_data(ticker, start_date, end_date)

    window = 20  # Zeitraum für den gleitenden Durchschnitt (in Tagen)
    moving_avg = calculate_moving_average(stock_data, window)
    rsi = calculate_rsi(stock_data)

    # Plot erzeugen
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Kursdaten und gleitenden Durchschnitt
    ax1.plot(stock_data['Close'], label='Schlusskurs', color='blue')
    ax1.plot(moving_avg, label='Gleitender Durchschnitt', color='orange')
    ax1.set_title(f'Aktienkurse und gleitender Durchschnitt für {ticker}')
    ax1.set_xlabel('Datum')
    ax1.set_ylabel('Preis in USD')
    ax1.legend()
    ax1.grid()

    # RSI-Diagramm
    ax2.plot(rsi, label='RSI', color='purple')
    ax2.axhline(70, linestyle='--', alpha=0.5, color='red')
    ax2.axhline(30, linestyle='--', alpha=0.5, color='green')
    ax2.set_title('Relative Strength Index (RSI)')
    ax2.set_xlabel('Datum')
    ax2.set_ylabel('RSI')
    ax2.legend()
    ax2.grid()

    # Bild als Bytes streamen
    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
