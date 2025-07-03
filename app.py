from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

API_LOGIN = "4b3db3e92c23385671198d22411c1c21"
API_TOKEN = "4e9008f506893c0d5d09a05d253294c333a90e1c8a1225e53b"
API_BASE = f"https://api.jumpseller.com/v1"
AUTH_PARAMS = f"?login={API_LOGIN}&authtoken={API_TOKEN}"

def jumpseller_get(path):
    url = f"{API_BASE}{path}{AUTH_PARAMS}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": "HTTP error", "details": str(e), "status_code": response.status_code}
    except Exception as e:
        return {"error": "Unknown error", "details": str(e)}

@app.route("/producto_variantes/<int:product_id>", methods=["GET"])
def producto_variantes(product_id):
    data = jumpseller_get(f"/products/{product_id}.json")
    if "product" in data:
        return jsonify(data["product"].get("variants", []))
    return jsonify({"error": "Producto no encontrado o sin variantes"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)