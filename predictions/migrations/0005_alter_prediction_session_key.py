# Generated by Django 5.2.3 on 2025-07-06 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0004_alter_prediction_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prediction',
            name='session_key',
            field=models.CharField(blank=True, db_index=True, default='', help_text='Django session key to enforce one prediction per session', max_length=40),
        ),
    ]
