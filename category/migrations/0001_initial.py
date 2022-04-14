# Generated by Django 4.0.4 on 2022-04-14 05:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='category.category')),
            ],
        ),
    ]
