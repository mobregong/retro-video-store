import sys
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app.routes.customers import get_customer_from_id
from app.routes.videos import get_video_by_id, valid_int
from flask import Blueprint, jsonify, request, make_response, abort
from datetime import datetime, timedelta

rentals_bp = Blueprint('rentals', __name__, url_prefix='/rentals')



# Routes
# Post check-out
@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def check_out_video():
    request_body = request.get_json()
    error_message = {"message": "Could not perform checkout"}, 400

    if "customer_id" not in request_body or "video_id" not in request_body:
        return make_response(error_message)

    customer = get_customer_from_id(request_body['customer_id'])
    video =  get_video_by_id(request_body['video_id'])
    videos_checked_out_by_customer_count = Rental.query.filter_by(customer_id=customer.id).count()
    videos_id_checked_out_count = Rental.query.filter_by(video_id=video.id).count()
    available_inventory = video.total_inventory - videos_id_checked_out_count

    if not available_inventory:   
        return make_response(error_message)
    else:
        videos_checked_out_by_customer_count += 1
        available_inventory -= 1
        due_date = datetime.utcnow() + timedelta(days=7)

        new_rental = Rental(video_id=video.id,
                            customer_id=customer.id,
                            due_date=due_date, 
                            available_inventory=available_inventory,
                            videos_checked_out_count=videos_checked_out_by_customer_count)

    db.session.add(new_rental)
    db.session.commit() 
    response_body = new_rental.to_dict()
    return make_response(response_body, 200)



@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def check_in_video():

    request_body = request.get_json()

    if "customer_id" not in request_body or "video_id" not in request_body:
        return make_response({"message": "Could not perform check in"}, 400)

    customer = get_customer_from_id(request_body['customer_id'])
    video =  get_video_by_id(request_body['video_id'])
    rentals = Rental.query.filter_by(video_id=video.id, customer_id=customer.id).one_or_none()
    if rentals == None:
        return make_response({"message": "No outstanding rentals for customer 1 and video 1"}, 400)

# video was not checked in yet 
    if not rentals.checked_in:
        # update available_inventory and checked ou count
        rentals.due_date = None,
        rentals.available_inventory =  rentals.available_inventory + 1
        rentals.videos_checked_out_count=  rentals.videos_checked_out_count - 1
        rentals.checked_in =  datetime.utcnow()

        db.session.commit() 

    response_body = rentals.to_dict()
    return make_response(response_body, 200)