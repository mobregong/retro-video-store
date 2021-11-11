from app import db
from app.models.video import Video
from datetime import datetime
from flask import Blueprint, jsonify, make_response, request, abort


video_bp = Blueprint('video', __name__, url_prefix='/videos')



''' Post - create a new video'''
@video_bp.route("", methods=["POST"])
def add_video():
    request_body = request.get_json() 

    try:
        if "title" not in request_body:
            response_body = {"details": 'Request body must include title.'}
            return make_response(response_body, 400)
        elif "release_date" not in request_body:
            response_body = {"details": 'Request body must include release_date.'}
            return make_response(response_body, 400)
        elif  "total_inventory" not in request_body:
            response_body = {"details": "Request body must include total_inventory."}
            return make_response(response_body, 400)
        
        new_video = Video(title = request_body["title"], 
                        release_date = request_body["release_date"],
                        total_inventory = request_body["total_inventory"])
        #! add it to db and commit it 
        db.session.add(new_video)
        db.session.commit()

        response_body = {"title": new_video.title,
                        "id": new_video.id,
                        "release_date": new_video.release_date,
                        "total_inventory": new_video.total_inventory}

        return make_response(jsonify(response_body),201)
    except Exception:
        abort(400)


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
        # count_id = Video.query.filter_by(release_date=video.release_date).count()
        # response_body = {'answer': count_id}
        return make_response(jsonify(response_body),200)
    except:
        abort(400)


''' PUT'''

@video_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id): 
    video = get_video_by_id(video_id)

    try:
        request_body = request.get_json()
        if not request_body or "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            abort(400)
        if "title" in request_body:
            video.title = request_body["title"]
        if "release_date" in request_body:
            video.release_date = request_body["release_date"]
        if "total_inventory" in request_body:
            video.total_inventory = request_body["total_inventory"]
        # commit uppdates
        db.session.commit()
        response_body = video.to_json()
        return make_response(response_body, 200)
    except:
        abort(400)


'''DELETE'''
@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id): 
    video = get_video_by_id(video_id)
    try:
        # delete entity and commit it
        
        db.session.delete(video)
        db.session.commit()

        response_body ={"id": video.id}

        return make_response(response_body), 200

    except Exception:
        abort(422)



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
