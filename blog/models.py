from django.db import models

# Create your models here.


class Article(models.Model):
    slug = models.SlugField(unique=True, max_length=100, primary_key=True)
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    body = models.TextField()

    def save(self, force_insert=False, force_update=False):
        super().save(force_insert, force_update)

        # PING GOOGLE

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

    article_slug = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.content[:100]
