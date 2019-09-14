from app import app, models, db, bcrypt


@app.route('/')
def index():
    return '<h1>hello fuckers</h1>'
