import os
import datetime
from models.PhotoObject import PhotoObject
from utils.utils import read_config
from flask import current_app

def get_photos() -> list:
    
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
    
    top_4_images = filtered_out_videos[:4]
        
    return top_4_images