from main.exceptions import AuthFailed
from main.settings import SECRET_KEY
from user.models import BlacklistedToken, User
from rest_framework.exceptions import *
import jwt
import datetime

class TokenManager:
    def getUser(self, request):
        auth = request.headers.get("Authorization")
        if auth is None:
            raise AuthFailed("Authorization Required!", status.HTTP_401_UNAUTHORIZED)
        token = auth.split(" ")[-1]
        payload = self.decodeToken(token)
        user = User.objects.filter(id=payload["id"]).first()
        if user:
            return user
        raise AuthFailed("User not Found!")

    def getUserWithToken(self, request):
        auth = request.headers.get("Authorization")
        if auth is None:
            raise AuthFailed("Authorization Required!")
        token = auth.split(" ")[-1]
        payload = self.decodeTokenWithoutVerification(token)
        user = User.objects.filter(id=payload["id"]).first()
        if user:
            return user, token
        raise AuthFailed("User not Found!")

    def generateAccessToken(self, user):
        exp_time = datetime.timedelta(days=60)

        payload = {
            "id": user.id,
            "username": str(user.username),
            "email": str(user.email),
            "exp": datetime.datetime.utcnow() + exp_time,
            "iat": datetime.datetime.utcnow(),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    def generateRefreshToken(self, user):
        exp_time = datetime.timedelta(days=60)

        payload = {
            "id": user.id,
            "username": str(user.username),
            "email": str(user.email),
            "exp": datetime.datetime.utcnow() + exp_time,
            "iat": datetime.datetime.utcnow(),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    def decodeToken(self, token):
        if not token:
            raise AuthFailed("Unauthorized!", 401)

        isBlacklisted = self.isTokenBlacklisted(token)
        if isBlacklisted:
            raise AuthFailed("Token Blacklisted", 401)

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthFailed("Login Session Expired", 401)
        except jwt.DecodeError:
            raise AuthFailed("Session can't be verified!", 401)
        except:
            raise AuthFailed("Login again", 401)

    def decodeTokenWithoutVerification(self, token):
        if not token:
            raise AuthFailed("Token not found")
        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"],
                options={"verify_signature": False},
            )
            return payload
        except:
            return None

    def isTokenBlacklisted(self, token):
        if BlacklistedToken.objects.filter(token=token).exists():
            return True
        else:
            return False