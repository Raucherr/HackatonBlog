from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models


class MyUserManager(BaseUserManager):
    # use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        # user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    user = None
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['__all__']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj):
        return self.is_staff

    @staticmethod
    def generate_activation_code():
        from django.utils.crypto import get_random_string
        code = get_random_string(8)
        return code

    def set_activation_code(self):
        code = self.generate_activation_code()
        if MyUser.objects.filter(activation_code=code).exists():
            self.set_activation_code()
        else:
            self.activation_code = code
            self.save()

    def send_activation_mail(self):
        message = f"""
        Здравствуйте! Спасибо за регистрацию на нашем сайте!
        Ваш код активации: {self.activation_code}
        """
        send_mail(
            "Подтверждение аккаунта",
            message,
            "test@gmail.com",
            [self.email]
        )

    def send_new_password(self, new_password):
        message = f'Ваш новый пароль: {new_password}'
        send_mail(
            'Восстановление пароля',
            message,
            'test@gmail.com',
            [self.email]
        )

class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, blank=True, null=True)
    photo = models.ImageField(upload_to='users_photo', blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user