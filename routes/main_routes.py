from os import path
from flask import Blueprint, send_from_directory, jsonify
from controllers import main_controllers

main_bp = Blueprint("main", __name__)
FRONTEND_FOLDER = path.join(path.dirname(path.dirname(__file__)), "frontend")

@main_bp.route("/", methods=["GET"])
def index():
    return main_controllers.root()

@main_bp.route("/api/photos", methods=["GET"])
def photos_route():
    raw_photos = main_controllers.get_photos()
    json_photos = [{
        "name": p.get_name(),
        "size": p.get_size(),
        "date": p.get_date().isoformat()
    } for p in raw_photos]
    
    return jsonify(json_photos)