from src.database import db
import datetime


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.Text, nullable=False)
    user_password = db.Column(db.Text, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    registration_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_active = db.Column(db.Boolean, default=True)

    roles = db.relationship("Role", back_populates="users")
    tweets = db.relationship("Tweet", back_populates="users")
    roles = db.relationship("Role", back_populates="users")
    tweets = db.relationship("Tweet", back_populates="users")
    followers = db.relationship("Follow", back_populates="followed", foreign_keys="[Follow.followed_user_id]")
    following = db.relationship("Follow", back_populates="follower", foreign_keys="[Follow.follower_user_id]")
    comments = db.relationship("Comment", back_populates="user")
    comment_likes = db.relationship("CommentLike", back_populates="user")
    tweet_likes = db.relationship("TweetLike", back_populates="user")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "registration_date": self.registration_date,
            "role_id": self.role_id,
            "user_active": self.user_active
        }

    def is_admin(self):
        return self.role_id == 1

    def is_active(self):
        return self.user_active == 1

