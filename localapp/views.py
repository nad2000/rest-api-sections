from app import app
from db import db

@app.route("/cleandb")
def cleandb():
    db.engine.execute("DELETE FROM users");
    db.engine.execute("DELETE FROM items");
    db.engine.execute("DELETE FROM stores");
    db.session.commit()
    return "OK"
