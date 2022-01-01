from eTracker import db
from flask_security import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Document, UserMixin):
    user_id         = db.IntField(unique=True)  
    email           = db.StringField(max_length=255, required=True, unique=True)
    password        = db.StringField()
    first_name      = db.StringField(max_length=255, required=True)
    last_name       = db.StringField(max_length=255, required=True)
    created_at      = db.DateTimeField(default=datetime.now, required=True)
    authenticated   = db.BooleanField(default=False)

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


class LinkStatus(db.Document):
    link_id = db.SequenceField()
    sender = db.ReferenceField(User)
    receiver = db.StringField(max_length=255, required=True)
    subject = db.StringField(max_length=255, required=True)
    tags = db.ListField(default=[])
    status = db.DictField()