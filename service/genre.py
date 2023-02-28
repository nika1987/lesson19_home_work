from dao.genre import GenreDAO
from dao.model.genre import GenreSchema


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, genre_d):
        created_genre = self.dao.create(genre_d)
        return GenreSchema().dump(created_genre)

    def update(self, genre_d):
        self.dao.update(genre_d)

    def delete(self, rid):
        self.dao.delete(rid)
