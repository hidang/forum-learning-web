# Generated by Django 3.2.8 on 2021-10-28 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_alter_question_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
