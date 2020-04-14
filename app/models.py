from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_on = db.Column(db.DateTime, index=True, default=datetime.now)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)   


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class ScrapedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String)
    price = db.Column(db.String)
    rating = db.Column(db.String)
    photo = db.Column(db.String)
    total_reviews = db.Column(db.String)
    total_rating = db.Column(db.String)
    link = db.Column(db.String, )
    keyword = db.Column(db.String)
    website= db.Column(db.String)

    def __repr_(self):
        return self.id

    def dictionary(self):
        return dict(id = self.id,
                    date = self.created_on,
                    name = self.name,
                    price = self.price,
                    rating = self.rating,
                    photo = self.photo,
                    total_reviews = self.total_reviews,
                    total_rating = self.total_rating,
                    link = self.link,
                    website = self.website,
                    keyword = self.keyword)


