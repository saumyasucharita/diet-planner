# Generated by Django 4.2.3 on 2023-08-10 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_dietplan_carbs_alter_dietplan_fat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dietplan',
            name='diet_plan_name',
        ),
        migrations.AddField(
            model_name='dietplan',
            name='image',
            field=models.URLField(null=True),
        ),
    ]