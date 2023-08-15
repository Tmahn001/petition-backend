# Generated by Django 4.2.4 on 2023-08-14 11:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_signature_signer_signature_signer_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='signature',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]