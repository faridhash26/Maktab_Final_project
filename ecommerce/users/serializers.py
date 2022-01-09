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





class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class UpdateProfileSerilizer(serializers.ModelSerializer):

    class Meta:
        models=CustomUser
        fields= ['id', 'username' ,"phone" , "address" ,"city" ,"zip","image" ]