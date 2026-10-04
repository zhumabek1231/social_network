from dataclasses import dataclass
import requests
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework. exceptions import APIException, AuthenticationFailed


@dataclass
class RemoteUser:
    id: int
    username: str
    is_official: bool

    @property
    def is_authenticated (self):
       return True

    @property
    def is_anonymous (self):
        return False


# class AuthServiceUnavailable(APIException):
#     status_code = 503
#     default_detail = 'Auth_Service временно не доступен.'
#     default_code = 'auth_service_unavailable'


class AuthServiceAuthentication (BaseAuthentication):
    def authenticate(self, request):
        authorization = get_authorization_header(request).split()

        if not authorization:
            return None

        if authorization[0].lower() != b'bearer':
           raise AuthenticationFailed('Используйте Bearer access token.')

        token = authorization[1].decode('utf-8')

        try:
            response = requests.get(
                 f'{settings.AUTH_SERVICE_URL}auth/verify/', headers = {'Authorization': f'Bearer {token}'}, timeout = 3)
        except requests.RequestException:
            raise 'service auth dont work'

        if response.status_code == 401:
            raise AuthenticationFailed('Access token неправильный или просрочен')
        if response.status_code != 200:
             raise APIException(f'error, {response.status_code}' )
        try:
            user_data = response.json()


            user = RemoteUser(
                id=int(user_data['id']),
                username=user_data['username'],
                is_official = user_data['is_official'],
            )
        except (ValueError, KeyError, TypeError):
            raise AuthenticationFailed('Auth Service вернул не правильные данные.')

        return user, token

    def authenticate_header(self, request):
       return 'Bearer'