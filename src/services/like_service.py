from flask import jsonify

from src.database import db
from src.models.comment import Comment
from src.models.comment_like import CommentLike
from src.models.tweet import Tweet
from src.models.tweet_like import TweetLike
from src.services.user_service import get_current_user


def get_tweet_likes(tweet_id):
    tweet = Tweet.query.get(tweet_id)
    if tweet is None:
        return jsonify({"description": f"task '{tweet_id}' not found"}), 404
    if tweet.is_active() is False:
        return jsonify({"description": f"task '{tweet_id}' not found"}), 404
    tweet_likes = TweetLike.query.filter(TweetLike.tweet_id == tweet_id).all()
    tweet_likes_to_dict = [like.to_dict() for like in tweet_likes]
    return jsonify(tweet_likes_to_dict), 200


def get_comment_likes(comment_id):
    comment = Comment.query.get(comment_id)
    tweet = Tweet.query.get(comment.tweet_id)
    if comment is None:
        return jsonify({"description": f"task '{comment_id}' not found"}), 404
    if comment.is_active() is False:
        return jsonify({"description": f"task '{comment_id}' not found"}), 404
    if tweet.is_active() is False:
        return jsonify({"description": f"task '{tweet.tweet_id}' not found"}), 404

    comment_likes = CommentLike.query.filter(CommentLike.comment_id == comment_id).all()
    comment_likes_to_dict = [like.to_dict() for like in comment_likes]
    return jsonify(comment_likes_to_dict), 200


def add_tweet_like(tweet_id):
    tweet = Tweet.query.get(tweet_id)
    user = get_current_user()
    if tweet is None:
        return jsonify({"description": f"task '{tweet_id}' not found"}), 404

    if tweet.is_active() is False:
        return jsonify({"description": f"task '{tweet_id}' not found"}), 404

    tweet_like = (TweetLike.query
                  .filter(TweetLike.tweet_id == tweet_id)
                  .filter(TweetLike.user_id == user.user_id).first())
    if tweet_like is not None:
        return jsonify({"description": "you can't add next tweet like"}), 409

    user = get_current_user()

    new_like = TweetLike(
        tweet_id=tweet_id,
        user_id=user.user_id
    )
    db.session.add(new_like)
    db.session.commit()
    return jsonify(new_like.to_dict()), 201


def add_comment_like(comment_id):
    comment = Comment.query.get(comment_id)
    user = get_current_user()

    if comment is None:
        return jsonify({"description": f"comment '{comment_id}' not found"}), 404

    if comment.is_active() is False:
        return jsonify({"description": f"comment '{comment_id}' not found"}), 404

    tweet = Tweet.query.get(comment.tweet_id)
    if tweet.is_active() is False:
        return jsonify({"description": f"tweet '{tweet.tweet_id}' not found"}), 404

    comment_like = CommentLike.query.filter(
        CommentLike.comment_id == comment_id).filter(CommentLike.user_id == user.user_id).first()
    if comment_like is not None:
        return jsonify({"description": "you can't add next comment like"}), 409

    new_like = CommentLike(
        comment_id=comment_id,
        user_id=user.user_id
    )
    db.session.add(new_like)
    db.session.commit()
    return jsonify(new_like.to_dict()), 201


def delete_tweet_like(tweet_id, like_id):
    tweet_like = TweetLike.query.get(like_id)
    tweet = Tweet.query.get(tweet_id)
    if tweet_like is None:
        return jsonify({"description": f"Tweet like '{like_id}' not found"}), 404

    if tweet_like.tweet_id != tweet_id:
        return jsonify({"description": "worng request"}), 404

    if tweet.is_active() is False:
        return jsonify({"description": f"Tweet '{tweet_id}' not found"}), 404

    db.session.delete(tweet_like)
    db.session.commit()
    return jsonify({"description": "tweet like deleted"}), 200


def delete_comment_like(comment_id, like_id):
    comment_like = CommentLike.query.get(like_id)
    comment = Comment.query.get(comment_id)
    tweet = Tweet.query.get(comment.tweet_id)
    if comment_like is None:
        return jsonify({"description": f"comment like '{like_id}' not found"}), 404

    if comment_like.comment_id != comment_id:
        return jsonify({"description": "worng request"}), 404

    if comment.is_active() is False:
        return jsonify({"description": f"comment '{comment_id}' not found"}), 404

    if tweet.is_active() is False:
        return jsonify({"description": f"Tweet '{tweet.tweet_id}' not found"}), 404

    db.session.delete(comment_like)
    db.session.commit()
    return jsonify({"description": "comment like deleted"}), 200
