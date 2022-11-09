from django.contrib import admin

# Register your models here.

from .models import Announce, PostImage


class PostImageAdmin(admin.StackedInline):
    model = PostImage


@admin.register(Announce)
class AnnounceAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin]

    class Meta:
        model = Announce


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass
