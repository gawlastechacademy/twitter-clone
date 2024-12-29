from flask import jsonify
from sqlalchemy import func, case
from sqlalchemy.orm import aliased

from src.models.comment import Comment
from src.models.comment_like import CommentLike
from src.models.follow import Follow
from src.models.tweet import Tweet
from src.models.tweet_like import TweetLike
from src.services.user_service import get_current_user
from src.database import db
from src.models.user import User

CommentUser = aliased(User)
LikeUser = aliased(User)


# return tweet from user whose you follow
def get_follow_tweets():
    user = get_current_user()

    follow_tweet_connected = (
        db.session.query(Tweet.user_id, Tweet.tweet_id, Tweet.created_at, Tweet.content, Follow.follower_user_id,
                         func.count(Comment.comment_id).label('comment_count'),
                         func.count(TweetLike.like_id).label("like_count"), User.user_active)
        .join(Tweet, Tweet.user_id == Follow.followed_user_id)
        .outerjoin(Comment, Comment.tweet_id == Tweet.tweet_id)
        .outerjoin(TweetLike, TweetLike.tweet_id == Tweet.tweet_id)
        .outerjoin(User, User.user_id == Tweet.user_id)
        .filter(Follow.follower_user_id == user.user_id)
        .filter(User.user_active == 1)
        .order_by(Tweet.created_at.desc())
        .group_by(Tweet.user_id,
                  Tweet.tweet_id,
                  Tweet.created_at,
                  Tweet.content,
                  Follow.follower_user_id,
                  User.user_active, )
        .order_by(Tweet.created_at.desc())
        .all())

    follow_tweets_to_dict = [
        {
            "user_id": user_id,
            "tweet_id": tweet_id,
            "created_at": created_at,
            "content": content,
            "follower_user_id": follower_user_id,
            "comment_count": comment_count,
            "like_count": like_count,
            "user_active": user_active,

        }
        for user_id, tweet_id, created_at, content, follower_user_id, comment_count, like_count, user_active in
        follow_tweet_connected
    ]
    return jsonify(follow_tweets_to_dict), 200


def get_all_tweets():
    user = get_current_user()
    if not user.is_admin():
        return jsonify({"description": "unauthorized"}), 401
    all_tweets = (
        db.session.query(Tweet.user_id, User.user_active, Tweet.tweet_id, Tweet.created_at, Tweet.content,
                         func.count(Comment.comment_id).label('comment_count'),
                         func.count(TweetLike.like_id).label("like_count"))
        .outerjoin(Comment, Comment.tweet_id == Tweet.tweet_id)
        .outerjoin(TweetLike, TweetLike.tweet_id == Tweet.tweet_id)
        .outerjoin(User, User.user_id == Tweet.user_id)
        .group_by(Tweet.tweet_id)
        .order_by(Tweet.user_id.asc())
        .all())

    tweets_to_dict = [
        {
            "user_id": user_id,
            "user_active": user_active,
            "tweet_id": tweet_id,
            "created_at": created_at,
            "content": content,
            "comment_count": comment_count,
            "like_count": like_count,

        }
        for user_id, user_active, tweet_id, created_at, content, comment_count, like_count in
        all_tweets
    ]
    return jsonify(tweets_to_dict), 200


def add_single_tweets(content):
    user = get_current_user()
    user_id = user.user_id
    new_tweet = Tweet(
        user_id=user_id,
        content=content,
    )
    db.session.add(new_tweet)
    db.session.commit()

    return jsonify(new_tweet.to_dict()), 201


