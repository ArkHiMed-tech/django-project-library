# Generated by Django 5.1.1 on 2024-09-14 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_remove_book_path_book_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
