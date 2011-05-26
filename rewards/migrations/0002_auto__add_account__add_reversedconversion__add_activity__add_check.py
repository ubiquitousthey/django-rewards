# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Account'
        db.create_table('rewards_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=2)),
            ('updated_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('rewards', ['Account'])

        # Adding model 'ReversedConversion'
        db.create_table('rewards_reversedconversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('original_conversion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rewards.Conversion'])),
        ))
        db.send_create_signal('rewards', ['ReversedConversion'])

        # Adding model 'Activity'
        db.create_table('rewards_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rewards.Account'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=2)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('reference', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('rewards', ['Activity'])

        # Adding model 'Check'
        db.create_table('rewards_check', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('payee', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('rewards', ['Check'])


    def backwards(self, orm):
        
        # Deleting model 'Account'
        db.delete_table('rewards_account')

        # Deleting model 'ReversedConversion'
        db.delete_table('rewards_reversedconversion')

        # Deleting model 'Activity'
        db.delete_table('rewards_activity')

        # Deleting model 'Check'
        db.delete_table('rewards_check')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'rewards.account': {
            'Meta': {'object_name': 'Account'},
            'balance': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'rewards.activity': {
            'Meta': {'object_name': 'Activity'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rewards.Account']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '2'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference': ('django.db.models.fields.IntegerField', [], {})
        },
        'rewards.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'commission': ('django.db.models.fields.FloatField', [], {'default': '0.10000000000000001'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'designator': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '28', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'rewards.check': {
            'Meta': {'object_name': 'Check'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'payee': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'rewards.conversion': {
            'Meta': {'object_name': 'Conversion'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rewards.Campaign']", 'to_field': "'designator'"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'reference': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'db_index': 'True', 'blank': 'True'}),
            'referrer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'created'", 'max_length': '32'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'rewards.inflow': {
            'Meta': {'object_name': 'Inflow'},
            'campaign_designator': ('django.db.models.fields.CharField', [], {'max_length': '28', 'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'referrer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'rewards.reversedconversion': {
            'Meta': {'object_name': 'ReversedConversion'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_conversion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rewards.Conversion']"})
        }
    }

    complete_apps = ['rewards']
