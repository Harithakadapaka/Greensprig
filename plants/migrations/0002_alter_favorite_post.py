# Generated by Django 4.2.21 on 2025-06-24 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("plants", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="favorite",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorites",
                to="plants.post",
            ),
        ),
    ]
