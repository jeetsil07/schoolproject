from rest_framework import serializers
from account.models import User
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    cpassword = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'cpassword', 'tc']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        print(data)
        if data['password'] != data['cpassword']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('cpassword')
        user = User.objects.create_user(**validated_data)
        return user       

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError({'msg': 'Invalid Credentials'})
        data['user'] = user
        return data
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'tc']
        
class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

    def validate_new_password(self, value):
        # Add any custom password validation here (length, complexity, etc.)
        if len(value) < 4:
            raise serializers.ValidationError("New password must be at least 4 characters long")
        return value