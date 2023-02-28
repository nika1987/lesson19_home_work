from dao.model.user import User


class UserDao:
    def __init__(self, session):
        # Инициализация класса UserDao
        self.session = session

    def get_one(self, uid):
        # Метод возвращает пользователя, найденного по заданному идентификатору user_id
        return self.session.query(User).get(uid)

    def get_by_username(self, username):
        #Метод возвращает пользователя, найденного по заданному username
        return self.session.query(User).filter(User.username == username).first()

    def get_all(self):
        # Метод возвращает всех пользователей
        return self.session.query(User).all()

    def create(self, user_data):
        # создание пользователя
        entity = User(**user_data)

        self.session.add(entity)
        self.session.commit()
        return entity

    def delete(self, uid):
        # удаление пользователя
        user = self.get_one(uid)

        self.session.delete(user)
        self.session.commit()

    def update(self, user_data):
        # обновление пользователя
        uid = user_data.get('uid')

        user = self.get_one(uid)# экземпляр класса User
        user.username = user_data.get('username')
        user.password = user_data.get('password')

        self.session.add(user)
        self.session.commit()
