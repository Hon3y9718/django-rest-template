from rest_framework.exceptions import APIException

class AuthFailed(APIException):
    status_code = 401
    default_detail = 'Authentication credentials were not provided or invalid'
    default_code = 'not_authenticated'

class NotFound(APIException):
    status_code = 404
    default_detail = 'Not Found'
    default_code = 'not_found'

class Success(APIException):
    status_code = 200
    default_detail = 'Success'
    default_code = 'success'