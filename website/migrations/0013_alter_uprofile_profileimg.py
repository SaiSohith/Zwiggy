# Generated by Django 3.2 on 2021-05-18 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_orderfood_rest_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uprofile',
            name='profileimg',
            field=models.ImageField(default='media\\profileimgs\\defaultpimg.jpg', upload_to='profileimgs/'),
        ),
    ]