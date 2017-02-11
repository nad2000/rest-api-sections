from flask import Flask

app = Flask(__name__)

@app.route('/')  # http://xxx/
def home():
    return "Hello, World!"

@app.route("/store", methods=["POST"])
def create_store():
    pass

@app.route("/store/<string:name>")
def get_store(name):
    pass


@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name):
    pass


@app.route("/store/<string:name>/item")
def get_items_in_store(name):
    pass

if __name__ == "__main__":
    app.run(port=5000)

