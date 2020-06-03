from flask import (
  Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from backend.auth import login_required
from backend.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
  db = get_db()
  users = db.execute(
    'SELECT * FROM user'
  ).fetchall()

  return render_template('index.html', users=users)