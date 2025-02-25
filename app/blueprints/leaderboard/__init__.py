from flask import Blueprint

leaderboard_bp = Blueprint('Leaderboard', __name__)

from . import routes