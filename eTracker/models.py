from eTracker import db
from flask_security import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func



class User(db.Model, UserMixin):
    __tablename__   = 'user'
    user_id         = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    email           = db.Column(db.String(255), nullable=False)
    password        = db.Column(db.String(500))
    first_name      = db.Column(db.String(255), nullable=False)
    last_name       = db.Column(db.String(255), nullable=False)
    created_at      = db.Column(db.DateTime(timezone=True), server_default=func.now())
    authenticated   = db.Column(db.Boolean(), default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.user_id)


class LinkStatus(db.Model):
    __tablename__ = 'link_status'
    link_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.ForeignKey("user.user_id"))
    sender = db.relationship("User", backref="LinkStatus")

    receiver = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    tags = db.relationship('Tag', backref="LinkStatus")
    status = db.relationship('Status', backref="LinkStatus")

class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link_id = db.Column(db.ForeignKey("link_status.link_id"))
    name = db.Column(db.String(100), nullable=False)

class Status(db.Model):
    status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link_id = db.Column(db.ForeignKey("link_status.link_id"))
    timestamp_utc = db.Column(db.DateTime(timezone=True))
    ip = db.Column(db.String(50))
    os = db.Column(db.String(50))
    browser = db.Column(db.String(50))
    v = db.Column(db.String(50))
    lang = db.Column(db.String(50))
    st = db.Column(db.String(200))