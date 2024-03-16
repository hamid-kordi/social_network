from django.contrib import admin
from .models import Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("created", "user", "slug")
    search_fields = ("user", "slug")
    prepopulated_fields = {"slug": ("body",)}
    list_filter = ("update", "created")
    raw_id_fields = ("user",)


#admin.site.register(Post, PostAdmin) or  @admin.register(Post)
