# Generated by Django 4.2.4 on 2023-08-28 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_category_name_remove_post_categories_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.CharField(default='General', max_length=200),
        ),
    ]
