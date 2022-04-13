# Generated by Django 4.0.1 on 2022-04-13 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directorate', '0004_articles'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.TextField(blank=True, null=True)),
                ('caption', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'posts',
                'managed': False,
            },
        ),
    ]
