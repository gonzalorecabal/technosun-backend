from flask import Flask, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

API_LOGIN = "4b3db3e92c23385671198d22411c1c21"
API_TOKEN = "4e9008f506893c0d5d09a05d253294c333a90e1c8a1225e53b"
STORE_URL = "https://technosun-cl.jumpseller.com"
AUTH = HTTPBasicAuth(API_LOGIN, API_TOKEN)

@app.route("/productos", methods=["GET"])
def productos():
    response = requests.get(f"{STORE_URL}/api/v1/products.json", auth=AUTH)
    return jsonify(response.json())

@app.route("/stock_bajo", methods=["GET"])
def stock_bajo():
    response = requests.get(f"{STORE_URL}/api/v1/products.json", auth=AUTH)
    productos = response.json()
    bajos = [p for p in productos if int(p["product"].get("stock", 0)) < 5]
    return jsonify(bajos)

if __name__ == "__main__":
    app.run()