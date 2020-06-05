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
  )

  # get random recipe from database
  random_query = """
                 SELECT *
                 FROM recipe
                 WHERE id IN
                 (SELECT id 
                    FROM recipe
                    ORDER BY RANDOM()
                    LIMIT 1)
                 """
  recipe = db.execute(random_query).fetchone()
  if recipe is None:
     print('uh oh')
  return render_template('index.html', users=users, recipe=dict(recipe))
