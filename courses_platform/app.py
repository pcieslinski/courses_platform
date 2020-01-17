from courses_platform.service import create_app
from courses_platform.service.config import DevConfig


app = create_app(config_object=DevConfig)
