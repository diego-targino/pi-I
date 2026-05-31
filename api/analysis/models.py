from django.db import models
from users.models.user_model import User


class SearchRequest(models.Model):

    RESULT_COMPLETE = 0
    RESULT_PARTIAL = 1
    RESULT_NOT_FOUND = 3

    STATUS_PENDING = 0
    STATUS_PROCESSING = 1
    STATUS_COMPLETED = 3
    STATUS_FAILED = 4

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="search_requests"
    )

    image_path = models.CharField(max_length=150)

    result_type = models.IntegerField(
        null=True,
        blank=True
    )

    status = models.IntegerField(
        default=STATUS_PENDING
    )

    api_status_code = models.IntegerField(
        null=True,
        blank=True
    )

    request_date = models.DateTimeField(
        auto_now_add=True
    )

    finished_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Request {self.id}"


class PlantAnalysisResult(models.Model):

    search_request = models.ForeignKey(
        SearchRequest,
        on_delete=models.CASCADE,
        related_name="results"
    )

    common_name = models.CharField(max_length=100)

    scientific_name = models.CharField(
        max_length=100
    )

    susceptible_animal_species = models.TextField()

    human_risks = models.TextField()

    common_symptoms = models.TextField()

    recommended_actions = models.TextField()

    confidence_score = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.common_name


class SearchErrorLog(models.Model):

    ERROR_API_UNAVAILABLE = 0
    ERROR_TIMEOUT = 1
    ERROR_INVALID_RESPONSE = 2
    ERROR_NOT_IDENTIFIED = 3
    ERROR_INTERNAL_ERROR = 4

    search_request = models.OneToOneField(
        SearchRequest,
        on_delete=models.CASCADE,
        related_name="error_log"
    )

    request_date = models.DateTimeField()

    status_code = models.IntegerField()

    error_type = models.IntegerField()

    error_description = models.TextField()

    error_response = models.TextField()

    def __str__(self):
        return f"Error {self.id}"