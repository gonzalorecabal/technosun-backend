from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

API_LOGIN = "4b3db3e92c23385671198d22411c1c21"
API_TOKEN = "4e9008f506893c0d5d09a05d253294c333a90e1c8a1225e53b"
BASE_URL = f"https://api.jumpseller.com/v1/products.json?login={API_LOGIN}&authtoken={API_TOKEN}"

@app.route("/productos", methods=["GET"])
def productos():
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": "HTTP error", "details": str(e), "status_code": response.status_code}), 500
    except Exception as e:
        return jsonify({"error": "Unknown error", "details": str(e)}), 500

@app.route("/stock_bajo", methods=["GET"])
def stock_bajo():
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        productos = response.json()
        bajos = [p for p in productos if int(p["product"].get("stock", 0)) < 5]
        return jsonify(bajos)
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": "HTTP error", "details": str(e), "status_code": response.status_code}), 500
    except Exception as e:
        return jsonify({"error": "Unknown error", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)