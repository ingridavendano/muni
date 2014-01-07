# --------------------------------------------------------------------------- #
# model.py                                                                    #
# Created by Ingrid Avendano 1/6/14.                                          #
# --------------------------------------------------------------------------- #
# Grabs all the data needed for the website.                                  # 
# --------------------------------------------------------------------------- #

import os
from flask import Flask, render_template, request

# --------------------------------------------------------------------------- #

app = Flask(__name__)
app.secret_key = "uber_challenge"

# --------------------------------------------------------------------------- #

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    app.run(debug=True)