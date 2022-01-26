from django.db.models import fields
from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)
    def create(self, validated_data):

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            city=validated_data['city'],
        )
        return user

    class Meta:
        model = CustomUser
        # Tuple of serialized model fields (see link [2])
        fields = ("id", "username", "password", "email","phone","city","password2")


class UserSerializerProfile(serializers.ModelSerializer):
    class Meta:
        model =CustomUser
        fields = ['id', 'username' ,"phone" , "address" ,"city" ,"zip","image" ]




class UpdateProfileSerilizer(serializers.ModelSerializer):

    class Meta:
        models=CustomUser
        fields= ['id', 'username' ,"phone" , "address" ,"city" ,"zip","image" ]


class GenerateOtpLoginSerializer(serializers.Serializer):
    phone= serializers.CharField()


class LoginUserWithOtpSerializer(serializers.Serializer):
    phone= serializers.CharField()
    otp = serializers.CharField()
