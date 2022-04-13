from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from .models import Profile
from .utils import send_activation_email

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirmation = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirmation')

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User already exist')
        return email

    def validate(self, validation_data):
        password = validation_data.get('password')
        password_confirmation = validation_data.pop('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Password Error')
        return validation_data

    def create(self, validated_data):
        # print(validated_data)
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User.objects.create_user(email, password)
        send_activation_email(user.email, user.activation_code)
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, validated_data):
        print(validated_data)
        email = validated_data.get('email')
        password = validated_data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)

            if not user:
                msg = 'No login with provided credentials'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'No "password" or "Email"'
            raise serializers.ValidationError(msg, code='authoriazation')

        validated_data['user'] = user
        return validated_data


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author_id'] = request.user.id
        profile = Profile.objects.create(**validated_data)
        return profile

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['favorite'] = f'{[i.title for i in instance.favorite.all()]}'
        return rep