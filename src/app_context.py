import os
from distutils.util import strtobool

from flask_marshmallow import Marshmallow
from flask_restx import Api

from common.extensions import PynamoDB

db = PynamoDB()
ma = Marshmallow()
api = Api() if strtobool(os.environ.get('SWAGGER_UI_ENABLED', '0')) \
    else Api(doc=False)
