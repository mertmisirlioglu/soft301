# Generated by Django 2.2.1 on 2020-01-15 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='type',
        ),
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('C', 'Concert'), ('T', 'Theatre'), ('S', 'Sports')], default='C', max_length=1),
            preserve_default=False,
        ),
    ]
