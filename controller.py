# -----------------------------------------------------------------------------
# controller.py 
# Created by Ingrid Avendano 1/6/14. 
# -----------------------------------------------------------------------------
# Contols different views and runs model depending on the view. 
# -----------------------------------------------------------------------------

import model
import os
from flask import Flask, render_template, request
import json

# -----------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = "uber_challenge"

# grab Google Maps API
config_file = open("./config.json")
config_data = json.load(config_file) 
config_file.close()

GOOGLE_MAPS_TOKEN = config_data["GOOGLE_API_KEY"]

# -----------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/map", methods=["GET"])
def map():
    return render_template("map.html", token=GOOGLE_MAPS_TOKEN)


@app.route("/getTimes.json", methods=["GET"])
def geo():
    longitude = request.args.get('lon')
    latitude = request.args.get('lat')

    print latitude, longitude
    model.geo_fencing_for_nearest_stop(latitude, longitude)
    return '{"text":"I am JSON"}'

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
