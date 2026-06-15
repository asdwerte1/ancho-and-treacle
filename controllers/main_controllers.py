import os
import json
import datetime
from models.PhotoObject import PhotoObject
from flask import current_app, Response

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

def root() -> None:
    html_path = os.path.join(FRONTEND_DIR, "index.html")
    with open(html_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            config_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        config_data = {}
        
    show_tunnel_notice = config_data.get("show_tunnel_text", False)
    
    if show_tunnel_notice:
        notice_element = """
        <p class="ml-3">Look out for quick zoomies through the <span class="highlight-text bold">tunnel</span>, or if they are being quiet
        and hiding sudden rocking of the tunnel as one of them moves inside it.</p>
        """
    else:
        notice_element = ""
        
    rendered_content = html_content.replace("<!-- DYNAMIC_TUNNEL_NOTICE -->", notice_element)
    
    return Response(rendered_content, mimetype="text/html")
        

def get_photos(number_of_images = None) -> list:
    
    """_summary_
        Fetches the four most recent photos from storage area.
    Returns:
        list: list of PhotoObjects
    """
    
    file_path = current_app.config.get("photo_file_path")
    photo_objects = []
    
    with os.scandir(file_path) as f:
        for entry in f:
            if entry.is_file():
                
                filename = entry.name
                
                file_stats = entry.stat()
                fileSize = file_stats.st_size
                
                dateInt = int(file_stats.st_mtime)
                date = datetime.datetime.fromtimestamp(dateInt)
                
                file_object = PhotoObject(filename, fileSize, date)                

                photo_objects.append(file_object)
    
    filtered_out_videos = []   
    for file in photo_objects:
        file_extension = os.path.splitext(file.get_name())[1].lower()
        if file_extension in [".jpg", ".jpeg", ".png", ".gif"]:
            filtered_out_videos.append(file)

    filtered_out_videos.sort(key=lambda x: x.get_date(), reverse=True)
    
    if number_of_images is None:
        images = filtered_out_videos[:6]
    else:
        images = filtered_out_videos[number_of_images:number_of_images + 2]
        
    return images