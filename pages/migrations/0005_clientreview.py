import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_fleet_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=150)),
                ('client_title', models.CharField(blank=True, max_length=150)),
                ('review', models.TextField()),
                ('rating', models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('image', models.ImageField(blank=True, null=True, upload_to='reviews/')),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['order', '-created_at'],
            },
        ),
    ]
