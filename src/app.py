from flask import Flask
from src.database import db
from flask_jwt_extended import JWTManager

from src.routes.tweet_route import tweet_bp
from src.routes.user_route import user_bp
from src.routes.comment_route import comment_bp
from src.routes.like_route import like_bp
from src.routes.follow_route import follow_bp


app = Flask(__name__)

app.register_blueprint(tweet_bp)
app.register_blueprint(user_bp)
app.register_blueprint(comment_bp)
app.register_blueprint(like_bp)
app.register_blueprint(follow_bp)

app.config.from_object("config.Config")
db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    from src.models.user import User
    from src.models.role import Role
    from src.models.tweet import Tweet
    from src.models.comment import Comment
    from src.models.tweet_like import TweetLike
    from src.models.comment_like import CommentLike
    from src.models.follow import Follow
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
