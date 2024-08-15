# Generated by Django 5.1 on 2024-08-15 07:45

import apps.tasks.choices.statuses
import apps.tasks.utils.set_end_of_month
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_projectfile_project_files'),
        ('tasks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=apps.tasks.choices.statuses.Statuses.choices, default=apps.tasks.choices.statuses.Statuses['NEW'], max_length=15)),
                ('priority', models.SmallIntegerField(choices=[(1, 'Very Low'), (2, 'Low'), (3, 'Medium'), (4, 'High'), (5, 'Critical')], default=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deadline', models.DateTimeField(default=apps.tasks.utils.set_end_of_month.calculate_end_of_month)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projects.project')),
                ('tags', models.ManyToManyField(related_name='tasks', to='tasks.tag')),
            ],
            options={
                'ordering': ['-deadline'],
                'unique_together': {('name', 'project')},
            },
        ),
    ]