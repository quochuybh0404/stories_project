# Generated by Django 4.1 on 2022-11-02 11:58

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stories',
            name='viewed',
        ),
        migrations.AlterField(
            model_name='stories',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
    ]
