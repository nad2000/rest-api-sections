from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

stores = [
        {
            "name": "My Wonderful Store",
            "items": [dict(name="My Item", price=15.99)]
            }
        ]


@app.route('/')  # http://xxx/
def home():
    ##return "Hello, World!"
    return render_template("index.html")


@app.route('/reset', methods=["POST"])
def reset():
    global stores
    stores = []
    return jsonify(stores)

# TEST:
# curl -H "Content-Type: application/json" -d '{"name": "a new store"}' -X POST http://127.0.0.1:5000/store
@app.route("/store", methods=["POST"])
def create_store():
    req_data = request.get_json()
    new_store = dict(name=req_data["name"], items=[])
    stores.append(new_store)
    return jsonify(new_store)


@app.route("/store/<string:name>")
def get_store(name):
    for s in stores:
        if s.get("name") == name:
            return jsonify(s)
    else:
        return jsonify({"message": "store not found"})


@app.route("/store")
@app.route("/stores")
def get_stores():
    # opt to use dict to make it extensible:
    return jsonify({"stores": stores})

@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name):
    req_data = request.get_json()
    for s in stores:
        if s.get("name") == name:
            new_item = dict(name=req_data.get("name"), price=req_data.get("price"))
            s["items"].append(new_item)
            return jsonify(s)
    else:
        return jsonify({"message": "store not found"})


@app.route("/store/<string:name>/item")
def get_items_in_store(name):
    for s in stores:
        if s.get("name") == name:
            return jsonify({"item": s.get("items", [])})
    else:
        return jsonify({"message": "store not found"})


if __name__ == "__main__":
    app.run(port=5000, debug=True)

