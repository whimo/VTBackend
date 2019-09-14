from app import app, models, db, bcrypt

from flask import Flask
from graphene import ObjectType, String, Schema
from flask_graphql import GraphQLView

class Query(ObjectType):
    hello = String(name=String(default_value="stranger"))
    goodbye = String()

    def resolve_vote(root, info, name, num_of_vote):
        return
    

schema = Schema(query=Query)

view_func = GraphQLView.as_view("graphql", schema=schema)

app.add_url_rule("/api", view_func=view_func)
