from rest_framework import serializers

from users.dtos.farm_dto import FarmDTO

class RegisterFarmSerializer(serializers.Serializer):

    name = serializers.CharField(
        max_length=150,
        required=True
    )

    location = serializers.CharField(
        max_length=150,
        required=True
    )

    municipality = serializers.CharField(
        max_length=150,
        required=True
    )

    def to_dto(self):

        return FarmDTO(
            name=self.validated_data["name"],
            location=self.validated_data["location"],
            municipality=self.validated_data["municipality"]
        )