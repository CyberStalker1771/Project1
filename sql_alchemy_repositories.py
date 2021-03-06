from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import update

from app import app

db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer(), primary_key=True, unique=True, autoincrement=True)

    created = db.Column(db.DateTime(), default=datetime.utcnow)

    title = db.Column(db.Text(), nullable=False)

    content = db.Column(db.Text(), nullable=False)

    comments = db.relationship('Comment', backref='post', lazy='dynamic')


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    username = db.Column(db.String(64), index=True, unique=True)

    email = db.Column(db.String(120), index=True, unique=True)

    password_hash = db.Column(db.String(128))


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer(), primary_key=True, unique=True, autoincrement=True)

    created = db.Column(db.DateTime(), default=datetime.utcnow)

    content = db.Column(db.Text(), nullable=False)

    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'))


db.create_all()
db.session.commit()


def get_post(post_id):
    return Post.query.get(post_id)


def get_all_posts():
    return Post.query.all()


def add_post(title, content):
    post = Post(title=title, content=content)

    db.session.add(post)

    db.session.commit()


def update_post(title, content, id):
    db.session.execute(update(Post)

                       .where(Post.id == id)

                       .values(title=title, content=content))

    db.session.commit()


def delete_post(id):
    Post.query.filter_by(id=id).delete()

    db.session.commit()


def add_user(name, email, password):
    pass


def add_comment(post_id, content):
    post = get_post(post_id)

    new_comment = Comment(post=post, content=content)

    db.session.add(new_comment)

    db.session.commit()


def get_comments(post_id):
    post = Post.query.get(post_id)

    comments = post.comments.all()

    return comments
