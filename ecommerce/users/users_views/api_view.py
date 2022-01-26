import base64
import pyotp
import environ
import os

from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from aiohttp import ClientSession
import asyncio

from users.models import CustomUser
from users.serializers import UserSerializer, UserSerializerProfile, LoginUserWithOtpSerializer, GenerateOtpLoginSerializer


async def send_otp(phone, otp):
    async with ClientSession() as session:
        unit_url = "https://RestfulSms.com/api/Token"
        validation_headers = {'content-type': 'application/json'}
        validation_body = {"SecretKey": os.environ.get(
            'SECURITY_CODE'), "UserApiKey": os.environ.get('API_KEY')}
        response = await session.post(unit_url, json=validation_body, headers=validation_headers)
        if response.status != 201:
            return False
        data1 = await response.json()
        sending_sms_url = "http://RestfulSms.com/api/VerificationCode"
        sms_body = {"Code": otp, "MobileNumber": phone}
        headers_sms = {'content-type': 'application/json',
                       "x-sms-ir-secure-token": data1["TokenKey"]}
        response = await session.post(sending_sms_url, json=sms_body, headers=headers_sms)
        if response.status != 201:
            return False
        return await response.json()


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.now()) + pyotp.random_hex()


class generationOtp:
    def create_otp(self, phone):
        keygen = pyotp.random_hex()
        key = base64.b32encode(keygen.encode())
        self.totp = pyotp.TOTP(key, interval=300)
        return self.totp.now()


sample = generationOtp()


class RegisterAPI(generics.CreateAPIView):
    model = CustomUser

    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):

        if request.data["password"] == request.data["password2"]:
            if "phone" in request.data and "email" in request.data and "city" in request.data:
                serializer = self.get_serializer(data=request.data)
                isvalid = serializer.is_valid(raise_exception=True)
                if isvalid:
                    self.perform_create(serializer)
                    headers = self.get_success_headers(serializer.data)

                    totp = sample.create_otp(serializer.data["phone"])
                    loop = asyncio.new_event_loop()
                    data = loop.run_until_complete(
                        send_otp(serializer.data["phone"], totp))
                    if data:
                        return Response({"Success": "user successfuly saved.", "otp": totp}, status=status.HTTP_201_CREATED, headers=headers)
                    else:
                        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({"message": "your field is worng."}, status=status.HTTP_400_BAD_REQUEST)


class LoginCustomer(APIView):
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]

    def post(self, request):
        if 'username' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=request.data.get(
            'username'), password=request.data.get('password'))
        if user is not None and user.user_type == "CT" and user.is_register == True:
            refresh = RefreshToken.for_user(user)
            return Response({'msg': 'Login Success', 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileCustomerApi(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializerProfile

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.request.user.id)


class ActivateUserPhone(APIView):

    def post(self, request):
        if 'phone' not in request.data or 'otp' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
            print('faz1')
        user = get_object_or_404(CustomUser, phone=request.data["phone"])
        try:
            if sample.totp.verify(request.data["otp"]):

                user_obj = get_object_or_404(CustomUser, phone=user.phone)
                if user_obj.is_register:
                    return Response({'msg': 'user already registered'}, status=status.HTTP_403_FORBIDDEN)
                user_obj.is_register = True
                user_obj.save()
                return Response({'msg': 'user successfuly registered'}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': 'OTP Wrong !'}, status=status.HTTP_400_BAD_REQUEST)


class GenerateOtpForLogin(APIView):
    def post(self, request):
        if 'phone' in request.data:
            serializer = GenerateOtpLoginSerializer(data=request.data)
            isvalid = serializer.is_valid(raise_exception=True)
            if isvalid:
                user_obj = get_object_or_404(
                    CustomUser, phone=request.data["phone"])
                totp = sample.create_otp(user_obj.phone)
                loop = asyncio.new_event_loop()
                data = loop.run_until_complete(send_otp(user_obj.phone, totp))
                if data:
                    return Response({"Success": "user successfuly registered.", "otp": totp}, status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)


class GenerateOtpForActivate(APIView):
    def post(self, request):
        if 'phone' not in request.data or 'otp' not in request.data:
            return Response({'msg': 'phone required'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = GenerateOtpLoginSerializer(data=request.data)
        isvalid = serializer.is_valid(raise_exception=True)
        if isvalid:
            user_obj = get_object_or_404(
                CustomUser, phone=request.data["phone"])
            totp = sample.create_otp(user_obj.phone)
            loop = asyncio.new_event_loop()
            data = loop.run_until_complete(send_otp(user_obj.phone, totp))
            if data:
                return Response({"Success": "user successfuly registered.", "otp": totp}, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)


class LoginWithOtp(APIView):
    def post(self, request):
        if 'phone' not in request.data or 'otp' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LoginUserWithOtpSerializer(data=request.data)
        isvalid = serializer.is_valid(raise_exception=True)
        if isvalid:
            user_obj = get_object_or_404(
                CustomUser, phone=request.data["phone"])
            if user_obj and sample.totp.verify(request.data["otp"]) and user_obj.is_register==True:
                refresh = RefreshToken.for_user(user_obj)

                return Response({'msg': 'Login Success', 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'you dont hav permision to login please register your phone '}, status=status.HTTP_200_OK)

        return Response({"message": "your field is worng."}, status=status.HTTP_400_BAD_REQUEST)
