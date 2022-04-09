from rest_framework.exceptions import APIException

class ProfileNotFound(APIException):
    status_code = 404
    default_detail = 'Profile not found'
    default_code = 'profile_not_found'

class NotYourProfile(APIException):
    status_code = 403
    default_detail = 'Not your profile'
    default_code = 'not_your_profile'