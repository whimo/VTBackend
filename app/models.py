from app import db


discussion_members = db.Table('discussion_members',
                              db.Column('discussion_id', db.Integer,
                                        db.ForeignKey('discussion.id'), nullable=False),
                              db.Column('user_id', db.Integer,
                                        db.ForeignKey('user.id'), nullable=False),
                              db.PrimaryKeyConstraint('discussion_id', 'user_id'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email =    db.Column(db.String(60), nullable=False, index=True, unique=True)
    password = db.Column(db.String(60), nullable=False)

    name =      db.Column(db.Text)
    last_name = db.Column(db.Text)

    vote_weight = db.Column(db.SmallInteger, default=1)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.id


class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    description = db.Column(db.Text, nullable=False)
    deadline =    db.Column(db.DateTime)

    members = db.relationship('User', backref='discussions', secondary=discussion_members)
