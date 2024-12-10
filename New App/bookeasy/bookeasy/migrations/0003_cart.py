# Generated by Django 5.1.3 on 2024-12-05 06:49

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookeasy', '0002_book_cart_it'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('book_name', models.CharField(blank=True, editable=False, max_length=255)),
                ('book_image', models.ImageField(blank=True, editable=False, null=True, upload_to='cart_book_images/')),
                ('price_at_addition', models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=10)),
                ('books_available', models.PositiveIntegerField(default=0, editable=False)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('cart_book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='bookeasy.book')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]