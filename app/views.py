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
    hello = String(name=String(default_value="stranger"))
    goodbye = String()

    def resolve_vote(root, info, name, num_of_vote):
        return


schema = Schema(query=Query)

view_func = GraphQLView.as_view("graphql", schema=schema)

app.add_url_rule("/api", view_func=view_func)
