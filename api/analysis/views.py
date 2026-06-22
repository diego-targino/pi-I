from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from analysis.serializers.analysis_serializer import AnalysisSerializer
from analysis.serializers.response_serializers import (
    AnalysisCreateResponseSerializer,
    AnalysisHistoryItemSerializer,
    AnalysisHistoryResponseSerializer,
    AnalysisDetailResponseSerializer
)
from analysis.services.plant_analisys_service import PlantAnalysisService

class PlantAnalysisViewSet(viewsets.ViewSet):
    """
    API de Análise de Plantas
    
    Endpoints para análise de imagens de plantas e histórico de análises.
    """

    @extend_schema(
        summary="Criar Análise de Planta",
        description="Realiza análise de uma imagem de planta e retorna diagnóstico com base em IA",
        request=AnalysisSerializer,
        responses={
            200: AnalysisCreateResponseSerializer,
            400: {"description": "Dados inválidos ou imagem em formato inválido"},
        }
    )
    def create(self, request):
        """
        Analisa uma imagem de planta.
        
        Aceita imagem em formato Base64 Data URI e retorna diagnóstico.
        """
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

    @extend_schema(
        summary="Listar Histórico de Análises",
        description="Retorna todas as análises completamente identificadas realizadas por um usuário. "
                    "Inclui informações da imagem e o primeiro resultado de análise de cada busca.",
        parameters=[
            OpenApiParameter(
                name='userId',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=True,
                description='ID do usuário proprietário das análises'
            )
        ],
        responses={
            200: AnalysisHistoryItemSerializer(many=True),
            400: {"description": "userId não fornecido ou inválido"},
            404: {"description": "Usuário não encontrado"},
        }
    )
    def list(self, request):
        """
        Lista histórico de análises de um usuário.
        
        Retorna apenas análises com resultado_type = RESULT_COMPLETE.
        Ordenadas por data da requisição (mais recentes primeiro).
        
        Parâmetro obrigatório: userId (query parameter)
        """
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

    @extend_schema(
        summary="Obter Detalhes de Análise",
        description="Retorna detalhes completos de uma análise específica",
        parameters=[
            OpenApiParameter(
                name='userId',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=True,
                description='ID do usuário'
            )
        ],
        responses={
            200: AnalysisDetailResponseSerializer,
            400: {"description": "userId não fornecido"},
            404: {"description": "Análise não encontrada"},
        }
    )
    def retrieve(self, request, pk=None):
        """
        Obtém detalhes de uma análise específica.
        
        Parâmetro obrigatório: userId (query parameter)
        """
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
