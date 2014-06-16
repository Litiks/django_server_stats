# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PageViewLog.view_name'
        db.add_column('server_stats_pageviewlog', 'view_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'PageViewLog.status_code'
        db.add_column('server_stats_pageviewlog', 'status_code',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PageViewLog.ip'
        db.add_column('server_stats_pageviewlog', 'ip',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20),
                      keep_default=False)


        # Changing field 'PageViewLog.gen_time'
        db.alter_column('server_stats_pageviewlog', 'gen_time', self.gf('django.db.models.fields.BigIntegerField')(null=True))

    def backwards(self, orm):
        # Deleting field 'PageViewLog.view_name'
        db.delete_column('server_stats_pageviewlog', 'view_name')

        # Deleting field 'PageViewLog.status_code'
        db.delete_column('server_stats_pageviewlog', 'status_code')

        # Deleting field 'PageViewLog.ip'
        db.delete_column('server_stats_pageviewlog', 'ip')


        # Changing field 'PageViewLog.gen_time'
        db.alter_column('server_stats_pageviewlog', 'gen_time', self.gf('django.db.models.fields.IntegerField')(null=True))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'server_stats.benchmarkmilestone': {
            'Meta': {'object_name': 'BenchmarkMilestone'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'server_stats.pageviewlog': {
            'Meta': {'object_name': 'PageViewLog'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gen_time': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'status_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'view_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'server_stats.querystat': {
            'Meta': {'object_name': 'QueryStat'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'queries': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['server_stats']