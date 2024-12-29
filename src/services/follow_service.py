from flask import jsonify

from src.database import db
from src.models.follow import Follow
from src.models.user import User
from src.services.user_service import get_current_user


def follow_user(user_id):
    followed = User.query.get(user_id)
    logged_user = get_current_user()
    previous_follow = Follow.query.filter(
        Follow.followed_user_id == followed.user_id and Follow.follower_user_id == logged_user.user_id).first()

    if followed is None:
        return jsonify({"description": f"user '{followed.user_id}' not found"}), 404

    if followed.is_active() is False:
        return jsonify({"description": f"user '{followed.user_id}' not found"}), 404

    if followed.user_id == logged_user.user_id:
        return jsonify({"description": "you can't follow yourself"}), 409

    if previous_follow is not None:
        return jsonify({"description": "you just follow this person"}), 409

    new_follow = Follow(
        follower_user_id=logged_user.user_id,
        followed_user_id=followed.user_id,
    )
    db.session.add(new_follow)
    db.session.commit()
    return jsonify(new_follow.to_dict()), 200


def delete_follow_user(user_id):
    followed = User.query.get(user_id)
    logged_user = get_current_user()
    previous_follow = Follow.query.filter(
        Follow.followed_user_id == followed.user_id and Follow.follower_user_id == logged_user.user_id).first()

    if followed is None:
        return jsonify({"description": f"user '{followed.user_id}' not found"}), 404

    if followed.is_active() is False:
        return jsonify({"description": f"user '{followed.user_id}' not found"}), 404

    if followed.user_id == logged_user.user_id:
        return jsonify({"description": "you can't follow yourself"}), 409

    if previous_follow is None:
        return jsonify({"description": "you don't follow this person"}), 409
    db.session.delete(previous_follow)
    db.session.commit()
    return jsonify({"description": f"User {logged_user.user_id} stop follow user {followed.user_id}"}), 200


def user_followers(user_id):
    followers = Follow.query.filter(Follow.followed_user_id == user_id).all()
    followers_to_dict = [follower.to_dict() for follower in followers]
    return jsonify(followers_to_dict), 200


def user_following(user_id):
    following = Follow.query.filter(Follow.follower_user_id == user_id).all()
    following_to_dict = [follow.to_dict() for follow in following]
    return jsonify(following_to_dict), 200
