import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.serializers import UserLoginSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            print(email, password)
            user = authenticate(email=email, password=password)
            if user is None:
                return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'msg': 'Login Successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)