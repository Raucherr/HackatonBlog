from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
#
# from .models import Profile
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


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    activation_code = serializers.CharField(min_length=8)

    def validate(self, attrs):
        email = attrs.get('email')
        activation_code = attrs.get('activation_code')

        if not User.objects.filter(email=email, activation_code=activation_code).exists():
            raise serializers.ValidationError('Пользователь не найден!')
        return attrs

    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.pop('password')
        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError('Неверный пароль')
        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        return attrs


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
        password = self.validated_data.get('new_password')
        user.set_password(password)


# class ProfileSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Profile
#         fields = '__all__'
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         validated_data['user'] = User.objects.get(id=request.user.id)
#         profile = Profile.objects.create(**validated_data)
#         return profile
#
#     def to_representation(self, instance):
#         rep = super().to_representation(instance)
#         # rep['favorite'] = f'{[i.title for i in instance.favorite.all()]}'
#         return rep