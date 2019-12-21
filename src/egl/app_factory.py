import logging

from flask import Blueprint, Flask, jsonify, Response, abort, g
from flask_login import LoginManager, login_user, current_user
from flask_marshmallow import Marshmallow
from requests import RequestException
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.exceptions import Unauthorized

from egl import config
from egl.api.v1 import api
from egl.api.v1.authentication import ns as auth_namespace
from egl.api.v1.services import SeedDataService
from egl.api.v1.users import ns as users_namespace
from egl.app_json_encoder import monkey_patch_json_encoder
from egl.app_session import AppSessionInterface
from egl.db.models import User
from egl.db.sessions import db

logger = logging.getLogger(__name__)
logger.setLevel('INFO')


def app_factory():
    monkey_patch_json_encoder()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = config.get('FLASK_SESSION_SECRET_KEY')

    db.init_app(app)

    Marshmallow(app)

    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.url_map.strict_slashes = False

    blueprint = Blueprint('v1', __name__, url_prefix='/api/v1')
    api.init_app(blueprint)
    api.add_namespace(auth_namespace, '/authentication')
    api.add_namespace(users_namespace, '/users')

    app.register_blueprint(blueprint)
    app.session_interface = AppSessionInterface()

    login_manager = LoginManager()
    login_manager.init_app(app)

    seed_data_enabled = config.get('SEED_DATA_ENABLED')
    if seed_data_enabled:
        with app.app_context():
            seed_data = SeedDataService()
            seed_data.seed()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @login_manager.request_loader
    def load_user_from_request(request):
        header = request.headers.get('Authorization')
        if header is None:

            # review how to whitelist end points that we know won't ever require authn/authz
            # total hack, clean up with werkzeug or flask trimming, or our own method... this is super messy.
            whitelist = ['/api/v1', '/api/v1?', '/api/v1/?', '/api/v1/swagger.json']
            if request.full_path in whitelist:
                return

            raise Unauthorized()

        header_value = header.split()
        auth_type = header_value[0].lower()

        if auth_type == 'bearer':
            authenticate_bearer_token(header_value[1])

        elif auth_type == 'basic':
            creds = request.authorization
            if creds is not None:
                authenticate_basic(creds.username, creds.password)

        if current_user is None:
            raise Unauthorized()

        g.authenticated_from_header = True

    @app.after_request
    def after_request(response):
        if 'cache-control' not in response.headers:
            response.headers['cache-control'] = 'no-cache'
        return response

    @api.errorhandler
    def default_error_handler(e):
        """
        Provide a default error handler for RestPlus to leverage.
        """
        logger.exception(e)
        debug = config.get('FLASK_DEBUG')
        if not debug:
            message = 'An unhandled exception occurred.'
            return {'message': message}, 500

    @app.errorhandler(400)
    def bad_request_error(e):
        return jsonify(error=400, text=str(e)), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify(error=404, text=str(e)), 404

    @app.errorhandler(500)
    def server_error(e):
        logger.error(e)
        return jsonify(error=500, text=str(e)), 500

    @app.errorhandler(RequestException)
    def request_exception(e):
        logger.error(e)
        return jsonify(error=500, text=str(e)), 500

    return app


def authenticate_basic(username, password):
    user = db.session.query(User).filter(User.email == username).one_or_none()
    if user is None:
        raise Unauthorized()

    if user.check_password(password):
        login_user(user)
    else:
        abort_with_challenge()


def authenticate_bearer_token(token):
    raise Unauthorized()


def abort_with_challenge():
    headers = {'WWW-Authenticate': 'Basic realm="Authentication Required"'}
    abort(Response('Unauthorized, Authorization header required.', 401, headers))
