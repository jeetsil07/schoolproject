import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.serializers import UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                'msg': 'Registration Successful',
                'tokens': tokens
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return Response({
                'msg': 'Login Successful',
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request,"1")
        print(request.user,"2")
        serializer = UserProfileSerializer(request.user)
        return Response({'profile': serializer.data}, status=status.HTTP_200_OK)