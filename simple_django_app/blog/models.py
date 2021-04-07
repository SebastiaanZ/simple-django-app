"""Models for our blog application."""
from django.core import validators
from django.db import models
from django.urls import reverse


class Tag(models.Model):
    """Tags to classify and categorize articles."""

    slug = models.SlugField(max_length=64, unique=True, verbose_name="name")

    def __str__(self) -> str:
        """Return the string representation of this Tag."""
        return str(self.slug)

    def get_absolute_url(self) -> str:
        """Get the absolute URL for this article."""
        return reverse("blog:tag-detail", kwargs={"slug": self.slug})


class Article(models.Model):
    """An article for our simple blog."""

    title = models.CharField(
        max_length=128,
        validators=[
            validators.MinLengthValidator(1, message="titles cannot be empty!")
        ],
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    body = models.TextField(help_text="The main body for this blog post.")
    tags = models.ManyToManyField(
        Tag,
        related_name="articles",
        blank=True,
    )

    def __str__(self) -> str:
        """Return a string representation of this article."""
        return str(self.title)

    def get_absolute_url(self) -> str:
        """Get the absolute URL for this article."""
        return reverse("blog:article-detail", kwargs={"pk": self.pk})
