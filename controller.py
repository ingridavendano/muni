# --------------------------------------------------------------------------- #
# controller.py                                                               #
# Created by Ingrid Avendano 1/6/14.                                          #
# --------------------------------------------------------------------------- #
# Contols different views and runs model depending on the view.               #
# --------------------------------------------------------------------------- #

import os
from flask import Flask, render_template, request

# --------------------------------------------------------------------------- #

app = Flask(__name__)
app.secret_key = "uber_challenge"
GOOGLE_MAPS_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# --------------------------------------------------------------------------- #

@app.route("/", methods=["GET"])
def index():
    return render_template("master.html", token=GOOGLE_MAPS_TOKEN)

# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    app.run(debug=True)
