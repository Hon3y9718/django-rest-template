from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination

from utility.tokenManager import TokenManager

class Utils(TokenManager):
    def check_required_fields(self, data, required_fields):
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValidationError({"detail": f"Missing required fields: {', '.join(missing_fields)}"})

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20  # Default page size
    page_size_query_param = 'size'  # Query parameter to control the page size
    max_page_size = None  # Maximum page size that can be requested