# if you follow or you are admin
def get_single_tweet(tweet_id):
    single_tweet = Tweet.query.get(tweet_id)

    if single_tweet is None:
        return jsonify({"description": f"tweet '{tweet_id}' not found"}), 404

    tweet_user = User.query.get(single_tweet.user_id)
    if not tweet_user.is_active():
        return jsonify({"description": f"tweet '{tweet_id}' not found"}), 404

    # choose count comment
    tweet_comments_count = (db.session.query(Comment.comment_id, Comment.tweet_id, CommentUser.user_active)
                            .outerjoin(CommentUser, CommentUser.user_id == Comment.user_id).filter(
        Comment.tweet_id == tweet_id).filter(CommentUser.user_active == 1).count())

    tweet_likes_count = (db.session.query(TweetLike.like_id, TweetLike.tweet_id, LikeUser.user_active)
                         .outerjoin(LikeUser, LikeUser.user_id == TweetLike.user_id)
                         .filter(TweetLike.tweet_id == tweet_id).filter(LikeUser.user_active == 1).count())

    tweet_to_dict = single_tweet.to_dict()

    comment_likes_count_subquery = (
        db.session.query(
            CommentLike.comment_id,
            func.count(case((LikeUser.user_active == 1, CommentLike.like_id))).label("comment_like_count")
        )
        .outerjoin(LikeUser, LikeUser.user_id == CommentLike.user_id)
        .group_by(CommentLike.comment_id)
        .subquery()
    )

    comments_to_tweet = (
        db.session.query(
            Comment.comment_id,
            Comment.created_at,
            Comment.user_id,
            Comment.content,
            func.coalesce(comment_likes_count_subquery.c.comment_like_count, 0).label("comment_like_count"),
            CommentUser.user_active,
        )
        .outerjoin(CommentUser, CommentUser.user_id == Comment.user_id)
        .outerjoin(comment_likes_count_subquery,
                   comment_likes_count_subquery.c.comment_id == Comment.comment_id)
        .filter(Comment.tweet_id == tweet_id)
        .filter(CommentUser.user_active == 1)
        .all()
    )


    #     comments_to_tweet = (db.session.query(Comment.comment_id, Comment.created_at, Comment.user_id,
    #     CommentUser.user_active)
    # .outerjoin(CommentUser, CommentUser.user_id == Comment.user_id)
    # .filter(Comment.tweet_id == tweet_id).filter(CommentUser.user_active == 1))

    # comments_to_tweet = (db.session.query(Comment.comment_id, Comment.created_at, Comment.user_id,
    #                                       Comment.content,
    #                                       func.count(case((LikeUser.user_active == 1, CommentLike.like_id))).label(
    #                                           "comment_like_count"), CommentUser.user_active)
    #                      .outerjoin(CommentLike, Comment.comment_id == CommentLike.comment_id)
    #                      .outerjoin(CommentUser, CommentUser.user_id == Comment.user_id)
    #                      .outerjoin(LikeUser, LikeUser.user_id == CommentLike.user_id)
    # 
    #                      .filter(Comment.tweet_id == tweet_id)
    #                      .filter(CommentUser.user_active == 1)
    #                      .group_by(Comment.comment_id, Comment.created_at, Comment.user_id, Comment.content,
    #                                CommentUser.user_active).all())

    comment_to_dict = [{
        "comment_id": comment_id,
        "comment_created_at": created_at,
        "user_id": user_id,
        "content": content,
        "comment_like_count": comment_like_count,
        "user_active": user_active,
    }

        for comment_id, created_at, user_id, content, comment_like_count, user_active in comments_to_tweet]

    tweet_to_dict["comments"] = comment_to_dict
    tweet_to_dict["comment_count"] = tweet_comments_count
    tweet_to_dict["like_count"] = tweet_likes_count
    return jsonify(tweet_to_dict), 200


def update_single_tweet(data, tweet_id):
    logged_user = get_current_user()
    tweet = Tweet.query.get(tweet_id)

    if tweet is None:
        return jsonify({"description": f"tweet '{tweet_id}' not found"}), 404

    if tweet.user_id != logged_user.user_id and not logged_user.is_admin():
        return jsonify({"description": "unauthorized"}), 401

    if "content" in data.keys():
        tweet.content = data["content"]
        db.session.commit()
    return jsonify(tweet.to_dict()), 200


def get_user_tweets(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"description": f"user '{user_id}' not found"}), 404

    tweets = Tweet.query.filter(Tweet.user_id == user.user_id).all()
    tweets_to_dict = [tweet.to_dict() for tweet in tweets]
    return jsonify(tweets_to_dict), 200


def delete_single_tweet(tweet_id):
    tweet = Tweet.query.get(tweet_id)
    user = get_current_user()

    if tweet is None:
        return jsonify({"description": f"tweet '{tweet_id}' not found"}), 404

    if tweet.user_id != user.user_id and not user.is_admin():
        return jsonify({"description": "unauthorized"}), 401

    # delete tweet like
    tweet.tweet_active = 0
    db.session.commit()

    return jsonify({"description": f"tweet {tweet.tweet_id} deleted"}), 200
