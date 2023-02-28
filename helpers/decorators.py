from flask import request, abort
from implemented import auth_service, user_service


def auth_required(func):
    # декоратор для не авторизованных пользователей
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization', None)# получаем из реквеста распечатанный словарь(json)(headers и по ключу авторизейшен).Используем метод get.\
        # где указана авторизация и получаем токен
        try:
            auth_service.decode_token(token)# если токен нормальный. то мы декодируем(из строки которую получили) его и выполняем функцию
        except Exception as e:
            print(e)
            abort(401)# если у пользователя нет авторизации, то отправляем 401
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    # декоратор, который проверяет права администратора
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')#получаем из реквеста распечатанный словарь(json)(headers и по ключу авторизейшен).Используем метод get.\
        # где указана авторизация и получаем токен
        try:
            result = auth_service.decode_token(token)# если токен нормальный. то мы декодируем
        except Exception as e:
            print(e)
            abort(401)
        found_user = user_service.get_by_username(result['username'])# достаем из базы по ключу юсернейм и проверяем наличие пользователя
        if found_user is None:
            abort(404)# не найден
        if found_user['role'] != 'admin':
            abort(403)
        return func(*args, **kwargs)

    return wrapper
