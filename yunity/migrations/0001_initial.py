# -*- coding: utf-8 -*-
# Generated by Django 1.9a1 on 2015-10-02 09:57
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

import yunity.utils.models.field
import yunity.utils.elasticsearch


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='AdministrationTrait',
            fields=[
                ('_AdministrationTrait_to_BaseModel', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.BaseModel')),
            ],
            bases=('yunity.basemodel',),
        ),
        migrations.CreateModel(
            name='VersionTrait',
            fields=[
                ('_VersionTrait_to_BaseModel', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.BaseModel')),
            ],
            bases=('yunity.basemodel',),
        ),
        migrations.CreateModel(
            name='FeedbackTrait',
            fields=[
                ('_FeedbackTrait_to_BaseModel', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.BaseModel')),
            ],
            bases=('yunity.basemodel',),
        ),
        migrations.CreateModel(
            name='MapItem',
            fields=[
                ('administrationtrait_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='yunity.AdministrationTrait')),
                ('feedbacktrait_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='yunity.FeedbackTrait')),
                ('versiontrait_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.VersionTrait')),
                ('provenance', yunity.utils.models.field.MaxLengthCharField(max_length=255)),
                ('name', models.TextField()),
                ('locations', django.contrib.postgres.fields.jsonb.JSONField()),
                ('contacts', django.contrib.postgres.fields.jsonb.JSONField()),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            bases=('yunity.versiontrait', 'yunity.feedbacktrait', 'yunity.administrationtrait', yunity.utils.elasticsearch.ElasticsearchMixin),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('mapitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.MapItem')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=64, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('display_name', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('yunity.mapitem', models.Model),
            managers=[
                ('objects', yunity.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.BaseModel')),
                ('name', yunity.utils.models.field.MaxLengthCharField(max_length=255)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='yunity.Category')),
            ],
            bases=('yunity.basemodel',),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.BaseModel')),
                ('status', yunity.utils.models.field.MaxLengthCharField(max_length=255)),
                ('type', yunity.utils.models.field.MaxLengthCharField(max_length=255)),
            ],
            bases=('yunity.basemodel',),
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.BaseModel')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('type', yunity.utils.models.field.MaxLengthCharField(max_length=255)),
                ('payload', models.TextField()),
                ('caused_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interation_caused', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('yunity.basemodel',),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.BaseModel')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('type', yunity.utils.models.field.MaxLengthCharField(max_length=255)),
                ('content', models.TextField()),
                ('reply_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='yunity.Message')),
                ('sent_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('yunity.basemodel',),
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('administrationtrait_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.AdministrationTrait')),
            ],
            bases=('yunity.administrationtrait',),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('feedbacktrait_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.FeedbackTrait')),
                ('time', models.DateTimeField(null=True)),
                ('status', yunity.utils.models.field.MaxLengthCharField(max_length=255)),
            ],
            bases=('yunity.feedbacktrait',),
        ),
        migrations.AddField(
            model_name='versiontrait',
            name='next_version',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='previous_version', to='yunity.VersionTrait'),
        ),
        migrations.AddField(
            model_name='interaction',
            name='changed',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='yunity.VersionTrait'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='about',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='yunity.FeedbackTrait'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='arbitrated_by',
            field=models.ManyToManyField(related_name='feedback_arbitrators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='feedback',
            name='provided_by',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_provider', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='administrationtrait',
            name='administrated_by',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ArbitrationLog',
            fields=[
                ('conversation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.Conversation')),
                ('target', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='yunity.Feedback')),
            ],
            bases=('yunity.conversation',),
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('conversation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.Conversation')),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            bases=('yunity.conversation',),
        ),
        migrations.CreateModel(
            name='Opportunity',
            fields=[
                ('mapitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.MapItem')),
            ],
            bases=('yunity.mapitem',),
        ),
        migrations.CreateModel(
            name='Participate',
            fields=[
                ('request_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.Request')),
                ('type', yunity.utils.models.field.MaxLengthCharField(max_length=255)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yunity.Opportunity')),
            ],
            bases=('yunity.request',),
        ),
        migrations.CreateModel(
            name='Take',
            fields=[
                ('request_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.Request')),
            ],
            bases=('yunity.request',),
        ),
        migrations.CreateModel(
            name='Valuable',
            fields=[
                ('mapitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.MapItem')),
            ],
            bases=('yunity.mapitem',),
        ),
        migrations.CreateModel(
            name='Wall',
            fields=[
                ('conversation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yunity.Conversation')),
            ],
            bases=('yunity.conversation',),
        ),
        migrations.AddField(
            model_name='request',
            name='requested_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='in_conversation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='yunity.Conversation'),
        ),
        migrations.AddField(
            model_name='mapitem',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yunity.Category'),
        ),
        migrations.AddField(
            model_name='wall',
            name='target',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='yunity.MapItem'),
        ),
        migrations.AddField(
            model_name='take',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yunity.Valuable'),
        ),
    ]
