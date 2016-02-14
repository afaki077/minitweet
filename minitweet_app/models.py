# ``# pragma: no cover`` is to exclude lines from coverage test
from . import db, bcrypt  # pragma: no cover


class Post(db.Model):

    __tablename__ = "posts"  # pragma: no cover

    id = db.Column(db.Integer, primary_key=True)  # pragma: no cover
    title = db.Column(db.String, nullable=False)  # pragma: no cover
    body = db.Column(db.String, nullable=False)   # pragma: no cover
    # ForeignKey
    author_id = db.Column(db.Integer, db.ForeignKey('users.id')) \
        # pragma: no cover

    def __init__(self, title='', body='', author_id=1):
        self.title = title
        self.body = body
        self.author_id = author_id

    def __repr__(self):
        # for debugging
        return "<Post {}>".format(self.title)


followers = db.Table("followers",
                     db.Column("follower_id",
                               db.Integer,
                               db.ForeignKey("users.id")
                               ),
                     db.Column("followed_id",
                               db.Integer,
                               db.ForeignKey("users.id")
                               )
                     )

likes = db.Table("likes",
                 db.Column("user_id",
                           db.Integer,
                           db.ForeignKey("users.id")
                           ),
                 db.Column("post_id",
                           db.Integer,
                           db.ForeignKey("posts.id")
                           ),
                 )


class User(db.Model):

    __tablename__ = "users"  # pragma: no cover

    id = db.Column(db.Integer, primary_key=True)  # pragma: no cover
    name = db.Column(db.String, nullable=False)  # pragma: no cover
    email = db.Column(db.String, nullable=False)  # pragma: no cover
    password = db.Column(db.String, nullable=False)  # pragma: no cover
    bio = db.Column(db.String)  # pragma: no cover
    website = db.Column(db.String)  # pragma: no cover
    # one to many relationship
    posts = db.relationship("Post", backref="author", lazy="dynamic") \
        # pragma: no cover
    confirmed = db.Column(db.Boolean, nullable=False, default=False) \
        # pragma: no cover
    following = db.relationship('User',  # pragma: no cover
                                secondary=followers,
                                primaryjoin=(followers.c.follower_id == id),
                                secondaryjoin=(followers.c.followed_id == id),
                                backref=db.backref('followers',
                                                   lazy='dynamic'),
                                lazy='dynamic'
                                )

    liked_posts = db.relationship('Post',  # pragma: no cover
                                  secondary=likes,
                                  primaryjoin=(likes.c.user_id == id),
                                  secondaryjoin=(likes.c.post_id == Post.id),
                                  backref=db.backref('likers',
                                                     lazy='dynamic'),
                                  lazy='dynamic'
                                  )

    def __init__(self, name='', email='', password='',
                            bio='', website="", confirmed=False):
        self.name = name
        self.email = email
        # generate one way hash for password
        self.password = bcrypt.generate_password_hash(password)
        self.bio = bio
        self.website = website
        self.confirmed = confirmed

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)
            return self

    def is_following(self, user):
        return self.following.filter(followers.c.followed_id == user.id) \
            .count() > 0

    def get_posts_from_followed_users(self):
        joined = Post.query.join(followers,
                                 (followers.c.followed_id == Post.author_id))
        filterd = joined.filter(followers.c.follower_id == self.id)
        orderd = filterd.order_by(Post.id.desc())
        return orderd

    def is_liking(self, post):
        return self.liked_posts.filter(likes.c.post_id == post.id).count() > 0

    def like(self, post):
        if not self.is_liking(post):
            self.liked_posts.append(post)
            return self

    def unlike(self, post):
        if self.is_liking(post):
            self.liked_posts.remove(post)
            return self

    # =========================================#
    #  Flask-Login extension required methods #
    # =========================================#

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        # for debugging
        return '<User {}>'.format(self.name)
