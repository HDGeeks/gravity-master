# Generated by Django 4.2.1 on 2023-05-05 19:42

import django.contrib.postgres.fields
from django.db import migrations, models
import location_field.models.plain


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.CharField(max_length=300)),
                ('location', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'customers',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Languages',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.CharField(max_length=300)),
                ('date', models.DateTimeField(auto_now=True)),
                ('location', models.CharField(default='', max_length=300)),
                ('noOfDataCollectors', models.IntegerField(default=0)),
                ('budget', models.FloatField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=500)),
                ('hasMultipleAnswers', models.BooleanField(default=False)),
                ('isDependent', models.BooleanField(default=False)),
                ('depQuestion', models.JSONField(null=True)),
                ('isRequired', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('CHOICE', 'CHOICE'), ('OPEN', 'OPEN'), ('MEDIA', 'MEDIA')], max_length=30)),
                ('options', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=300), null=True, size=None)),
                ('audioURL', models.URLField(null=True)),
                ('imageURL', models.URLField(null=True)),
                ('videoURL', models.URLField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('createdAt', models.DateTimeField(auto_now=True)),
                ('responses', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=300), size=None)),
                ('location', location_field.models.plain.PlainLocationField(default='', max_length=63)),
            ],
            options={
                'verbose_name_plural': 'QuestionAnswers',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('language', models.CharField(choices=[('AMHARIC', 'Amharic'), ('OROMO', 'Oromo'), ('TIGRIGNA', 'Tigrigna'), ('SOMALI', 'Somali'), ('AFAR', 'Afar')], default='Amharic', max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE')], default='', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Surveys',
            },
        ),
    ]
