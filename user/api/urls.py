from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user.api.views import RegistrationView, LogoutView, JWTRegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("login/",obtain_auth_token, name="obtain_auth_token" ),# For obtaining token for authenticated users)
    path("register/", RegistrationView.as_view(),name="register"),# For registering new users)
    path("logout/", LogoutView.as_view(), name="logout"),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/register/", JWTRegisterView.as_view(), name='jwt_register')
]