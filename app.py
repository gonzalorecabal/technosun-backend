from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

API_LOGIN = "4b3db3e92c23385671198d22411c1c21"
API_TOKEN = "4e9008f506893c0d5d09a05d253294c333a90e1c8a1225e53b"
API_BASE = "https://api.jumpseller.com/v1"
AUTH_PARAMS = f"?login={API_LOGIN}&authtoken={API_TOKEN}"

def jumpseller_get(path, extra_params=""):
    url = f"{API_BASE}{path}{AUTH_PARAMS}{extra_params}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": "HTTP error", "details": str(e), "status_code": response.status_code}
    except Exception as e:
        return {"error": "Unknown error", "details": str(e)}

def obtener_todos_los_productos(limit=100):
    productos = []
    page = 1
    while True:
        data = jumpseller_get("/products.json", f"&page={page}&limit={limit}")
        if isinstance(data, list):
            productos.extend(data)
            if len(data) < limit:
                break
            page += 1
        else:
            break
    return productos

@app.route("/productos", methods=["GET"])
def productos():
    return jsonify(obtener_todos_los_productos())

@app.route("/producto/<int:product_id>", methods=["GET"])
def producto_por_id(product_id):
    return jsonify(jumpseller_get(f"/products/{product_id}.json"))

@app.route("/producto_variantes/<int:product_id>", methods=["GET"])
def producto_variantes(product_id):
    data = jumpseller_get(f"/products/{product_id}.json")
    if "product" in data:
        return jsonify(data["product"].get("variants", []))
    return jsonify({"error": "Producto no encontrado o sin variantes"})

@app.route("/stock_bajo", methods=["GET"])
def stock_bajo():
    productos = obtener_todos_los_productos()
    bajos = [p for p in productos if int(p["product"].get("stock", 0)) < 5]
    return jsonify(bajos)

@app.route("/categoria", methods=["GET"])
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
    nombre = request.args.get("nombre", "").lower()
    productos = obtener_todos_los_productos()
    encontrados = [p for p in productos if nombre in p["product"]["name"].lower()]
    return jsonify(encontrados)

@app.route("/producto_variante_max_stock/<int:product_id>", methods=["GET"])
def producto_variante_max_stock(product_id):
    data = jumpseller_get(f"/products/{product_id}.json")
    if "product" in data:
        variantes = data["product"].get("variants", [])
        if variantes:
            max_variante = max(variantes, key=lambda v: int(v.get("stock", 0)))
            return jsonify(max_variante)
    return jsonify({"error": "No se encontraron variantes"})

@app.route("/producto_variante_mas_barata/<int:product_id>", methods=["GET"])
def producto_variante_mas_barata(product_id):
    data = jumpseller_get(f"/products/{product_id}.json")
    if "product" in data:
        variantes = data["product"].get("variants", [])
        if variantes:
            mas_barata = min(variantes, key=lambda v: float(v.get("price", "9999999")))
            return jsonify(mas_barata)
    return jsonify({"error": "No se encontraron variantes"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)