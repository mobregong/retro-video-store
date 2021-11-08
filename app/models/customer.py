from app import db
import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone_number": self.phone_number,
            "registered_at": self.registered_at
        }