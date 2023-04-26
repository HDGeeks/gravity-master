# Generated by Django 4.0.5 on 2022-07-22 11:04

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.CharField(max_length=300)),
                ('location', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.CharField(max_length=300)),
                ('date', models.DateTimeField(auto_now=True)),
                ('location', models.CharField(default='', max_length=300)),
                ('noOfDataCollectors', models.IntegerField(default=0)),
                ('budget', models.FloatField(default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE')], default='', max_length=100)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.project')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('hasMultipleAnswers', models.BooleanField(default=False)),
                ('isRequired', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('CHOICE', 'CHOICE'), ('OPEN', 'OPEN')], max_length=30)),
                ('options', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=300), null=True, size=None)),
                ('audioURL', models.URLField(null=True)),
                ('imageURL', models.URLField(null=True)),
                ('videoURL', models.URLField(null=True)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.survey')),
            ],
        ),
    ]
