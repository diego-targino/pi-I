from users.repositories import UserRepository

class UserService:

    @staticmethod
    def get_user_by_id(user_id):
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def create_user(data):
        if UserRepository.get_by_email(data["email"]):
            raise Exception("Email já existe")

        return UserRepository.create(data)