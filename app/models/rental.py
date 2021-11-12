from app import db
import datetime

class Rental(db.Model):

    # relationship
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True,nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True,nullable=False)
    # extra columns
    due_date = db.Column(db.DateTime(timezone=True),nullable=False)
    available_inventory = db.Column(db.Integer, nullable=False)
    videos_checked_out_count = db.Column(db.Integer, nullable=True) #changed to true , if == 0 then videos_checked_out_count
    checked_in = db.Column(db.DateTime(timezone=True), nullable=True) # else False 
    # if checked in == date else == False 



    def to_dict(self):

        if not self.checked_in:
            return {
                "customer_id": self.customer_id,
                "video_id": self.video_id,
                "due_date": self.due_date,
                "available_inventory": self.available_inventory,
                "videos_checked_out_count": self.videos_checked_out_count
            }
        return {
                "customer_id": self.customer_id,
                "video_id": self.video_id,
                "due_date": self.due_date,
                "available_inventory": self.available_inventory,
                "videos_checked_out_count": self.videos_checked_out_count if self.videos_checked_out_count else False,
                "checked_in": self.checked_in
            }