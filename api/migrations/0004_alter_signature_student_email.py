# Generated by Django 4.2.4 on 2023-08-14 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_petition_id_alter_signature_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signature',
            name='student_email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]