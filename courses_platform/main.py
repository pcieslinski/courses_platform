from flask.helpers import get_debug_flag

from app.service import create_app
from app.service.config import DevConfig, ProdConfig


CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(config_object=CONFIG)


if __name__ == '__main__':
    app.run()
