from os import path
from flask import Blueprint, send_from_directory, jsonify, request
from controllers import main_controllers

main_bp = Blueprint("main", __name__)
FRONTEND_FOLDER = path.join(path.dirname(path.dirname(__file__)), "frontend")

@main_bp.route("/", methods=["GET"])
def index():
    return main_controllers.root()

@main_bp.route("/api/photos", methods=["GET"])
def photos_route():
    number_of_loaded_photos = request.args.get("number", default=None, type=int)
    raw_photos = main_controllers.get_photos(number_of_images=number_of_loaded_photos)
    json_photos = [{
        "name": p.get_name(),
        "size": p.get_size(),
        "date": p.get_date().isoformat()
    } for p in raw_photos]
    
    return jsonify(json_photos)