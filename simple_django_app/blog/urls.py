"""URL patterns for the Blog application."""
from django.urls import path
from .views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView,
    TagCreateView,
    TagDetailView,
    TagListView,
)

app_name = "blog"

urlpatterns = [
    path("", ArticleListView.as_view(), name="root"),
    path("articles/", ArticleListView.as_view(), name="article-list"),
    path("article/<int:pk>/", ArticleDetailView.as_view(), name="article-detail"),
    path("articles/create/", ArticleCreateView.as_view(), name="article-create"),
    path("article/edit/<int:pk>/", ArticleUpdateView.as_view(), name="article-update"),
    path(
        "article/delete/<int:pk>/", ArticleDeleteView.as_view(), name="article-delete"
    ),
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/create/", TagCreateView.as_view(), name="tag-create"),
    path("tag/<slug:slug>/", TagDetailView.as_view(), name="tag-detail"),
]
