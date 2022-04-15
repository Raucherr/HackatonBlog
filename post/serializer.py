from rest_framework import serializers
from category.serializers import CategorySerializer
from post.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def _get_image_url(self, instance):
        request = self.context.get('request')
        if instance.img:
            url = instance.img.url
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = User.objects.get(id=request.user.id)
        post = Post.objects.create(**validated_data)
        return post

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['author'] = instance.author.email
        representation['img'] = self._get_image_url(instance)
        return representation
