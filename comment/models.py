from django.contrib.auth import get_user_model
from django.db import models

from post.models import Post

User = get_user_model()


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    comment = models.TextField()
    image = models.ImageField(upload_to='media', blank=True)
    public_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment