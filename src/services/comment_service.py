from flask import jsonify

from src.database import db
from src.models.comment import Comment
from src.models.tweet import Tweet
from src.services.user_service import get_current_user



def get_tweet_comments(tweet_id):
    tweet = Tweet.query.get(tweet_id)
    if tweet is None:
        return jsonify({"description": f"task '{tweet_id}' not found"}), 404
    if tweet.is_active() is False:
        return jsonify({"description": f"task '{tweet_id}' not found"}), 404

    comments = Comment.query.filter(Comment.tweet_id == tweet_id and Comment.comment_active == True).all()

    comments_to_dict = [comment.to_dict() for comment in comments]
    return jsonify(comments_to_dict), 200


def get_single_comment(comment_id):
    comment = Comment.query.get(comment_id)
    tweet = Tweet.query.get(comment.tweet_id)
    if comment is None:
        return jsonify({"description": f"comment '{comment_id}' not found"}), 404
    if tweet.is_active() is False:
        return jsonify({"description": f"tweet '{comment_id}' not found"}), 404
    if comment.is_active() is False:
        return jsonify({"description": f"comment '{comment_id}' not found"}), 404

    return jsonify(comment.to_dict()), 200


def add_tweet_comments(data, tweet_id):
    tweet = Tweet.query.get(tweet_id)
    user = get_current_user()
    if tweet is None:
        return jsonify({"description": f"task '{tweet_id}' not found"}), 404
    if tweet.is_active() is False:
        return jsonify({"description": f"task '{tweet_id}' not found"}), 404
    if "content" not in data.keys():
        return jsonify({"description": "Missing 'content' key in the request body"}), 400

    new_comment = Comment(
        tweet_id=tweet_id,
        user_id=user.user_id,
        content=data["content"],
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify(new_comment.to_dict()), 201


def delete_single_comment(comment_id):

    comment = Comment.query.get(comment_id)
    user = get_current_user()
    tweet = Tweet.query.get(comment.tweet_id)

    if comment is None:
        return jsonify({"description": f"comment '{comment_id}' not found"}), 404
    if comment.is_active() is False:
        return jsonify({"description": f"comment '{comment_id}' not found"}), 404

    if comment.user_id != user.user_id and not user.is_admin():
        return jsonify({"description": "unauthorized"}), 401

    if tweet.is_active() is False:
        return jsonify({"description": f"Tweet '{comment_id}' not found"}), 404

    comment.comment_active = False
    db.session.commit()

    return jsonify({"description": "comment deleted"}), 200

