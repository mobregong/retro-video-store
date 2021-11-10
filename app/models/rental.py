from app import db

class Rental(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True,nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True,nullable=False)
    due_date = db.Column(db.DateTime(timezone=True),nullable=False)
    available_inventory = db.Column(db.Integer, nullable=False)
    videos_checked_out_count = db.Column(db.Integer, nullable=False)


    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "available_inventory": self.available_inventory,
            "videos_checked_out_count": self.videos_checked_out_count
        }