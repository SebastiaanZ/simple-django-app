"""
Register models to make them accessible from the admin view.

You can visit the admin view at `/admin/`.
"""
from django.contrib import admin

from simple_django_app.blog.models import Article, Tag

admin.site.register(Article)
admin.site.register(Tag)
