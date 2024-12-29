from src.database import db
import datetime


class Comment(db.Model):
    __tablename__ = "comments"
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.tweet_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    comment_active = db.Column(db.Boolean, default=True)


    user = db.relationship("User", back_populates="comments")
    tweet = db.relationship("Tweet", back_populates="comments")
    comment_likes = db.relationship("CommentLike", back_populates="comment")


    def to_dict(self):
        return {
            "comment_id": self.comment_id,
            "tweet_id": self.tweet_id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at,
            "comment_active": self.comment_active,
        }

    def is_active(self):
        return self.comment_active == 1