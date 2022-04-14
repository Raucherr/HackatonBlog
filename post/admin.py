# from django.contrib import admin
# from .models import Post
#
# admin.site.register(Post)


from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, PostImage


class InlinePostImage(admin.TabularInline):
    model = PostImage
    extra = 1
    fields = ['image', ]


class PostAdminDisplay(admin.ModelAdmin):
    inlines = [InlinePostImage, ]
    list_display = ('title',  'image')

    def image(self, obj):
        img = obj.image.first()
        if img:
            return mark_safe(f'<img src="{img.image.url}" width="80" height="20" style="object-fit: contain" />')
        else:
            return ""


admin.site.register(Post, PostAdminDisplay)