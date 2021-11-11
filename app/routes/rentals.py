import re
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, request, make_response, abort
from datetime import datetime, timedelta
from tests.test_wave_01 import CUSTOMER_ID

rentals_bp = Blueprint('rentals', __name__, url_prefix='/rentals')

# Helper Functions
def valid_int(number):
    try:
        id = int(number)
        return id 
    except:
        abort(400)

def get_customer_from_id(customer_id):
    id = valid_int(customer_id)
    customer = Customer.query.filter_by(id=id).one_or_none()    
    if customer is None:
        response_body = {"message": f"Customer {id} was not found"}
        abort(make_response(response_body, 404))   
    return customer

def get_video_from_id(customer_id):
    id = valid_int(customer_id)
    video = Video.query.filter_by(id=id).one_or_none()    
    if video is None:
        response_body = {"message": f"Video {id} was not found"}
        abort(make_response(response_body, 404))   
    return video

# Routes
# Post check-out
@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def create_rental():
    request_body = request.get_json()
    
    if "customer_id" not in request_body or "video_id" not in request_body:
        response_body = {"message": "Could not perform checkout"}
        return make_response(response_body, 400)
    else:
        customer = get_customer_from_id(request_body['customer_id'])
        video =  get_video_from_id(request_body['video_id'])
        videos_checked_out_count = Rental.query.filter_by(video_id=request_body['video_id']).count()
        available_inventory = video.total_inventory - videos_checked_out_count
        if available_inventory < 1:
            response_body = {"message": "Could not perform checkout"}
            return make_response(response_body, 400)
        else:
            videos_checked_out_count += 1
            available_inventory -= 1
            due_date = datetime.utcnow() + timedelta(days=7)
            new_rental = Rental(video_id=request_body['video_id'],
                                customer_id=request_body['customer_id'],
                                due_date=due_date, 
                                available_inventory=available_inventory,
                                videos_checked_out_count=videos_checked_out_count)
        db.session.add(new_rental)
        db.session.commit() 
        response_body = new_rental.to_dict()
        return make_response(response_body, 200)

# 