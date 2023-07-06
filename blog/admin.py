from django.contrib import admin, messages
from django.http import HttpRequest

from threading import Thread
import asyncio

from django_object_actions import DjangoObjectActions, action

from .models import Article, Message, Generator
from .openai_handler import generate


# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = "date"
    empty_value_display = "-empty-"
    readonly_fields = ('date', 'timestamp', 'modified')
    list_display = ['title', 'timestamp']
    ordering = ['-timestamp']


async def generate_article(object: Generator):
    object.running = True
    await object.asave()

    article = await generate(object.content)

    object.running = False
    object.used = True
    await object.asave()

    object.article_slug = article.slug if article else 'invalid'
    await object.asave()



def thread_function(object: Generator):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(generate_article(object))
    loop.close()


@admin.register(Generator)
class GeneratorAdmin(DjangoObjectActions, admin.ModelAdmin):
    date_hierarchy = "date"
    empty_value_display = "-empty-"
    readonly_fields = ('date', 'used', 'running', 'article_slug')
    list_display = ['content', 'running', 'used']

    @action(label='Generate', description='Prompt GPT to generate an article.')
    def generate(self, request: HttpRequest, obj: Generator):
        if obj.used:
            messages.warning(request, 'This prompt has already been used.')
            return

        if obj.running:
            messages.warning(request, 'This prompt is already running.')
            return

        thread = Thread(target=thread_function, args=[obj], daemon=True)
        thread.start()

        messages.success(request, 'The generator has started.')

    change_actions = ['generate']


admin.site.register(Message)
