import enum
from datetime import datetime
from app import db
from app.user.entities import User


class EnumTopic(enum.Enum):
    News = 1
    Publication = 2
    Other = 3


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    text = db.Column(db.Text)
    image_file = db.Column(db.String(200), nullable=False, default='postdefault.jpg')
    created = db.Column(db.TIMESTAMP, default=datetime.now().replace(microsecond=0))
    type = db.Column(db.Enum(EnumTopic), default=EnumTopic.News)
    enabled = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    user = db.relationship(User)

    def __repr__(self):
        return f"Post(id={self.id}, title='{self.title}', type='{self.type}')"


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    posts = db.relationship('Posts', backref='category', lazy=True)


post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
                     )


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    posts = db.relationship('Posts', secondary=post_tags, backref='tags')
