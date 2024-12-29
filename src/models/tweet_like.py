from src.database import db
import datetime


class TweetLike(db.Model):
    __tablename__ = "tweet_likes"
    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.tweet_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = db.relationship("User", back_populates="tweet_likes")
    tweet = db.relationship("Tweet", back_populates="tweet_likes")

    __table_args__ = (
        db.UniqueConstraint('user_id', 'tweet_id', name='unique_user_id_tweet_id_like'),)

    def to_dict(self):
        return {
            "like_id": self.like_id,
            "tweet_id": self.tweet_id,
            "user_id": self.user_id,
            "created_at": self.created_at,
        }
