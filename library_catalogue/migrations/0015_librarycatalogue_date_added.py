# Generated by Django 4.2.7 on 2024-06-04 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_catalogue', '0014_alter_usercatalogue_date_returned'),
    ]

    operations = [
        migrations.AddField(
            model_name='librarycatalogue',
            name='date_added',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
