from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service
from helpers.decorators import auth_required, admin_required
director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @auth_required
    def post(self):
        data = request.json
        director = director_service.create(data)
        return director, 201


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, bid):
        new_director = request.json
        if "id" not in new_director:
            new_director["id"] = bid
        director_service.update(new_director)
        return "", 204

    @admin_required
    def delete(self, bid):
        director_service.delete(bid)
        return "", 204
