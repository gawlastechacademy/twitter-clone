from src.database import db


class Role(db.Model):
    __tablename__ = "roles"
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.Text, unique=True, nullable=False)
    users = db.relationship("User", back_populates="roles")

    def to_dict(self):
        return
        {"role_id": self.role_id,
         "role_name": self.role_name
         }
