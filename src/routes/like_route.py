from flask import Blueprint
import src.services.like_service as like_service
from flask_jwt_extended import jwt_required

like_bp = Blueprint("like", __name__)


# all

@like_bp.route("/tweets/<tweet_id>/likes", methods=["GET"])
@jwt_required()
def get_tweet_likes(tweet_id):
    return like_service.get_tweet_likes(tweet_id)


# all
@like_bp.route("/comments/<comment_id>/likes", methods=["GET"])
@jwt_required()
def get_comment_likes(comment_id):
    return like_service.get_comment_likes(comment_id)


# all
@like_bp.route("/tweets/<tweet_id>/likes", methods=["POST"])
@jwt_required()
def add_tweet_like(tweet_id):
    return like_service.add_tweet_like(tweet_id)


@like_bp.route("/comments/<comment_id>/likes", methods=["POST"])
@jwt_required()
def add_comment_like(comment_id):
    return like_service.add_comment_like(comment_id)


# admin and user
@like_bp.route("/tweets/<tweet_id>/likes/<like_id>", methods=["DELETE"])
@jwt_required()
def delete_tweet_like(tweet_id, like_id):
    return like_service.delete_tweet_like(tweet_id, like_id)


# admin and user
@like_bp.route("/comments/<comment_id>/likes/<like_id>", methods=["DELETE"])
@jwt_required()
def delete_comment_like(comment_id, like_id):
    return like_service.delete_comment_like(comment_id, like_id)
