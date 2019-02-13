from flask import Blueprint

bp_error = Blueprint('error', __name__)

from . import errors
