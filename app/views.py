from app import app, models, db, lm, bcrypt
from flask import g
from flask_login import current_user
from graphene import ObjectType, String, Schema
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
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


class User(SQLAlchemyObjectType):
    class Meta:
        model = models.User


class Discussion(SQLAlchemyObjectType):
    class Meta:
        model = models.Discussion


class Section(SQLAlchemyObjectType):
    class Meta:
        model = models.Section


class Vote(SQLAlchemyObjectType):
    class Meta:
        model = models.Vote


class Message(SQLAlchemyObjectType):
    class Meta:
        model = models.Message


class Query(ObjectType):
    users =       graphene.List(User)
    discussions = graphene.List(Discussion)
    sections =    graphene.List(Section)
    votes =       graphene.List(Vote)
    messages =    graphene.List(Message)

    def resolve_users(self, info):
        query = User.get_query(info)
        return query.all()

    def resolve_discussions(self, info):
        query = Discussion.get_query(info)
        return query.all()

    def resolve_sections(self, info):
        query = Section.get_query(info)
        return query.all()

    def resolve_votes(self, info):
        query = Vote.get_query(info)
        return query.all()

    def resolve_messages(self, info):
        query = Message.get_query(info)
        return query.all()


schema = Schema(query=Query, auto_camelcase=False)

view_func = GraphQLView.as_view("graphql", schema=schema, graphiql=True)

app.add_url_rule("/api", view_func=view_func)
