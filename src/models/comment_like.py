from src.database import db
import datetime


class CommentLike(db.Model):
    __tablename__ = "comment_likes"
    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = db.relationship("User", back_populates="comment_likes")
    comment = db.relationship("Comment", back_populates="comment_likes")

    __table_args__ = (
        db.UniqueConstraint('user_id', 'comment_id', name='unique_user_id_comment_id_like'),)

    def to_dict(self):
        return {
            "like_id": self.like_id,
            "comment_id": self.comment_id,
            "user_id": self.user_id,
            "created_at": self.created_at,
        }
