from app import db
import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(80), nullable=False)
#     postal_code = db.Column(db.String(10))
#     # What is the best datatype for phone number?
#     phone_number = db.Column(db.String(32))
#     registered_at= db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow())

#     def to_json(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "postal_code": self.postal_code,
#             "registered_at":self.registered_at,
#         }