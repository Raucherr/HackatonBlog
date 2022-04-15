
from django.contrib.auth import get_user_model
from django.db import models

from account.models import User
from category.models import Category


class Post(models.Model):
    title = models.TextField()
    category = models.ForeignKey(Category, null=True,
                                 on_delete=models.CASCADE,
                                 related_name='post')
    description = models.TextField()
    img = models.ImageField(blank=True, upload_to='post_photo')
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
