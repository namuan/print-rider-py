from flask import Blueprint

prints_blueprint = Blueprint('prints', __name__, template_folder='templates')

from . import routes
