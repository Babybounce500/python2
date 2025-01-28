import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime

def load_data(ticker, start, end):
    """
    Lädt historische Aktienkurse von Yahoo Finance.
    
    :param ticker: Aktienmarktsymbol
    :param start: Startdatum (YYYY-MM-DD)
    :param end: Enddatum (YYYY-MM-DD)
    :return: DataFrame mit den historischen Kursdaten
    """
    data = yf.download(ticker, start=start, end=end)
    return data

def calculate_moving_average(data, window):
    """
    Berechnet den gleitenden Durchschnitt über einen bestimmten Zeitraum.
    
    :param data: DataFrame mit den Kursdaten
    :param window: Zeitraum für den gleitenden Durchschnitt
    :return: Series mit dem gleitenden Durchschnitt
    """
    return data['Close'].rolling(window=window).mean()

def calculate_rsi(data, window=14):
    """
    Berechnet den Relative Strength Index (RSI).
    
    :param data: DataFrame mit den Kursdaten
    :param window: Zeitraum für die RSI-Berechnung
    :return: Series mit dem RSI
    """
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def plot_data(data, moving_average, rsi):
    """
    Plottet die Kursdaten, den gleitenden Durchschnitt und den RSI.
    
    :param data: DataFrame mit den Kursdaten
    :param moving_average: Series mit dem gleitenden Durchschnitt
    :param rsi: Series mit dem RSI
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Kursdaten und gleitenden Durchschnitt
    ax1.plot(data['Close'], label='Schlusskurs', color='blue')
    ax1.plot(moving_average, label='Gleitender Durchschnitt', color='orange')
    ax1.set_title('Aktienkurse und gleitender Durchschnitt')
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

    plt.tight_layout()
    plt.show()

def advanced_analysis(data):
    max_close = data['Close'].max()
    min_close = data['Close'].min()
    total_volume = data['Volume'].sum()    

    print(f'Maximale Schlusskurs: {max_close}')
    print(f'Minimaler Schlusskurs: {min_close}')
    print(f'Totales Volumen: {total_volume}')

def main():
    # Benutzer nach dem Ticker fragen
    ticker = input("Gib das Aktienkürzel ein (z.B. AAPL für Apple, JPM für JPMorgan): ").upper()
    
    start_date = '2020-01-01'
    end_date = datetime.today().strftime('%Y-%m-%d')  # Heute als Enddatum

    window = 20  # Zeitraum für den gleitenden Durchschnitt (in Tagen)

    # Daten laden
    stock_data = load_data(ticker, start_date, end_date)

    # Überprüfen Sie, ob Daten vorhanden sind
    if not stock_data.empty:
        # Gleitenden Durchschnitt berechnen
        moving_avg = calculate_moving_average(stock_data, window)

        # RSI berechnen
        rsi = calculate_rsi(stock_data)

        # Daten plotten
        plot_data(stock_data, moving_avg, rsi)

        # Erweiterte Analyse durchführen
        advanced_analysis(stock_data)
    else:
        print(f"Es wurden keine Daten für das Ticker-Symbol {ticker} zurückgegeben. Bitte überprüfen Sie das Ticker-Symbol.")

if __name__ == "__main__":
    main()
