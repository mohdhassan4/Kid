# Generated by Django 3.0.8 on 2021-04-09 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_course_date_enrolled'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='zoom_link',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]