from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape

app = Flask(__name__)

mongo=PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():
    mars_info=mongo.db.mars_info.find_one()

    return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def web_scrape():
    mars_data=scrape.scrape()

    mongo.db.mars_info.update({},mars_data, upsert=True)

    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)