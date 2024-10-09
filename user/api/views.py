from rest_framework.response import Response
from rest_framework import status
from user.api.serializers import RegistationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
class RegistrationView(APIView):

    
    def post(self, request):
        
        serializer = RegistationSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'User registered successfully'
            data['email'] = user.email
            data['username'] = user.username
            data["token"] = Token.objects.get(user=user).key
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutView(APIView):
    def post(self, request):
        # Retrieve the token associated with the user
        if request.user.is_authenticated:
            try:
                token = Token.objects.get(user=request.user)
                token.delete()  # Delete the token to log out the user
                return Response({"message": "You have logged out"}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({"error": "Token doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "User is not logged in"}, status=status.HTTP_400_BAD_REQUEST)
            
            
class JWTRegisterView(APIView):
    def post(self, request):
        
        serializer = RegistationSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'User registered successfully'
            data['email'] = user.email
            data['username'] = user.username
            refresh = RefreshToken.for_user(user)
            data["token"] = {
                "refresh" : str(refresh),
                "access": str(refresh.access_token)
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
