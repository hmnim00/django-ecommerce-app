# Generated by Django 3.2.5 on 2021-07-13 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('xbox', 'Xbox'), ('playstation', 'Playstation'), ('nintendo', 'Nintendo'), ('otro', 'Otro')], default='otro', max_length=54),
        ),
    ]