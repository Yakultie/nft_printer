from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

def getDirectImageURL(openSeaURL):
    driver = webdriver.Chrome()
    url = openSeaURL
    driver.maximize_window()

    try:
        driver.get(url)

        time.sleep(5)
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html.parser")

        main_image = soup.find("img", attrs={"class": "Image--image", "style": "width: auto; height: auto; max-width: 100%; max-height: 100%; border-radius: initial;"})

        driver.quit()

        return main_image['src']

    except:
        return False

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["POST"])
@limiter.limit("10/minute")
def index_post():
    msg = ""
    opensea_url = request.form.get("opensea_url")
    confirm1state = request.form.get("confirm1")
    confirm2state = request.form.get("confirm2")
    """
    print(opensea_url)
    print(confirm1state == "on")
    print(confirm2state == "on")
    """
    if not opensea_url:
        msg = "OpenSea URL not provided"
        image_url = "not_provided"
    if not ((confirm1state == "on") and (confirm2state == "on")):
        msg = "You have not confirmed ownership of your NFT"
        image_url = "not_provided"
    else:
        image_url = getDirectImageURL(opensea_url)
    print(image_url)

    return render_template("index.html", msg=msg, image_url=image_url)

@app.route("/", methods=["GET"])
def index_get():
    return render_template("index.html", image_url="not_provided")

if __name__ == '__main__':
    from waitress import serve
    port = int(os.environ.get('PORT', 5000))
    serve(app, host="0.0.0.0", port=port)

