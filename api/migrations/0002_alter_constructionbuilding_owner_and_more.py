# Generated by Django 4.1.3 on 2023-10-07 20:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constructionbuilding',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='construction_list_owners', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='constructionname',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='construction_list_names', to=settings.AUTH_USER_MODEL),
        ),
    ]