"""Seed file to make sample db"""

from models import db, User, Feedback
from app import app

# Create all tables

db.drop_all()
db.create_all()

CONTENT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Est velit egestas dui id ornare. Eu facilisis sed odio morbi."

users = [
    User.register("dogluvr", "password", "email@email.com" "Joe", "Sutherland"),

    User.register("kewldood", "password", "sokewl@aol.com", "Chad", "Kewlwwwl"),

    User.register("gigithecat", "password" "kittens@yahoo.com", "Sara", "Gordon")

]

db.session.add_all(users)
db.session.commit()

feedback = Feedback(title='SECOND', content='MORE CONTENT', username='TEST')