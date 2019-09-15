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


@lm.request_loader
def load_user_from_request(request):
    print('hey')
    uid = request.headers.get('Authorization')
    if uid:
        user = models.User.query.filter_by(id=uid).first()
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None


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
    sections =    graphene.List(Section, id=graphene.Argument(type=graphene.Int, required=False))
    votes =       graphene.List(Vote)
    messages =    graphene.List(Message)
    discussion = String(d_name = String(), d_description = String(), d_deadline = DateTime())

    def resolve_users(self, info):
        query = User.get_query(info)
        return query.all()

    def resolve_discussions(self, info, id=None):
        query = Discussion.get_query(info)
        if id:
            query = query.filter(models.Discussion.id == id)
        return query.all()

    def resolve_sections(self, info, id=None):
        query = Section.get_query(info)
        if id:
            query = query.filter(models.Section.id == id)

        return query.all()

    def resolve_votes(self, info):
        query = Vote.get_query(info)
        return query.all()

    def resolve_messages(self, info):
        query = Message.get_query(info)
        return query.all()

    def resolve_discussion(root, info, d_name, d_description, d_deadline):
        new_discussion = models.Discussion(name=d_name, description=d_description, deadline = d_deadline, creation_date=datetime.utcnow())
        db.session.add(new_discussion)
        db.session.commit()
        return '{"status": "ok"}'


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
        name =         graphene.String(required=True)
        description =  graphene.String(required=True)
        deadline =     graphene.DateTime()

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
        voted_for =   graphene.Boolean(required=False)

    vote = graphene.Field(Vote)

    def mutate(root, info, user_id, section_id, voted_for=None):
        section = models.Section.query.get(section_id)
        if section and not section.discussion.closed:
            new_vote = models.Vote(user_id=user_id, section_id=section_id, voted_for=voted_for)
            db.session.add(new_vote)
            db.session.commit()
            section.get_voted_for_percentage()
        else:
            new_vote = None

        return NewVoteMutation(vote=new_vote)


class NewSectionMutation(Mutation):
    class Arguments:
        discussion_id = graphene.String(required=True)
        description =   graphene.String(required=True)

    section = graphene.Field(Section)

    def mutate(root, info, discussion_id, description):
        discussion = models.Discussion.query.get(discussion_id)
        if discussion and not discussion.closed:
            new_section = models.Section(discussion_id=discussion_id, description=description)
            db.session.add(new_section)
            db.session.commit()
        else:
            new_section = None

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
        else:
            user_ = None

        return NewLoginMutation(user=user_)


class NewMessageMutation(Mutation):
    class Arguments:
        content =    graphene.String(required=True)
        user_id =    graphene.String(required=True)
        section_id = graphene.String(required=True)

    message = graphene.Field(Message)

    def mutate(root, info, content, user_id, section_id):
        new_message = models.Message(content=content, user_id=user_id, section_id=section_id)
        db.session.add(new_message)
        db.session.commit()

        return NewMessageMutation(message=new_message)


class EditSectionMutation(Mutation):
    class Arguments:
        section_id =    graphene.String(required=True)
        description =   graphene.String(required=False)

    section = graphene.Field(Section)

    def mutate(root, info, section_id, description=None):
        section_ = models.Section.query.get(section_id)
        if section_:
            section_.description = description or section_.description
            db.session.commit()

        return EditSectionMutation(section=section_)


class CloseDiscussionMutation(Mutation):
    class Arguments:
        discussion_id = graphene.String(required=True)

    discussion = graphene.Field(Discussion)

    def mutate(root, info, discussion_id):
        discussion_ = models.Discussion.query.get(discussion_id)
        if discussion_:
            discussion_.closed = True
            db.session.commit()

        return CloseDiscussionMutation(discussion=discussion_)


class Mutations(ObjectType):
    register = NewUserMutation.Field()
    discussion = NewDiscussionMutation.Field()
    section = NewSectionMutation.Field()
    vote = NewVoteMutation.Field()
    login = NewLoginMutation.Field()
    message = NewMessageMutation.Field()
    section_edit = EditSectionMutation.Field()
    close_discussion = CloseDiscussionMutation.Field()


schema = Schema(query=Query, mutation=Mutations, auto_camelcase=False)

view_func = GraphQLView.as_view("graphql", schema=schema, graphiql=True)

app.add_url_rule("/api", view_func=view_func)
