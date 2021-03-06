from app import db
from sqlalchemy.orm import synonym
from werkzeug import check_password_hash, generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    # password = db.Column(db.Text)
    _password = db.Column('password', db.String(100))
    active = db.Column(db.Boolean, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    topics = db.relationship('Topic', backref='owner', lazy='dynamic')
    entries = db.relationship('Entry', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def get_id(self):
        return self.id

    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)

    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)

    def check_password(self, password):
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, query, email, password):
        user = query(cls).filter(cls.email == email).first()
        if user is None:
            return None, False
        return user, user.check_password(password)

    def __repr__(self):
        return '<User id={id} username={username!r}>'.format(id=self.id, username=self.username)


members = db.Table('members',
                   db.Column('topic_id', db.Text, db.ForeignKey('topic.id')),
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                   )


class Topic(db.Model):
    id = db.Column(db.Text, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    is_public = db.Column(db.Boolean)
    entries = db.relationship('Entry', backref='topic', lazy='dynamic')
    members = db.relationship('User', secondary=members,
                              backref=db.backref('my_entries', lazy='dynamic'))

    def __repr__(self):
        return '<Topic id={id} title={title!r}>'.format(id=self.id, title=self.title)


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Text, db.ForeignKey('topic.id'))
    user_id = db.Column(db.Text, db.ForeignKey('user.id'))
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    # Bug, Enhance, Idea..
    category = db.Column(db.Text)
    # New, Vote, Pending, Done, Close
    status = db.Column(db.Text, default='new')
    points = db.relationship('Point', backref='entry', lazy='dynamic')
    comments = db.relationship('Comment', backref='entry', lazy='dynamic')

    def __repr__(self):
        return '<Entry id={id} title={title!r}>'.format(id=self.id, title=self.title)


class Point(db.Model):
    __tablename__ = 'point'
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), primary_key=True)
    user_id = db.Column(db.Text, db.ForeignKey('user.id'), primary_key=True)
    date = db.Column(db.Date, primary_key=True)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))
    user_id = db.Column(db.Text, db.ForeignKey('user.id'))
    text = db.Column(db.Text)
    time = db.Column(db.DateTime)


class Reset(db.Model):
    key = db.Column(db.Text, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
