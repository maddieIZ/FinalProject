import urllib.request as urllib
from flask import Flask, render_template, abort, session, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import os

images_FOLDER = os.path.join('static', 'images')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stockInfo.db'
app.config['UPLOAD_FOLDER'] = images_FOLDER
db = SQLAlchemy(app)
# API_KEY = "54111a47b9dfd8e47a37fa7366d981ea"
API_KEY = "6087327c6a4789a02ecab96d1937499e"

from static.database import Profiles, Tickers

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/company/<ticker>")
def test8(ticker):
    return render_template("company.html", ticker=ticker)

@app.route("/oil")
def test9():
    return render_template("oil.html")

@app.route("/DataSources")
def test10():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'database.png')
    return render_template("DataSourcesPage.html",user_image = full_filename)

@app.route("/oilanalysis")
def test11():
    return render_template("oilanalysis.html")

@app.route("/ML Presentation")
def test12():
    full_filename12 = os.path.join(app.config['UPLOAD_FOLDER'], 'nick-chong-N__BnvQ_w18-unsplash.jpg')
    return render_template("ML Presentation.html",user_image = full_filename12)

@app.route("/sharepriceanalyse")
def test13():
    return render_template("sharepriceanalyse.html")

# @app.route("/EnergyML")
# def test15():
#     return render_template("EnergyML.html")

@app.route("/API/profile/<ticker>")
def returnProfile(ticker):
    results = Profiles.query.filter_by(symbol=ticker).first()
    return results.profile


@app.route("/API/prices/<ticker>")
def returnPrices(ticker):
    results = fetch(
        f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?serietype=line&apikey={API_KEY}")
    return results


@app.route("/API/search/<ticker>")
def returnSearch(ticker):
    search_results = search(ticker)
    results = []
    for stock in search_results:
        results.append({"name": stock.name, "symbol": stock.symbol})
    results = jsonify(results)
    return results


@app.route("/API/display/")
def returnDisplay():
    results = fetch(
        f"https://financialmodelingprep.com/api/v3/company/stock/list?apikey={API_KEY}")
    return results


@app.route('/data')
def data():
    args = request.args
    return args


def fetch(link):
    with urllib.urlopen(link) as url:
        s = url.read()
        return s


def search(query):
    results = Tickers.query.filter(or_(Tickers.name.like(
        f"%{query}%"), Tickers.symbol.like(f"%{query}%"))).limit(10).all()
    return results


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
