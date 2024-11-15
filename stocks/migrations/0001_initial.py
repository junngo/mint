# Generated by Django 5.1.1 on 2024-11-14 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('market_type', models.CharField(choices=[('KOSPI', 'KOSPI'), ('KOSDAQ', 'KOSDAQ')], max_length=10)),
                ('isin_code', models.CharField(blank=True, max_length=20, null=True)),
                ('group_code', models.CharField(blank=True, max_length=10, null=True)),
                ('listing_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'stock',
            },
        ),
    ]
