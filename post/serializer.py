from rest_framework import serializers

from comment.models import Comment
from comment.serializer import CommentSerializer
from post.models import Post, PostImage


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = ('image', )

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['image'] = self._get_image_url(instance)
        return rep


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author_id'] = request.user.id
        post = Post.objects.create(**validated_data)
        return post

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['author'] = instance.author.email
        rep['comments'] = CommentSerializer(Comment.objects.filter(post=instance.id), many=True).data
        return rep