from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from wtforms.validators import Email

bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<username={u.username} password={u.password} email={u.email} first_name={u.first_name} last_name={u.last_name}>"

    username = db.Column(db.String(20), primary_key=True, info={'label': 'Username'})

    password = db.Column(db.String, nullable=False, info={'label': 'Password'})

    email = db.Column(db.String(50), nullable=False, unique=True, info={'label': 'Email', 'validators': Email()})

    first_name = db.Column(db.String(30), nullable=False, info={'label': 'First Name'})

    last_name = db.Column(db.String(30), nullable=False, info={'label': 'Last Name'})

    feedback = db.relationship('Feedback', backref='user', cascade='all, delete')

    @classmethod
    def register(cls, username, pwd, email, fname, lname):
        """Register user with hashed password and return user"""

        hashed = bcrypt.generate_password_hash(pwd)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=fname, last_name=lname)

    @classmethod
    def authenticate(cls, username, pwd):
        """Login user with hashed password"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False


class Feedback(db.Model):
    """Feedback Model"""

    __tablename__ = 'feedback'

    def __repr__(self):
        f = self
        return f"<id={f.id} title={f.title} content={f.content} username={f.username}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    username = db.Column(db.String(50), db.ForeignKey('users.username'), nullable=False)