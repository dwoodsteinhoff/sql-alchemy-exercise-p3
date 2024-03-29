"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User Table"""

    __tablename__='users'

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement= True)
    
    first_name = db.Column(db.String(25),
                           nullable = False
                           )
    
    last_name = db.Column(db.String(50),
                         nullable = False
                         )
    
    image_url = db.Column(db.String(),
                          default = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'
                        )

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name} {self.image_url}>"

class Post(db.Model):
    """Post Table"""

    __tablename__='posts'

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement= True)
    
    title = db.Column(db.String(25),
                      nullable = False)
    
    content = db.Column(db.Text,
                        nullable = False)

    created_at = db.Column(db.DateTime,
                            nullable = False,
                            default= datetime.datetime.now)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable = False)
    
    user = db.relationship('User', backref = 'posts')

    post_tag = db.relationship('PostTag', backref = 'post')

    tags = db.relationship('Tag',
                           secondary = "posts_tags",
                           backref = "posts")

    def __repr__(self):
        return f"<Post {self.id} {self.title} {self.content} {self.created_at}>" 
    
class Tag(db.Model):
    """Tag Table"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement= True)
    
    name = db.Column(db.Text,
                     nullable = False,
                     unique = True)
    
    post_tag = db.relationship('PostTag', backref = 'tag')
    
class PostTag(db.Model):
    """ PostTag Table"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key = True)
    
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key = True)