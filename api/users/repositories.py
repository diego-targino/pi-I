from core.database.base_repository import BaseRepository
from users.models import User


class UserRepository(BaseRepository):
    model = User

    @classmethod
    def get_by_email(cls, email):
        return cls.model.objects.filter(email=email).first()