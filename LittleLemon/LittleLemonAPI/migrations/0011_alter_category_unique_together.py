# Generated by Django 4.2.14 on 2024-07-19 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0010_alter_category_slug'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('slug', 'title')},
        ),
    ]