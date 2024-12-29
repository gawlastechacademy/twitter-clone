from src.database import db
import datetime


class Tweet(db.Model):
    __tablename__ = "tweets"
    tweet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    tweet_active = db.Column(db.Boolean, default=True)

    users = db.relationship("User", back_populates="tweets")
    comments = db.relationship("Comment", back_populates="tweet")
    tweet_likes = db.relationship("TweetLike", back_populates="tweet")

    def to_dict(self):
        return {
            "tweet_id": self.tweet_id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at,
            " tweet_active": self. tweet_active,
        }

    def is_active(self):
        return self.tweet_active == 1