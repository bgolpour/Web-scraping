from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
#import os
# Create an instance of our Flask app.
app = Flask(__name__)

# Use flask_pymongo to set up the mongo connection
# app.config["MONGO_URI"] = os.environ.get('authenticatio')
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#mongo = PyMongo(app, uri="mongodb://localhost:27017//mars_app")

# # Pass connection to the pymongo instance.
# client = pymongo.MongoClient(conn)

# # Connect to a database. Will create one if not already available.
# db = client.mars_db

# # Drops collection if available to remove duplicates
# db.mars.drop()


# Set route main
@app.route('/')
def index():
    # find data
    mars = mongo.db.mars.find_one()

    # return template and data
    return render_template("index.html", mars = mars)

# Root that will trigger scrape function
@app.route("/scrape")
def scrape():
    # Run scrapped functions
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    print(mars_data)
    mars.update({}, {"$set": mars_data}, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
