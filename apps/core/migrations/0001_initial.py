# Generated by Django 4.2.3 on 2023-08-08 00:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DietPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_name', models.CharField(max_length=127)),
                ('calories', models.IntegerField(null=True)),
                ('protein', models.IntegerField(null=True)),
                ('fat', models.IntegerField(null=True)),
                ('carbs', models.IntegerField(null=True)),
                ('diet_plan_name', models.CharField(max_length=127)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
