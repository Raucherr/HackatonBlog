
from django.contrib.auth import get_user_model
from django.db import models

from account.models import User

class Post(models.Model):
    title = models.TextField()
    description = models.TextField()
    img = models.ImageField(blank=True, upload_to='post_photo')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.title

