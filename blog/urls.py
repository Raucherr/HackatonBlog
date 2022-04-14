from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='My API',
        description='API of Blog App',
        default_version='v1'
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('account.urls')),
    path('api/v1/', include('comment.urls')),
    path('api/v1/', include('category.urls')),
    path('api/v1/', include('post.urls')),
    path('docs/', schema_view.with_ui('swagger'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



