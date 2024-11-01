from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from utility.utils import *
from user.serializers import *
from user.models import BlacklistedToken, User
from main.exceptions import *

# Create your views here.
class SignUpView(APIView):
    utils = Utils()
    @csrf_exempt
    def post(self, request):
        ## Check for required fields
        required_fields = ['first_name', 'last_name', 'email', 'password', 'role']
        self.utils.check_required_fields(request.data, required_fields)

        email = request.data["email"].lower()
        userWithEmail = User.objects.filter(email=email.lower()).first()

        if userWithEmail:
            raise AuthFailed("An Account with this Email Already Exists")
        else:
            ## Register User
            request.data['username'] = email
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            ## Get user and Generate Token
            user = User.objects.filter(email=request.data["email"]).get()
            
            user.is_logged_in = True
            user.save()

            accessToken = self.utils.generateAccessToken(user)
            refreshToken = self.utils.generateRefreshToken(user)

            return Response(
                {"result": True, "token": accessToken, "refreshToken": refreshToken, "user": UserSerializer(user).data}
            )
        
class LoginView(APIView):
    utils = Utils()
    def post(self, request):
        
        ## Check for required fields
        required_fields = ['email', 'password']
        self.utils.check_required_fields(request.data, required_fields)

        email = request.data["email"].lower()
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None or user.is_deleted:
            raise NotFound("We don't have an account with this Email")
        if not user.check_password(password):
            raise AuthFailed("Incorrect Password")
        
        user.is_logged_in = True
        user.save()

        accessToken = self.utils.generateAccessToken(user)
        refreshToken = self.utils.generateRefreshToken(user)
        
        return Response(
            {"result": True, "token": accessToken, "refreshToken": refreshToken, "user": UserSerializer(user).data}
        )

class LogoutView(APIView):
    utils = Utils()

    def get(self, request):
        user, token = self.utils.getUserWithToken(request)
        ## Blacklist given token if not expired already
        if not BlacklistedToken.objects.filter(token=token).exists():
            # Save the token to the BlacklistedToken table if it doesn't exist
            BlacklistedToken.objects.create(token=token)
                        
        user.is_logged_in = False

        return Response({"result": True})

class MyProfileView(APIView):
    utils = Utils()

    def get(self, request):
        user = self.utils.getUser(request)
        serializer = UserSerializer(user)

        return Response({"result": True, "user": serializer.data})
    
class DeactivateAccountView(APIView):
    utils = Utils()

    def post(self, request):
        user = self.utils.getUser(request)

        user.is_active = False  # Deactivate the user account
        user.save()
        return Response({"message": "Your account has been deactivated."}, status=status.HTTP_200_OK)

class ActivateAccountView(APIView):
    utils = Utils()

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, pk=user_id)
        user.is_active = True  # Deactivate the user account
        user.save()
        return Response({"message": "Your account has been activated."}, status=status.HTTP_200_OK)

class DeleteUserAccountView(APIView):
    utils = Utils()

    def delete(self, request):
        user = self.utils.getUser(request)

        user.is_deleted = True  # Deactivate the user account
        user.save()
        return Response({"message": "Your account has been deleted."}, status=status.HTTP_200_OK)

class UpdateProfile(APIView):
    utils = Utils()

    # Partially update a User Role
    def put(self, request, *args, **kwargs):
        user = self.utils.getUser(request)

        user_id = kwargs.get('id')
        user_instance = get_object_or_404(User, pk=user_id)

        serializer = UserSerializer(user_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": True, "user": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
