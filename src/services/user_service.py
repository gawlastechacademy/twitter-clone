from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity

from src.database import db
from src.models.role import Role
from src.models.user import User


def add_user_role():
    admin = Role.query.get(1)
    if admin is None:
        admin_role = Role(
            role_id=1,
            role_name="admin"
        )
        db.session.add(admin_role)

    user = Role.query.get(2)
    if user is None:
        user_role = Role(
            role_id=2,
            role_name="user"
        )
        db.session.add(user_role)
    db.session.commit()


def create_user(user_name, user_password):
    add_user_role()
    user = User.query.filter(User.user_name == user_name).first()

    if user is not None:
        return jsonify({"description": f"user '{user_name}' already exists in database"}), 409

    new_user = User(
        user_name=user_name,
        user_password=user_password,
        role_id=1,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201


def login(user_name, user_password):
    user = User.query.filter(User.user_name == user_name and User.user_password == user_password).first()

    if user is None:
        return jsonify({"description": "wrong username or password"}), 400

    if not user.is_active():
        return jsonify({"description": "unauthorized"}), 401

    access_token = create_access_token(identity=user_name)
    return jsonify(access_token=access_token), 200


def get_current_user():
    current_user = get_jwt_identity()
    user = User.query.filter(User.user_name == current_user).first()

    return user


def get_all_users():
    user = get_current_user()
    if not user.is_admin():
        return jsonify({"description": "unauthorized"}), 401
    users = User.query.all()
    user_dict = [user.to_dict() for user in users]
    return jsonify(user_dict), 200


def get_single_user(user_id):
    user_logged = get_current_user()
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"description": f"user '{user_id}' not found"}), 404

    return jsonify(user.to_dict()), 200


def change_single_user(data, user_id):
    user = User.query.get(user_id)
    user_logged = get_current_user()

    if user is None:
        return jsonify({"description": f"user '{user_id}' not found"}), 404

    if user.user_id != user_logged.user_id and not user_logged.is_admin():
        return jsonify({"description": "unauthorized"}), 401

    if "user_active" in data.keys():
        if not user_logged.is_admin:
            return jsonify({"description": "unauthorized"}), 401
        user.user_active = data["user_active"]
        db.session.commit()

    if "role_id" in data.keys():
        if not user_logged.is_admin():
            return jsonify({"description": "unauthorized"}), 401
        user.role_id = data["role_id"]
        db.session.commit()

    if "password" in data.keys():
        user.user_password = data["password"]
        db.session.commit()



    return jsonify(user.to_dict()), 200


def delete_single_user(user_id):
    user = User.query.get(user_id)
    user_logged = get_current_user()

    if user is None:
        return jsonify({"description": f"user '{user_id}' not found"}), 404

    if user.user_id != user_logged.user_id and not user_logged.is_admin():
        return jsonify({"description": "unauthorized"}), 401

    user.user_active = 0
    db.session.commit()
    return jsonify({"description": f"user {user_id} deleted"}), 200
