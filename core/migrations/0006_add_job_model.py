# Migration: add Job model
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0005_course_brochure_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('company', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200, blank=True)),
                ('description', models.TextField(blank=True)),
                ('apply_link', models.URLField(blank=True)),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('is_remote', models.BooleanField(default=False)),
            ],
        ),
    ]
