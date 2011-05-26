# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Campaign'
        db.create_table('rewards_campaign', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('designator', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=28, unique=True, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('commission', self.gf('django.db.models.fields.FloatField')(default=0.10000000000000001)),
        ))
        db.send_create_signal('rewards', ['Campaign'])

        # Adding model 'Inflow'
        db.create_table('rewards_inflow', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('campaign_designator', self.gf('django.db.models.fields.CharField')(max_length=28, db_index=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('referrer', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('rewards', ['Inflow'])

        # Adding model 'Conversion'
        db.create_table('rewards_conversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rewards.Campaign'], to_field='designator')),
            ('value', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(default='', max_length=64, db_index=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('referrer', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.CharField')(default='created', max_length=32)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('rewards', ['Conversion'])


    def backwards(self, orm):
        
        # Deleting model 'Campaign'
        db.delete_table('rewards_campaign')

        # Deleting model 'Inflow'
        db.delete_table('rewards_inflow')

        # Deleting model 'Conversion'
        db.delete_table('rewards_conversion')


    models = {
        'rewards.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'commission': ('django.db.models.fields.FloatField', [], {'default': '0.10000000000000001'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'designator': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '28', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['rewards']
