from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

API_LOGIN = "4b3db3e92c23385671198d22411c1c21"
API_TOKEN = "4e9008f506893c0d5d09a05d253294c333a90e1c8a1225e53b"
API_BASE = f"https://api.jumpseller.com/v1"
AUTH_PARAMS = f"?login={API_LOGIN}&authtoken={API_TOKEN}"

def jumpseller_get(path, params=""):
    url = f"{API_BASE}{path}{AUTH_PARAMS}{params}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": "HTTP error", "details": str(e), "status_code": response.status_code}
    except Exception as e:
        return {"error": "Unknown error", "details": str(e)}

@app.route("/productos", methods=["GET"])
def productos():
    return jsonify(jumpseller_get("/products.json"))

@app.route("/producto/<int:product_id>", methods=["GET"])
def producto_por_id(product_id):
    return jsonify(jumpseller_get(f"/products/{product_id}.json"))

@app.route("/stock_bajo", methods=["GET"])
def stock_bajo():
    productos = jumpseller_get("/products.json")
    bajos = [p for p in productos if int(p["product"].get("stock", 0)) < 5]
    return jsonify(bajos)

@app.route("/categorias", methods=["GET"])
def categorias():
    return jsonify(jumpseller_get("/categories.json"))

@app.route("/ordenes", methods=["GET"])
def ordenes():
    return jsonify(jumpseller_get("/orders.json"))

@app.route("/orden/<int:order_id>", methods=["GET"])
def orden_por_id(order_id):
    return jsonify(jumpseller_get(f"/orders/{order_id}.json"))

@app.route("/clientes", methods=["GET"])
def clientes():
    return jsonify(jumpseller_get("/customers.json"))

@app.route("/cliente/<int:customer_id>", methods=["GET"])
def cliente_por_id(customer_id):
    return jsonify(jumpseller_get(f"/customers/{customer_id}.json"))

@app.route("/buscar_producto", methods=["GET"])
def buscar_producto():
    nombre = request.args.get("nombre", "")
    productos = jumpseller_get("/products.json")
    encontrados = [p for p in productos if nombre.lower() in p["product"]["name"].lower()]
    return jsonify(encontrados)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)