from datetime import UTC, datetime, timedelta

from decouple import config
from users.dtos.login_dto import LoginDto
from users.dtos.register_user_dto import RegisterUserDTO
from users.models.farm_model import Farm
from users.models.user_model import User, UserStatus
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
import jwt

class UserService:

    @staticmethod
    @transaction.atomic
    def create_user(dto : RegisterUserDTO):

        if User.objects.filter( phone=dto.phone).exists():
            raise Exception("Telefone já existe")
        
        user = User.objects.create(
            name = dto.name,
            phone = dto.phone,
            password_hash = make_password(
                dto.password
            ),
            is_admin = False,
            status = UserStatus.ACTIVE
        );

        farm =Farm.objects.create(
            user = user,
            name = dto.farm.name,
            location = dto.farm.location,
            municipality = dto.farm.municipality
        );
    
        return {
            "user": {
                "id": user.id,
                "name": user.name,
                "phone": user.phone,
                "is_admin": user.is_admin,
                "status": user.status,
                "farm": {
                    "name": farm.name,
                    "location": farm.location,
                    "municipality": farm.municipality
                } if farm else None
            }
        }

    @staticmethod
    def login(dto: LoginDto):
    
        user = User.objects.filter(phone=dto.phone).first()
        
        if not user:
            raise Exception("Telefone ou Senha incorretos")

        if not check_password(dto.password, user.password_hash):
            raise Exception("Telefone ou Senha incorretos")

        farm = Farm.objects.filter(user=user).first()

        expiration = datetime.now(UTC) + timedelta(hours=24)

        token = jwt.encode(
            {
                "sub": user.id,
                "phone": user.phone,
                "exp": expiration
            },
            config('JWT_SECRET_KEY'),
            algorithm="HS256"
        )
        
        return {
            "token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "phone": user.phone,
                "is_admin": user.is_admin,
                "status": user.status,
                "farm": {
                    "name": farm.name,
                    "location": farm.location,
                    "municipality": farm.municipality
                } if farm else None
            }
        }