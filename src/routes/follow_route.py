from flask import Blueprint
import src.services.comment_service as comment_service
from flask_jwt_extended import jwt_required

from src.services import follow_service

follow_bp = Blueprint("follow", __name__)


#
# /users/<user_id>/follow
# /users/<user_id>/followers
# /users/<user_id>/following

# for user or admin if you follow you can;t
@follow_bp.route("/users/<user_id>/follow/", methods=["POST"])
@jwt_required()
def follow_user(user_id):
    return follow_service.follow_user(user_id)


@follow_bp.route("/users/<user_id>/follow/", methods=["DELETE"])
@jwt_required()
def delete_follow_user(user_id):
    return follow_service.delete_follow_user(user_id)


# who follow user
@follow_bp.route("/users/<user_id>/followers/", methods=["GET"])
@jwt_required()
def user_followers(user_id):
    return follow_service.user_followers(user_id)


# who user follow
@follow_bp.route("/users/<user_id>/following/", methods=["GET"])
@jwt_required()
def user_following(user_id):
    return follow_service.user_following(user_id)
