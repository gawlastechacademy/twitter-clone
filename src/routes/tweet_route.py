from flask import Blueprint, request
import src.services.tweet_service as tweet_service
from flask_jwt_extended import jwt_required

tweet_bp = Blueprint("tweet", __name__)


# return tweet from user whose you follow
@tweet_bp.route("/feed/", methods=["GET"])
@jwt_required()
def list_todos():
    return tweet_service.get_follow_tweets()


# only for admin
@tweet_bp.route("/tweets/", methods=["GET"])
@jwt_required()
def list_tweets():
    return tweet_service.get_all_tweets()


@tweet_bp.route("/tweets/", methods=["POST"])
@jwt_required()
def add_tweet():
    post_request = request.json
    content = post_request["content"]
    return tweet_service.add_single_tweets(content)


# all
@tweet_bp.route("/tweets/<tweet_id>", methods=["GET"])
@jwt_required()
def get_single_tweet(tweet_id):
    return tweet_service.get_single_tweet(tweet_id)


@tweet_bp.route("/tweets/<tweet_id>", methods=["PUT"])
@jwt_required()
def update_single_task(tweet_id):
    post_request = request.json
    return tweet_service.update_single_tweet(post_request, tweet_id)


# all
@tweet_bp.route("/users/<user_id>/tweets/", methods=["GET"])
@jwt_required()
def tweets_user(user_id):
    return tweet_service.get_user_tweets(user_id)

# get all tweet comments if you follow if yoy are user, if you admin

@tweet_bp.route("/tweets/<tweet_id>", methods=["DELETE"])
@jwt_required()
def delete_single_task(tweet_id):
    return tweet_service.delete_single_tweet(tweet_id)