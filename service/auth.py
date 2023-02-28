import calendar
import datetime

from flask import abort

import jwt

from helpers.constants import JWT_ALGORITHM, JWT_SECRET

from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        """
        иницилизация класса, в качестве зависимости имеет UserService
        """
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        """
        получив username и пароль мы можем найти нужного нам пользователя и сгенерировать токен
        """
        user = self.user_service.get_by_username(username)

        if user is None:
            raise abort(404)

        if not is_refresh:

            if not self.user_service.compare_password(user['password'], password):
                abort(401)

        data = {
            "username": user['username'],
            "role": user['role']
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def approve_refresh_token(self, refresh_token):
        """
        используя метод с декодированием токена.Получаем информацию о пользователи
        """
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        # проверяем есть ли токен. Нам прислали рефреш токен то мы доверяем пользователю и не требуем пароля
        username = data.get("username")
        user = self.user_service.get_by_username(username=username)
        if user is None:
            raise abort(404)

        return self.generate_tokens(username=username, password=user['password'], is_refresh=True)

    def decode_token(self, token):
        """
        это метод служит для декодирования токена
        """
        token = token.split("Bearer ")[-1] #получаем чистый токен из токена
        data = jwt.decode(jwt=token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM]) # извлечение декодированного токена в словарь
        return data
