import base64
from dataclasses import asdict
from datetime import datetime
import json
from time import timezone
from typing import List
import uuid

from analysis.dtos.analisys_dto import AnalysisDto
from django.core.files.base import ContentFile

from django.db import transaction
from analysis.models.plant_analysis_result_model import PlantAnalysisResult
from analysis.models.search_error_log_model import SearchErrorLog
from analysis.models.search_request_model import SearchRequest
from core.ai.gemini_service import GeminiService
from core.ai.responses.plant_analysis_response import PlantAnalysisResponse
from users.models.user_model import User
from rest_framework.exceptions import NotFound

class PlantAnalysisService:

    @transaction.atomic
    def analisys(dto : AnalysisDto):

        user = User.objects.filter(id=dto.user_id).first()

        if not user:
            raise NotFound("Usuário não encontrado")

        file_name = f"{uuid.uuid4()}.{dto.extension}"

        image_content = ContentFile(
            base64.b64decode(dto.base64),
            name=file_name
        )

        search_request = SearchRequest.objects.create(
            user=user,
            status=SearchRequest.STATUS_PROCESSING,
            request_date=datetime.now()
        )

        search_request.image.save(
            file_name,
            image_content,
            save=True
        )

        result : PlantAnalysisResponse = GeminiService.analyse_image(
            dto.base64,
            dto.mime_type
        )

        try:
            if result.ResultType in [SearchRequest.RESULT_COMPLETE, SearchRequest.RESULT_PARTIAL]:
                search_request.api_status_code = 200
                search_request.result_type = result.ResultType
                search_request.status = SearchRequest.STATUS_COMPLETED
                search_request.finished_at = datetime.now()

                search_request.save(
                    update_fields=[
                        "api_status_code",
                        "status",
                        "result_type",
                        "finished_at"
                    ]
                )

                for analysis_result in result.AnalysisResults:
                    plant_analisis_result = PlantAnalysisResult.objects.create(
                        search_request=search_request,
                        common_name =analysis_result.CommonName,
                        scientific_name=analysis_result.ScientificName,
                        susceptible_animal_species=";".join(analysis_result.SusceptibleAnimalSpecies if analysis_result.SusceptibleAnimalSpecies else []),
                        human_risks=analysis_result.HumanRisks,
                        common_symptoms=";".join(analysis_result.CommonSymptoms if analysis_result.CommonSymptoms else []),
                        recommended_actions=";".join(analysis_result.RecommendedActions if analysis_result.RecommendedActions else []),
                        confidence_score=analysis_result.ConfidenceScore
                    )

                    plant_analisis_result.save()
            else:
                search_request.status = SearchRequest.STATUS_FAILED
                search_request.api_status_code = 200
                search_request.result_type = result.ResultType
                search_request.finished_at = datetime.now()

                search_request.save(
                    update_fields=[
                        "status",
                        "api_status_code",
                        "result_type",
                        "finished_at"
                    ]
                )

                SearchErrorLog.objects.create(
                    search_request=search_request,
                    request_date=search_request.request_date,
                    status_code=200,
                    error_type=SearchErrorLog.ERROR_NOT_IDENTIFIED if result.ResultType == SearchRequest.RESULT_NOT_FOUND else SearchErrorLog.ERROR_INTERNAL_ERROR,
                    error_description=result.ErrorMessage,
                    error_response=result.ResponseContent
                )

            return {
                "search_request_id": search_request.id,
                "result_type": search_request.result_type,
                "analysis_results": [
                    asdict(item)
                    for item in result.AnalysisResults
                ] if result.AnalysisResults else [],
                "error_message": result.ErrorMessage 
            }

        except Exception as ex:

            search_request.status = SearchRequest.STATUS_FAILED
            search_request.api_status_code = 500
            search_request.finished_at = datetime.now()

            search_request.save(
                update_fields=[
                    "status",
                    "api_status_code",
                    "finished_at"
                ]
            )

            SearchErrorLog.objects.create(
                search_request=search_request,
                request_date=search_request.request_date,
                status_code=500,
                error_type=SearchErrorLog.ERROR_INTERNAL_ERROR,
                error_description=str(ex),
                error_response=result.ResponseContent
            )

            return {
                "search_request_id": search_request.id,
                "result_type": search_request.result_type,
                "error_message": "Houve um erro no processamento da imagem, por favor tente novamente mais tarde."
            }
    @staticmethod
    def get_details(search_request_id, user_id):

        user = User.objects.filter(id=user_id).first()

        if not user:
            raise NotFound("Usuário não encontrado")

        search_request = SearchRequest.objects.filter(
            id=search_request_id
        ).first()

        if not search_request:
            raise NotFound("Análise não encontrada")

        if search_request.user.id != user.id:
            raise NotFound("Análise não encontrada")

        return {
            "search_request_id": search_request.id,
            "result_type": search_request.result_type,
            "status": search_request.status,
            "image": search_request.image.url if search_request.image else None,
            "analysis_results": [
                {
                    "id": result.id,
                    "common_name": result.common_name,
                    "scientific_name": result.scientific_name,
                    "susceptible_animal_species": result.susceptible_animal_species,
                    "human_risks": result.human_risks,
                    "common_symptoms": result.common_symptoms,
                    "recommended_actions": result.recommended_actions,
                    "confidence_score": float(result.confidence_score)
                }
                for result in search_request.results.all()
            ]
        }