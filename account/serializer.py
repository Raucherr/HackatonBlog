from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from .models import Profile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirmation = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirmation')

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():  # objects из setting.py
            raise serializers.ValidationError('User already exists')
        return email

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirmation = validated_data.get('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError("passwords error")
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User.objects.create_user(email, password)
        profile = Profile.objects.create(user_id=user.id)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.pop('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            if not user:
                msg = 'No login with provided credentials'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = "no password or email"
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def create_new_password(self):
        from django.utils.crypto import get_random_string
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        random_password = get_random_string(8)
        user.set_password(random_password)
        user.send_new_password(random_password)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Укажите верный пароль')
        return old_password

    def validate(self, attrs):
        password1 = attrs.get('new_password')
        password2 = attrs.get('password_confirm')
        if password1 != password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def set_new_password(self):
        user = self.context['request'].user
        password =self.validated_data.get('new_password')
        user.set_password(password)