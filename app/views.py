from app import app, models, db, lm, bcrypt
from flask import g
from flask_login import current_user
from graphene import ObjectType, String, Schema
from flask_graphql import GraphQLView


@app.before_request
def before_request():
    '''
    Set current request user before every request
    '''
    g.user = current_user


@lm.user_loader
def load_user(userid):
    '''
    Flask-Login user loader
    '''
    return models.User.query.get(int(userid))



class Query(ObjectType):
    vote = String(user_id=String(), section_id=String())
    goodbye = String()

    def resolve_vote(root, info, user_id, section_id):
        new_vote = models.Vote(user_id=user_id, section_id=section_id)
        db.session.add(new_vote)
        db.session.commit()
        return True


schema = Schema(query=Query, auto_camelcase=False)

view_func = GraphQLView.as_view("graphql", schema=schema)

app.add_url_rule("/api", view_func=view_func)
