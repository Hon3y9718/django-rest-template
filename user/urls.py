from django.urls import path
from .views.authViews import *

urlpatterns = [
    path("signup", SignUpView.as_view(), name="register-user"),
    path("login", LoginView.as_view(), name="login-user"),
    path("logout", LogoutView.as_view(), name="logput-user"),
    path("profile", MyProfileView.as_view(), name="profile-user"),
    path("deactivate", DeactivateAccountView.as_view(), name="deactive-user"),
    path("activate/<int:id>", ActivateAccountView.as_view(), name="deactive-user"),
    path("delete", DeleteUserAccountView.as_view(), name="delete-user"),
    path("update/<int:id>", UpdateProfile.as_view(), name="update-user"),
]