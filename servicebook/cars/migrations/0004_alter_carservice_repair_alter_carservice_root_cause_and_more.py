# Generated by Django 4.1.4 on 2022-12-13 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_alter_carinfo_brand_alter_carservice_repair_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carservice',
            name='repair',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='carservice',
            name='root_cause',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='carservice',
            name='symptoms',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]
