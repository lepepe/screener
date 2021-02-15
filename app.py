import os, csv
import talib
import yfinance as yf
import datetime
import pandas
from flask import Flask, escape, request, render_template
from patterns import candlestick_patterns
import config
import psycopg2
import psycopg2.extras

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS, port=config.DB_PORT)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute(""" SELECT * FROM stock """)
rows = cursor.fetchall()

app = Flask(__name__)
today = datetime.datetime.today().strftime('%Y-%m-%d')
first_date = datetime.datetime.today().replace(month=1, day=1).strftime('%Y-%m-%d')

@app.route('/snapshot')
def snapshot():
    stocks = {}
    for row in rows: 
        symbol = row['symbol']
        data = yf.download(symbol, start=first_date, end=today)
        data.to_csv('datasets/daily/{}.csv'.format(symbol))

    return {
        "code": "success"
    }

@app.route('/')
def index():
    pattern  = request.args.get('pattern', False)
    stocks = {}
    for row in rows: 
        stocks[row['symbol']] = {'company': row['name']}

    if pattern:
        for filename in os.listdir('datasets/daily'):
            df = pandas.read_csv('datasets/daily/{}'.format(filename))
            pattern_function = getattr(talib, pattern)
            symbol = filename.split('.')[0]

            try:
                results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                last = results.tail(1).values[0]

                if last > 0:
                    stocks[symbol][pattern] = 'bullish'
                elif last < 0:
                    stocks[symbol][pattern] = 'bearish'
                else:
                    stocks[symbol][pattern] = None
            except Exception as e:
                print('failed on filename: ', filename)

    return render_template('index.html', candlestick_patterns=candlestick_patterns, stocks=stocks, pattern=pattern)
