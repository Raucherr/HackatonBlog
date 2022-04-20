from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from post.models import Post
from post.permissions import IsPostAuthor
from post.serializer import PostSerializer
from django.db.models import Q
from rest_framework.decorators import action
#import django_filters

#class PostFilter(django_filters.FilterSet):
#    title = django_filters.CharFilter(lookup_expr='iexact')
#    description = django_filters.CharFilter(lookup_expr='iexact')

#    class Meta:
#        model = Post
#        fields = ['title', 'description']

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter, filters.DjangoFilterBackend]
    search_fields = ('title', 'description')

    @action(detail=False, methods=['get'])              #action decorator is available ONLY with viewsets
    def search(self, request, pk=None):                 #router builds path posts/search/?q=paris
        # print(request.query_params)
        q = request.query_params.get('q')               #<----=----->request.GET
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if self.action == 'list':
            serializer_class = PostSerializer
        return serializer_class

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsPostAuthor()]
        return []

    @action(detail=False, methods=['get'])
    def my_posts(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(email=request.user.email)
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
