from rest_framework import serializers
from account.models import User

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
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']
       

    # def validate(self, data):
    #     email = data.get('email')
    #     password = data.get('password')

    #     if not email or not password:
    #         raise serializers.ValidationError("Email and password are required")

    #     user = User.objects.filter(email=email).first()
    #     if user is None or not user.check_password(password):
    #         raise serializers.ValidationError("Invalid credentials")

    #     return user