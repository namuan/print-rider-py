from http import HTTPStatus

from flask import request, make_response, render_template, current_app

from printrider import db_config
from printrider.prints import prints_blueprint
from printrider.prints.service import save_document, find_document


@prints_blueprint.route('/prints', methods=["POST"])
def save_print():
    doc_json = request.get_json()
    doc_id = save_document(db_config, doc_json)
    resp = make_response('', HTTPStatus.CREATED)
    resp.headers['Location'] = current_app.config['DOMAIN_NAME'] + "/prints/" + doc_id
    return resp


@prints_blueprint.route("/prints/<print_id>", methods=["GET"])
def get_print(print_id):
    document_code = find_document(db_config, print_id)
    return render_template('print.html', code=document_code)


@prints_blueprint.errorhandler(ValueError)
def handle_bad_request(e):
    return render_template('error.html', error_msg=e)


@prints_blueprint.errorhandler(HTTPStatus.BAD_REQUEST)
@prints_blueprint.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def handle_all_errors(e):
    return render_template('error.html', error_msg=e.description)
