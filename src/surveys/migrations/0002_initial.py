# Generated by Django 4.2 on 2023-05-02 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='dataCollectors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='survey',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.project'),
        ),
        migrations.AddField(
            model_name='questionanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.question'),
        ),
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='surveys.category'),
        ),
        migrations.AddField(
            model_name='question',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='surveys.language'),
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.survey'),
        ),
        migrations.AddField(
            model_name='project',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.customer'),
        ),
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['name'], name='customer_name_idx'),
        ),
        migrations.AddIndex(
            model_name='survey',
            index=models.Index(fields=['name'], name='project'),
        ),
        migrations.AddIndex(
            model_name='survey',
            index=models.Index(fields=['project'], name='project_id_idx'),
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['title'], name='title_idx'),
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['survey'], name='survey_id_idx'),
        ),
    ]
