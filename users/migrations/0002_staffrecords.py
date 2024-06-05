# Generated by Django 4.2.7 on 2024-05-31 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffRecords',
            fields=[
                ('staff_record_id', models.AutoField(primary_key=True, serialize=False)),
                ('qualification', models.CharField(max_length=255)),
                ('experience', models.TextField()),
                ('skill_set', models.TextField()),
                ('grade', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'staff_records',
                'managed': True,
            },
        ),
    ]
