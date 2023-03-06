from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# ---- many to many ----
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy.schema import Column, ForeignKey, Table
# from sqlalchemy.types import Integer, String
# ---- many to many ----


import os
environment = os.getenv("FLASK_ENV")
SCHEMA = os.environ.get('SCHEMA')

user_conversations=db.Table(
    "user_conversations",
    db.Model.metadata,
    db.Column('users', db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), primary_key=True),
    db.Column('conversations', db.Integer, db.ForeignKey(add_prefix_for_prod('conversations.id')), primary_key=True)
)

if environment == "production":
    user_conversations.schema = SCHEMA

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40),nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    profile_photo=db.Column(db.String(500))
    title=db.Column(db.String(100))

    posts = db.relationship("Post", back_populates="user")
    comments = db.relationship("Comment", back_populates="user")
    messages_users = db.relationship("Message", back_populates="user")

    #user to conversation: many to many

    conversations=db.relationship(
        "Conversation",
        secondary=user_conversations,
        back_populates="users",
        cascade="all, delete"
    )

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'last_name': self.last_name,
            'first_name': self.first_name,
            "profile_photo":self.profile_photo,
            "title":self.title
        }
