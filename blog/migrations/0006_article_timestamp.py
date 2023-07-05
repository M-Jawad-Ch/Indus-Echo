# Generated by Django 4.2.3 on 2023-07-05 13:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_article_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
