from unittest.mock import MagicMock

import pytest as pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture
def movie_dao():
    movie_dao = MovieDAO(None)

    first_movie = Movie(title="Москва слезам не верит", description="О любви", trailer="https://www.youtube.com/watch?v=UKei_d0cbP4",
                        year=2019, rating=5, director="Иванов Иван", genre="Роман")
    second_movie = Movie(title="Титаник", description="О любви", trailer="www.youtube.com/watch?v",  year=2021, rating=7, director="Иванов Иван", genre="Роман")

    third_movie = Movie(title="Шпион", description="О шпионе", trailer="www.youtube.com/watch?v",  year=2022, rating=8, director="Иванов Иван", genre="Роман")

    movie_dao.get_one = MagicMock(return_value=first_movie)
    movie_dao.get_all = MagicMock(return_value=[first_movie, second_movie, third_movie])
    movie_dao.create = MagicMock(return_value=Movie(first_movie))
    movie_dao.update = MagicMock(return_value=Movie(second_movie))
    movie_dao.delete = MagicMock(return_value=Movie(third_movie))
    return movie_dao

class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_all_movies(self):
        movies = self.movie_service.get_all()

        assert len(movies) > 0

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie.id == 1
        assert movie.id is not None

    def test_create(self):
        movie_d = {"name": "Ужасы"}

        movie = self.movie_service.create(movie_d)

        assert movie.id is not None

   #def test_update(self):
        #movie_d = {"name": "Комедия"}

        #assert self.movie_service.update(movie_d) is not None