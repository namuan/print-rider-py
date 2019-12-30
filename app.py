from werkzeug.middleware.proxy_fix import ProxyFix

from printrider import create_app
from printrider.config import setup_config
from printrider.utils import log

app_config = setup_config()
log("Loaded configuration: {}".format(app_config.DOMAIN_NAME))

app = create_app(app_config)
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run()
