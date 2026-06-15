from flask import Flask, send_file, request, abort
from urllib.parse import urlparse
from routes.main_routes import main_bp
import os
from utils.utils import read_config

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

def create_app():
    
    app = Flask(__name__)
    config_data = read_config(CONFIG_PATH)
    app.config.update(config_data)
    
    configured_domain = app.config.get("app_data", {}).get("domain", "")
    expected_host = urlparse(configured_domain).netloc
    
    @app.before_request
    def restrict_domain():
        allowed_hosts = [expected_host, "localhost", "127.0.0.1"]
        incoming_host = request.host
        
        if incoming_host not in allowed_hosts:
            abort(403, description="Access denied: Invalid host")
            
    app.register_blueprint(main_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    port_number = int(app.config.get("app_data").get("port"))
    
    app.run(host="127.0.0.1", port=port_number)