from rest_framework import serializers


class AnalysisResultItemSerializer(serializers.Serializer):
    """Serializer para um item de resultado de análise."""
    common_name = serializers.CharField()
    scientific_name = serializers.CharField()
    susceptible_animal_species = serializers.ListField(child=serializers.CharField())
    human_risks = serializers.CharField()
    common_symptoms = serializers.ListField(child=serializers.CharField())
    recommended_actions = serializers.ListField(child=serializers.CharField())
    confidence_score = serializers.FloatField()


class AnalysisCreateResponseSerializer(serializers.Serializer):
    """Serializer para resposta de criação de análise."""
    search_request_id = serializers.IntegerField()
    result_type = serializers.CharField()
    analysis_results = AnalysisResultItemSerializer(many=True)
    error_message = serializers.CharField(required=False, allow_null=True)


class AnalysisHistoryItemSerializer(serializers.Serializer):
    """Serializer para um item do histórico de análises."""
    id = serializers.IntegerField()
    result_type = serializers.CharField()
    status = serializers.CharField()
    request_date = serializers.DateTimeField()
    finished_at = serializers.DateTimeField(required=False, allow_null=True)


class AnalysisHistoryResponseSerializer(serializers.Serializer):
    """Serializer para resposta de histórico de análises."""
    analyses = AnalysisHistoryItemSerializer(many=True)
    total = serializers.IntegerField()


class AnalysisDetailResponseSerializer(serializers.Serializer):
    """Serializer para resposta de detalhes de análise."""
    search_request_id = serializers.IntegerField()
    result_type = serializers.CharField()
    status = serializers.CharField()
    request_date = serializers.DateTimeField()
    finished_at = serializers.DateTimeField(required=False, allow_null=True)
    analysis_results = AnalysisResultItemSerializer(many=True)
    error_message = serializers.CharField(required=False, allow_null=True)
