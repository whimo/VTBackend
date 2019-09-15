from app import app, models, db, lm, bcrypt
from flask import g
from datetime import datetime
from flask_login import login_user, current_user
from graphene import ObjectType, Mutation, String, Schema, DateTime
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
    discussions = graphene.List(Discussion, id=graphene.Argument(type=graphene.Int, required=False))
    sections =    graphene.List(Section)
    votes =       graphene.List(Vote)
    messages =    graphene.List(Message)

    def resolve_users(self, info):
        query = User.get_query(info)
        return query.all()

    def resolve_discussions(self, info, id=None):
        query = Discussion.get_query(info)
        if id:
            query = query.filter(models.Discussion.id == id)
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



class NewUserMutation(Mutation):
    class Arguments:
        email =     graphene.String(required=True)
        password =  graphene.String(required=True)
        name =      graphene.String()
        last_name = graphene.String()

    user = graphene.Field(User)

    def mutate(root, info, email, password, name=None, last_name=None):
        new_user = models.User(email=email,
                               password=bcrypt.generate_password_hash(password).decode('utf-8'),
                               name=name,
                               last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        return NewUserMutation(user=new_user)

class NewDiscussionMutation(Mutation):
    class Arguments:
        name =     graphene.String(required=True)
        description =  graphene.String(required=True)
        deadline = graphene.DateTime()

    discussion = graphene.Field(Discussion)

    def mutate(root, info, name, description, deadline):
        new_discussion = models.Discussion(name=name, description=description, deadline=deadline)
        db.session.add(new_discussion)
        db.session.commit()
        return NewDiscussionMutation(discussion=new_discussion)

class NewVoteMutation(Mutation):
    class Arguments:
        user_id =     graphene.String(required=True)
        section_id =  graphene.String(required=True)
        
    vote = graphene.Field(Vote)

    def mutate(root, info, user_id, section_id):
        print(g.user.id)
        new_vote = models.Vote(user_id=user_id, section_id=section_id)
        db.session.add(new_vote)
        db.session.commit()
        return NewVoteMutation(vote=new_vote)

class NewSectionMutation(Mutation):
    class Arguments:
        discussion_id =     graphene.String(required=True)
        description =  graphene.String(required=True)
        
    section = graphene.Field(Section)

    def mutate(root, info, discussion_id, description):
        new_section = models.Section(discussion_id=discussion_id, description=description)
        db.session.add(new_section)
        db.session.commit()
        return NewSectionMutation(section=new_section)

class NewLoginMutation(Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(User)
    
    def mutate(root, info, email, password):
        user_ = models.User.query.filter_by(email=email).first()

        if user_ and bcrypt.check_password_hash(user_.password, password):
            login_user(user_)

        
        return NewLoginMutation(user=user_)

class Mutations(ObjectType):
    register = NewUserMutation.Field()
    discussion = NewDiscussionMutation.Field()
    section = NewSectionMutation.Field()
    vote = NewVoteMutation.Field()
    login = NewLoginMutation.Field()


schema = Schema(query=Query, mutation=Mutations, auto_camelcase=False)

view_func = GraphQLView.as_view("graphql", schema=schema, graphiql=True)

app.add_url_rule("/api", view_func=view_func)
