# Generated by Django 4.1 on 2022-09-22 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allRentals', '0010_remove_userfeedback_avg_score_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='total_rating_score',
            field=models.IntegerField(default=5),
        ),
    ]