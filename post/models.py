
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# class Category(models.Model):
#     title = models.CharField(max_length=100, unique=True)
#
#     def __str__(self):
#         return self.title


class Post(models.Model):
    title = models.TextField()
    img = models.ImageField(upload_to='')
    description = models.TextField()
    public_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title