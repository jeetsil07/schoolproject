import re
from django.db import connections
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from account.serializers import UserLoginSerializer, UserPasswordChangeSerializer, UserProfileSerializer, UserRegistrationSerializer
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
        serializer = UserProfileSerializer(request.user)
        return Response({'profile': serializer.data}, status=status.HTTP_200_OK)


class UserPasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserPasswordChangeSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(
                serializer.validated_data['new_password'])
            request.user.save()
            return Response({'msg': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersdetailsView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            users_list = User.objects.fetch_basi_users()
            if not users_list:
                return Response({'msg': 'No users found'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'users': users_list}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)