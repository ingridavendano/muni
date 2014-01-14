# -----------------------------------------------------------------------------
# controller.py 
# Created by Ingrid Avendano 1/6/14. 
# -----------------------------------------------------------------------------
# Contols different views and runs model depending on the view. 
# -----------------------------------------------------------------------------

import model
import os
from flask import Flask, render_template, request, session
import json

# -----------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = "uber_challenge"

# grab Google Maps API
config_file = open("./config.json")
config_data = json.load(config_file) 
config_file.close()

GOOGLE_MAPS_TOKEN = config_data["GOOGLE_MAPS"]

# -----------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def index():
    # return render_template("master.html", token=GOOGLE_MAPS_TOKEN)
    if session.get("location") and session.get("code"):
        return render_template("index.html", 
            display=True, 
            stop=session["code"], 
            location=session["location"],
            token=GOOGLE_MAPS_TOKEN
            )
    else: 
        return render_template("index.html", display=False, stop="", location="")


@app.route("/map", methods=["GET"])
def map():
    return render_template("map.html", token=GOOGLE_MAPS_TOKEN)


@app.route("/getTimes.json", methods=["GET"])
def geo():
    latitude = request.args.get('lat')
    longitude = request.args.get('lng')

    session["location"] = (latitude, longitude)
    json_departures = model.geo_fence(latitude, longitude)

    return json_departures

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
