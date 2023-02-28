from flask import request, abort
from implemented import auth_service, user_service


def auth_required(func):
    # декоратор для не авторизованных пользователей
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        try:
            auth_service.decode_token(token)
        except Exception as e:
            print(e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    # декоратор, который проверяет права администратора
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        try:
            result = auth_service.decode_token(token)
        except Exception as e:
            print(e)
            abort(401)
        found_user = user_service.get_by_username(result['username'])
        if found_user['role'] != 'admin':
            abort(403)
        return func(*args, **kwargs)

    return wrapper
