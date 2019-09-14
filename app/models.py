from app import db


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
