from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental 
from app.routes.customers import get_customer_from_id
from datetime import datetime
from flask import Blueprint, jsonify, make_response, request, abort


video_bp = Blueprint('video', __name__, url_prefix='/videos')


''' Post - create a new video'''
@video_bp.route("", methods=["POST"])
def add_video():
    request_body = request.get_json() 

    try:   
        new_video = Video(title = request_body["title"], 
                        release_date = request_body["release_date"],
                        total_inventory = request_body["total_inventory"])

        db.session.add(new_video)
        db.session.commit()
        response_body = {"title": new_video.title,
                        "id": new_video.id,
                        "release_date": new_video.release_date,
                        "total_inventory": new_video.total_inventory}

        return make_response(jsonify(response_body),201)
    except KeyError as err:
        response_body = {"details": f"Request body must include {err.args[0]}."}
        return make_response(response_body, 400) 

'''Get - real all videos'''
@video_bp.route("", methods=["GET"])
def read_all():
    videos = Video.query.all()


    try:
        response_body = []
        for video in videos:
            response_body.append(video.to_json())
        
        return make_response(jsonify(response_body),200)

    except:
        abort(400)


'''GET - read one'''
@video_bp.route("/<video_id>", methods=["GET"])
def read_one_video(video_id):
    video = get_video_by_id(video_id)

    try:
        response_body = video.to_json()
        print(response_body)
        return make_response(jsonify(response_body),200)
    except:
        abort(400)


''' PUT- update whole video row'''

@video_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id): 
    video = get_video_by_id(video_id)

    try:
        request_body = request.get_json()      
        if "title" in request_body:
            video.title = request_body["title"]
        if "release_date" in request_body:
            video.release_date = request_body["release_date"]
        if "total_inventory" in request_body:
            video.total_inventory = request_body["total_inventory"]

        db.session.commit()
        response_body = video.to_json()

        return make_response(response_body, 200)
    except KeyError as err:
        abort(400)


'''DELETE - one item by id'''
@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id): 
    video = get_video_by_id(video_id)
    rentals = Rental.query.filter_by(video_id=video_id).all()

    try:
        if rentals != None:
            for rental in rentals:
                db.session.delete(rental)
                db.session.commit()
        db.session.delete(video)
        db.session.commit()
        response_body ={"id": video.id}

        return make_response(response_body), 200

    except Exception:
        abort(422)



@video_bp.route("/<id>/rentals", methods=["GET"])
def handle_video_rental(id):

    if get_video_by_id(id):
        rentals  = Rental.query.filter_by(video_id=id).all()

    response_body = []
    for rental in rentals:
        customer =  get_customer_from_id(rental.customer_id)
        response_body.append({"due_date": rental.due_date,
                            "name": customer.name,
                            "phone": customer.phone,
                            "postal_code":customer.postal_code})

    return make_response(jsonify(response_body),200)



''' Helper Functions '''

def get_video_by_id(video_id):
    id = valid_int(video_id)
    video = Video.query.filter_by(id=id).one_or_none()    

    if video is None:
        response_body = {"message": f"Video {id} was not found"}
        abort(make_response(response_body, 404))   
    return video

def valid_int(number):
    try:
        id = int(number)
        return id 
    except:
        abort(400)




'''Error Handlers'''


@video_bp.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "Bad request"}),400

@video_bp.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}),422
