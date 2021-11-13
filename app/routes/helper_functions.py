from app.models.customer import Customer
from app.models.video import Video
from flask import Blueprint, jsonify, request, make_response, abort
from app.models.rental import Rental

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

def get_video_by_id(video_id):
    id = valid_int(video_id)
    video = Video.query.filter_by(id=id).one_or_none()    

    if video is None:
        response_body = {"message": f"Video {id} was not found"}
        abort(make_response(response_body, 404))   
    return video