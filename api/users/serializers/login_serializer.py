from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from users.dtos.login_dto import LoginDto


class LoginSerializer(serializers.Serializer):
    phone = PhoneNumberField(region="BR", required=True)

    password = serializers.CharField(
        write_only=True,
        min_length=6,
        required=True
    )

    def to_dto(self):
        return LoginDto(
            phone=self.validated_data.get("phone"),
            password=self.validated_data.get("password")
        )