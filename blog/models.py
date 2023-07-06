from django.db import models
from django.utils.text import slugify
from django.contrib.sitemaps import ping_google
from django.utils import timezone

from datetime import datetime
# Create your models here.


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True, default='NULL')
    name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Article(models.Model):
    slug = models.SlugField(unique=True, max_length=100, primary_key=True)
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        self.modified = datetime.now(tz=timezone.utc)
        super(Article, self).save(*args, **kwargs)

        try:
            ping_google('/sitemap.xml')
        except Exception as e:
            pass

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/post/{self.slug}'


class Message(models.Model):
    text = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.date)


class Generator(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    running = models.BooleanField(default=False)

    def __str__(self):
        return self.content[:100]
