# Generated by Django 2.1.1 on 2019-07-09 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SampleManage', '0011_auto_20190628_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetectMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('methodname', models.CharField(max_length=50)),
                ('algorithm', models.CharField(max_length=50)),
                ('paramvalue', models.CharField(max_length=3000)),
                ('path', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'detectmethod',
            },
        ),
    ]
