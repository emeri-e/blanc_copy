# Generated by Django 4.2.11 on 2024-03-23 22:38

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bitgo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank_Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('acc_no', models.CharField(max_length=50)),
                ('bank', models.CharField(choices=[('044', 'Access Bank'), ('058', 'GTBank')], default='044', max_length=3)),
                ('is_default', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('dark_mode', models.BooleanField(default=False)),
                ('use_biometrics', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
                ('status', models.CharField(choices=[(None, 'PENDING'), ('complete', 'COMPLETE'), ('pending', 'PENDING'), ('failed', 'FAILED')], default='pending', max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('bank_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='withdrawals', to='dashboard.bank_account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-timestamp', '-id'),
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to='dashboard.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='dashboard.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('canceled', 'canceled'), ('complete', 'complete'), ('failed', 'failed')], default='pending', max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('transaction_id', models.CharField(max_length=100, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('is_withdrawn', models.BooleanField(default=False)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='bitgo.address')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddField(
            model_name='bank_account',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_accounts', to='dashboard.profile'),
        ),
    ]