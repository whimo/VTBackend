from app import app, models, db, lm, bcrypt
from flask import g
from flask_login import current_user
from graphene import ObjectType, String, Schema, DateTime
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

    vote = String(user_id=String(), section_id=String())
    register = String(user_email=String(),user_password=String(),user_name=String(),user_lastname=String())
    login = String(user_email=String(), user_password=String())
    discussion = String(d_name = String(), d_description = String(), d_deadline = DateTime())
    take_disc_data = String(d_id = String())
    section = String(discussion_id1 = String(), description1=String())


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
    
    def resolve_vote(root, info, user_id, section_id):
        if str(g.user.id) == str(user_id):
            new_vote = models.Vote(user_id=user_id, section_id=section_id)
            db.session.add(new_vote)
            db.session.commit()
            return '{"status": "ok"}'
        else:
            return '{"status":"wrong"}'

    def resolve_register(root, info, user_email, user_password, user_name, user_lastname):
        new_password_hash = bcrypt.generate_password_hash(user_password)
        new_person = models.User(last_name=user_lastname, email=user_email, password=new_password_hash.decode('utf-8'), name=user_name)
        db.session.add(new_person)
        db.session.commit()
        return '{"status": "ok"}'
    
    def resolve_login(root, info, user_email, user_password):
        user = models.User.query.filter_by(email=user_email).first()
        if user and bcrypt.check_password_hash(user.password, user_password):
            login_user(user)
            return '{"status": "ok"}'
        else:
            return '{"status":"wrong"}'

    def resolve_discussion(root, info, d_name, d_description, d_deadline):
        new_discussion = models.Discussion(name=d_name, description=d_description, deadline = d_deadline)
        db.session.add(new_discussion)
        db.session.commit()
        return '{"status": "ok"}'

    def resolve_section(root, info, discussion_id1, description1):
        new_section = models.Section(discussion_id=discussion_id1, description=description1)
        db.session.add(new_section)
        db.session.commit()
        return '{"status": "ok"}'


schema = Schema(query=Query, auto_camelcase=False)

view_func = GraphQLView.as_view("graphql", schema=schema, graphiql=True)

app.add_url_rule("/api", view_func=view_func)
