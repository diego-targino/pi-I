from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from users.dtos.farm_dto import FarmDTO
from users.dtos.register_user_dto import RegisterUserDTO

from users.serializers.register_farm_serializer import (
    RegisterFarmSerializer
)


class RegisterUserSerializer(serializers.Serializer):

    name = serializers.CharField(
        max_length=150,
        required=True
    )

    phone = PhoneNumberField(
        region="BR",
        required=True
    )

    password = serializers.CharField(
        write_only=True,
        min_length=6,
        required=True
    )

    confirm_password = serializers.CharField(
        write_only=True,
        required=True
    )

    farm = RegisterFarmSerializer(
        required=True
    )

    def validate(self, data):

        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password":
                    "As senhas não coincidem."
                }
            )

        return data

    def to_dto(self):

        farm_data = self.validated_data["farm"]

        farm_dto = FarmDTO(
            name=farm_data["name"],
            location=farm_data["location"],
            municipality=farm_data["municipality"]
        )

        return RegisterUserDTO(
            name=self.validated_data["name"],
            phone=str(self.validated_data["phone"]),
            password=self.validated_data["password"],
            farm=farm_dto
        )