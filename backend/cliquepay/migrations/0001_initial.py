# Generated by Django 5.2 on 2025-04-08 17:11

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=128, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('photo_url', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'groups',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False, unique=True)),
                ('cognito_id', models.CharField(max_length=255, unique=True)),
                ('full_name', models.CharField(default='Unnamed User', help_text="User's full name (required)", max_length=150)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, help_text='Optional phone number in international format', max_length=16, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('avatar_url', models.URLField(blank=True, default='https://storage.cloud.google.com/cliquepay_profile_photo_bucket/Default_pfp.jpg')),
                ('currency', models.CharField(default='USD', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'users',
                'indexes': [models.Index(fields=['name'], name='username_idx'), models.Index(fields=['full_name'], name='full_name_idx'), models.Index(fields=['email'], name='email_idx')],
            },
        ),
        migrations.CreateModel(
            name='GroupMessage',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=128, primary_key=True, serialize=False, unique=True)),
                ('content', models.TextField()),
                ('message_type', models.CharField(choices=[('TEXT', 'Text'), ('FILE', 'File'), ('IMAGE', 'Image')], default='TEXT', max_length=5)),
                ('file_url', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='cliquepay.group')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_group_messages', to='cliquepay.user')),
            ],
            options={
                'db_table': 'group_messages',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='GroupInvitation',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=128, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accepted_at', models.DateTimeField(blank=True, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='cliquepay.group')),
                ('invited_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_group_invitations', to='cliquepay.user')),
                ('invited_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_invitations', to='cliquepay.user')),
            ],
            options={
                'db_table': 'group_invitations',
            },
        ),
        migrations.AddField(
            model_name='group',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_groups', to='cliquepay.user'),
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False, unique=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('remaining_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('receipt_url', models.URLField(blank=True, null=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='cliquepay.group')),
                ('friend', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='cliquepay.user')),
                ('paid_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses_paid', to='cliquepay.user')),
            ],
            options={
                'db_table': 'expenses',
            },
        ),
        migrations.CreateModel(
            name='DirectMessage',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=128, primary_key=True, serialize=False, unique=True)),
                ('content', models.TextField()),
                ('message_type', models.CharField(choices=[('TEXT', 'Text'), ('FILE', 'File'), ('IMAGE', 'Image')], default='TEXT', max_length=5)),
                ('file_url', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_read', models.BooleanField(default=False)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='cliquepay.user')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_direct_messages', to='cliquepay.user')),
            ],
            options={
                'db_table': 'direct_messages',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='GroupReadReceipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_receipts', to='cliquepay.group')),
                ('last_read_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_receipts', to='cliquepay.groupmessage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_receipts', to='cliquepay.user')),
            ],
            options={
                'db_table': 'group_read_receipts',
                'ordering': ['-last_read_message__created_at'],
                'unique_together': {('user', 'group')},
            },
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('member', 'Member')], default='member', max_length=10)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='cliquepay.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_memberships', to='cliquepay.user')),
            ],
            options={
                'db_table': 'group_members',
                'constraints': [models.UniqueConstraint(fields=('user', 'group'), name='unique_group_membership')],
            },
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=128, primary_key=True, serialize=False, unique=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('blocked', 'Blocked')], default='pending', max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('action_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendship_actions', to='cliquepay.user')),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1_friendships', to='cliquepay.user')),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2_friendships', to='cliquepay.user')),
            ],
            options={
                'db_table': 'friendships',
                'constraints': [models.UniqueConstraint(fields=('user1', 'user2'), name='unique_friendship'), models.CheckConstraint(condition=models.Q(('user1__lt', models.F('user2'))), name='force_user_order')],
            },
        ),
        migrations.CreateModel(
            name='ExpenseSplit',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False, unique=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('remaining_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='splits', to='cliquepay.expense')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_splits', to='cliquepay.user')),
            ],
            options={
                'db_table': 'expense_splits',
                'unique_together': {('expense', 'user')},
            },
        ),
    ]
