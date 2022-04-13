# Generated by Django 4.0.4 on 2022-04-13 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('img', models.ImageField(upload_to='')),
                ('description', models.TextField()),
                ('public_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
