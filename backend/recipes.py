from flask import (
    Blueprint, flash, g, redirect,  render_template, request, session, url_for,
)

from backend.db import get_db, get_json

bp = Blueprint('recipes', __name__, url_prefix='/recipes')


@bp.route('/', methods=["GET"])
def list_recipes():
    db = get_db()
    
    query = """
            SELECT title, author_notes, username FROM recipe r
            INNER JOIN user u
            ON r.author_id = u.id
            """
    recipes = db.execute(query)
    return render_template('recipes/recipes.html', recipes=recipes)

@bp.route('/user/<int:user_id>')
def get_user_recipes(user_id):
    db = get_db()
    query = """
            SELECT * 
            FROM recipe r 
            WHERE r.author_id = ? 
            """
    query_args = (user_id,)
    res = db.execute(query, query_args).fetchall()
     
    if res is None:
        return "no recipes found for specified user :("
    return get_json(res)    

@bp.route('/<int:recipe_id>')
def get_recipe(recipe_id):
    db = get_db()
    query = """
            SELECT * 
            FROM recipe r 
            WHERE r.id = ? 
            """
    query_args = (recipe_id,)
    res = db.execute(query, query_args).fetchone()

    if res is None:
        return "oops! recipe not found :("
    return get_json(res)
    #return jsonify(dict(res))

@bp.route('/create', methods=(['GET', 'POST']))
def create_recipe():
    if request.method == 'POST':
        print(request.form.keys)
        title = request.form.get('title', "default title")
        notes = request.form.get('notes', "default notes")
        
        ing = request.form.get('ing1', "default ing")
        step = request.form.get('step1', "default step")
        ingno = request.form.get('ingno', "default ingno")
        stepno = request.form.get('stepno', "default stepno")
        print(ingno, ing, stepno, step)

        db = get_db()
        c = db.cursor()
        err = None

        if not (notes and title):
            error = "cannot create a recipe without fields"
        
        if err is None:
            query = """
                    INSERT INTO recipe 
                    (author_id, title, author_notes)
                    VALUES (?, ?, ?)
                    """
            query_args = (g.user['id'], title, notes)
            c.execute(query, query_args)
            recipe_id = c.lastrowid
            ins_ingredient(c, recipe_id, ingno, 5, ing) 

            db.commit()
            return redirect(url_for('recipes.list_recipes'))
        else:
            print(err)
    return render_template('recipes/create.html')

# changes are not committed
def ins_ingredient(db, recipe_id, ing_no, value, item):
    query = """
            INSERT INTO ingredient
            (recipe_id, ingredient_no, measurement, item)
            VALUES (?, ?, ?, ?)
            """
    query_args = (recipe_id, ing_no, value, item,)
    db.execute(query, query_args)

def create_step():
    pass
