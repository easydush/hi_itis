# Generated by Django 4.1.6 on 2023-02-14 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_teacherprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherprofile',
            name='teacher',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.teacher'),
            preserve_default=False,
        ),
    ]