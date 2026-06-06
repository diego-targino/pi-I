from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action

from analysis.serializers.analysis_serializer import AnalysisSerializer
from analysis.services.plant_analisys_service import PlantAnalysisService

class PlantAnalysisViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = AnalysisSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        dto = serializer.to_dto()
        result = PlantAnalysisService.analisys(dto)
        return Response(
            result,
            status=status.HTTP_200_OK
        )

    def list(self, request):

        user_id = request.query_params.get("userId")

        if not user_id:
            return Response(
                {"message": "userId é obrigatório"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = PlantAnalysisService.get_history(
            int(user_id)
        )

        return Response(
            result,
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, pk=None):
        user_id = request.query_params.get("userId")

        if not user_id:
            return Response(
                {"message": "userId é obrigatório"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = PlantAnalysisService.get_details(
            int(pk),
            int(user_id)
        )

        return Response(
            result,
            status=status.HTTP_200_OK
        )
