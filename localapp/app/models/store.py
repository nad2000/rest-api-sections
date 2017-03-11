from db import db

class Store(db.Model):

    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    items = db.relationship("Item", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return dict(id=self.id, name=self.name, items=[i.to_dict() for i in self.items.all()])

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_items(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

