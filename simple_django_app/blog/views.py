"""
Views for our blog application.

It's not uncommon to refactor this module into a subpackage when the
number of views increases. In this case, I could have made a `views/`
subpackage with two modules, `article.py` and `tag.py`, to create a
bit of structure. Since we only have a few, short view classes, I've
kept them together for now.
"""
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django.views.generic.list import ListView

from .models import Article, Tag


class ArticleListView(ListView):
    """A list of all articles."""

    model = Article
    context_object_name = "articles"


class ArticleDetailView(DetailView):
    """A detail view of a single article."""

    model = Article
    context_object_name = "article"


class ArticleCreateView(CreateView):
    """A simple view to create an article."""

    model = Article
    fields = ["title", "body", "tags"]
    context_object_name = "article"


class ArticleUpdateView(UpdateView):
    """A simple view to create an article."""

    model = Article
    fields = ["title", "body", "tags"]
    context_object_name = "article"


class ArticleDeleteView(DeleteView):
    """A simple view to create an article."""

    model = Article
    success_url = reverse_lazy("blog:article-list")


class TagListView(ListView):
    """A list of all tags with their article counts."""

    model = Tag
    context_object_name = "tags"


class TagDetailView(DetailView):
    """A detail view of a single tag listing all articles tagged with it."""

    model = Tag
    context_object_name = "tag"


class TagCreateView(CreateView):
    """A simple view to create an tag."""

    model = Tag
    fields = ["slug"]
