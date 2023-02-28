import base64
import hashlib
import hmac

from flask import abort

from dao.model.user import UserSchema
from helpers.constants import PWD_SALT, PWD_ITERATIONS


class UserService:
    # Метод инициализации класса UserService
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        # Метод возвращает список всех пользователей
        try:
            result = self.dao.get_all()
            return UserSchema().dump(result, many=True)
        except Exception as e:
            print(e)
            return []

    def get_one(self, uid):
        # Метод возвращает пользователя по идентификатору
        try:
            result = self.dao.get_one(uid)
            return UserSchema().dump(result)
        except Exception as e:
            print(e)
            return "Нет такого пользователя"

    def get_by_username(self, username):
        # Метод возвращает пользователя, найденного по имени
        try:
            result = self.dao.get_by_username(username)
            return UserSchema().dump(result)
        except Exception as e:
            print(e)
            return "Нет такого пользователя"

    def create(self, user_data):
        if self.get_by_username(user_data.get('username')):
            return abort(400, 'Пользователь с таким именем ужe cуществует в базе данных')
        # Метод добавления нового пользователя в базу данных
        try:
            user_data['password'] = self.generate_password(user_data['password'])
            create_user = self.dao.create(user_data)
            user_dict = UserSchema().dump(create_user)
            user_dict.pop('password')
            return user_dict
        except Exception as e:
            print(e)
            return "Не удалось сгенерировать пароль пользователя"

    def delete(self, uid):
        # Метод удаления пользователя из базы данных
        try:
            self.dao.delete(uid)
        except Exception as e:
            print(e)
            return "Не удалось удалить пользователя"

    def update(self, user_data, uid):
        # Метод обновления пользователя в базу данных
        try:
            user_data['password'] = self.compare_password(user_data['password'])
            user_data['uid'] = uid
            self.dao.update(user_data)
            return "Обновлено успешно"
        except Exception as e:
            print(e)
            return "Не удалось обновить данные"

    def generate_password(self, password):

        # метод выполняет 2 операции: 1 получение бинарного представления, в виде некой последовательности чисел, которуюмы назовем hash_digest.

        hash_digest = hashlib.pbkdf2_hmac(

            'sha256',

            password.encode('utf-8'),
            PWD_SALT,

            PWD_ITERATIONS
        )

        return base64.b64encode(hash_digest)

    def compare_password(self, password_hash, other_password) -> bool:
        # Метод  на проверку соответствия пароля из реквеста паролю БД

        decoded_digest = base64.b64decode(password_hash)

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            PWD_SALT,
            PWD_ITERATIONS
        )
        # вернет результат True или False если хеши равны или не равны
        return hmac.compare_digest(decoded_digest, hash_digest)
