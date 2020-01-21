from app.service import create_app
from app.service.config import DevConfig


app = create_app(config_object=DevConfig)
