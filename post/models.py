
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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    public_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    product = models.ForeignKey(Post, on_delete=models.CASCADE,
                                related_name='image')
    image = models.ImageField(upload_to='products_photo')

    def __str__(self):
        return self.product.title