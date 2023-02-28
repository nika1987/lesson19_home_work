from flask import request
from flask_restx import Namespace, Resource

from implemented import user_service

user_ns = Namespace('user')


@user_ns.route('/')
class UsersView(Resource):

    def get(self):
        all_users = user_service.get_all()

        return all_users, 200

    def post(self):
        data = request.json
        user = user_service.create(data)

        return user, 201, {'Location': f'/users{user["id"]}'}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        one_user = user_service.get_one(uid)

        return one_user, 200

    def put(self, uid):
        new_user = request.json

        return user_service.update(new_user, uid), 200

    def delete(self, uid):
        user_service.delete(uid)
        return "", 204
