import os

from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix

from printrider import create_app
from printrider.config import setup_config
from printrider.utils import log

is_offline = os.environ.get("AWS_SAM_LOCAL", False)

if is_offline:
    log("Offline detected. Loading local.env")
    load_dotenv("local.env", verbose=True)
else:
    log("Running on AWS Lambda. Loading prod.env")
    load_dotenv("prod.env", verbose=True)

app_config = setup_config(is_offline)
log("Loaded configuration: {}".format(app_config.DYNAMO_URL))

app = create_app(app_config)
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run()
