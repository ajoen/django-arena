# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ForumCategory'
        db.create_table(u'arena_forumcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=146)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=3)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'arena', ['ForumCategory'])

        # Adding model 'Forum'
        db.create_table(u'arena_forum', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forums', to=orm['arena.ForumCategory'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=146)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=3)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='U', max_length=1)),
        ))
        db.send_create_signal(u'arena', ['Forum'])

        # Adding model 'ForumThread'
        db.create_table(u'arena_forumthread', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forum_threads', to=orm['arena.Forum'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forum_threads', to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('last_post_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
            ('thread_type', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
        ))
        db.send_create_signal(u'arena', ['ForumThread'])

        # Adding model 'ForumPost'
        db.create_table(u'arena_forumpost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forum_thread', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forum_posts', to=orm['arena.ForumThread'])),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forum_posts', to=orm['auth.User'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
        ))
        db.send_create_signal(u'arena', ['ForumPost'])

        # Adding model 'ForumThreadHit'
        db.create_table(u'arena_forumthreadhit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('visitor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('forum_thread', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hits', to=orm['arena.ForumThread'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'arena', ['ForumThreadHit'])


    def backwards(self, orm):
        # Deleting model 'ForumCategory'
        db.delete_table(u'arena_forumcategory')

        # Deleting model 'Forum'
        db.delete_table(u'arena_forum')

        # Deleting model 'ForumThread'
        db.delete_table(u'arena_forumthread')

        # Deleting model 'ForumPost'
        db.delete_table(u'arena_forumpost')

        # Deleting model 'ForumThreadHit'
        db.delete_table(u'arena_forumthreadhit')


    models = {
        u'arena.forum': {
            'Meta': {'object_name': 'Forum'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forums'", 'to': u"orm['arena.ForumCategory']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '146'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'arena.forumcategory': {
            'Meta': {'ordering': "['order']", 'object_name': 'ForumCategory'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '146'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'arena.forumpost': {
            'Meta': {'object_name': 'ForumPost'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'forum_thread': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forum_posts'", 'to': u"orm['arena.ForumThread']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forum_posts'", 'to': u"orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'arena.forumthread': {
            'Meta': {'ordering': "['-last_post_date']", 'object_name': 'ForumThread'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forum_threads'", 'to': u"orm['auth.User']"}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forum_threads'", 'to': u"orm['arena.Forum']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_post_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'thread_type': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'visitors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'visited_forum_threads'", 'symmetrical': 'False', 'through': u"orm['arena.ForumThreadHit']", 'to': u"orm['auth.User']"})
        },
        u'arena.forumthreadhit': {
            'Meta': {'object_name': 'ForumThreadHit'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'forum_thread': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hits'", 'to': u"orm['arena.ForumThread']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'visitor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['arena']