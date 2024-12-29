import datetime

from src.database import db


class Follow(db.Model):
    __tablename__ = "follows"
    follow_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    followed_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    follower = db.relationship("User", back_populates="following", foreign_keys=[follower_user_id])
    followed = db.relationship("User", back_populates="followers", foreign_keys=[followed_user_id])
    __table_args__ = (
        db.UniqueConstraint('follower_user_id', 'followed_user_id', name='unique_follower_followed'),)

    def to_dict(self):
        return {
            "follow_id": self.follow_id,
            "follower_user_id": self.follower_user_id,
            "followed_user_id": self.followed_user_id,
            "created_at": self.created_at,
        }


