# -----------------------------------------------------------------------------
# controller.py 
# Created by Ingrid Avendano 1/6/14. 
# -----------------------------------------------------------------------------
# Contols different views and runs model depending on the view. 
# -----------------------------------------------------------------------------

import model
import os
from flask import Flask, render_template
import json

# -----------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = "hey_gurl_hey"

# grab Google Maps API
with open("./config.json") as api_key:
    GOOGLE_MAPS_TOKEN = json.load(api_key)["GOOGLE_MAPS"]

# -----------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def index():
    """ Render template to include Google API key. """ 
    return render_template("index.html", token=GOOGLE_MAPS_TOKEN)


@app.route("/lat/<latitude>/lng/<longitude>/rad/<radius>/stops")
def nearest_muni_departures(latitude, longitude, radius): 
    """ Grab JSON data that being fetch from Backbone. """
    json_departures = model.geo_fence(latitude, longitude, radius)
    return json_departures

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.getenv('CIRCUIT_PORT', 5000))
    app.run(host='0.0.0.0', port=port)
