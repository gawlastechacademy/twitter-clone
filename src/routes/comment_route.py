from flask import Blueprint, request
import src.services.comment_service as comment_service
from flask_jwt_extended import jwt_required

comment_bp = Blueprint("comment", __name__)


# all
@comment_bp.route("/tweets/<tweet_id>/comments/", methods=["GET"])
@jwt_required()
def get_tweet_comments(tweet_id):
    return comment_service.get_tweet_comments(tweet_id)


@comment_bp.route("/comments/<comment_id>/", methods=["GET"])
@jwt_required()
def get_single_comment(comment_id):
    return comment_service.get_single_comment(comment_id)


@comment_bp.route("/tweets/<tweet_id>/comments/", methods=["POST"])
@jwt_required()
def add_tweet_comments(tweet_id):
    post_request = request.json
    return comment_service.add_tweet_comments(post_request, tweet_id)


# if you user or admin
@comment_bp.route("/comments/<comment_id>/", methods=["DELETE"])
@jwt_required()
def delete_single_comment(comment_id):
    return comment_service.delete_single_comment(comment_id)
