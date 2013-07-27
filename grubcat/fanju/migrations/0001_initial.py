# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Region'
        db.create_table(u'fanju_region', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'fanju', ['Region'])

        # Adding model 'Restaurant'
        db.create_table(u'fanju_restaurant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='restaurant', unique=True, null=True, to=orm['fanju.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=135)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('introduction', self.gf('django.db.models.fields.CharField')(max_length=6000, blank=True)),
        ))
        db.send_create_signal(u'fanju', ['Restaurant'])

        # Adding M2M table for field regions on 'Restaurant'
        db.create_table(u'fanju_restaurant_regions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('restaurant', models.ForeignKey(orm[u'fanju.restaurant'], null=False)),
            ('region', models.ForeignKey(orm[u'fanju.region'], null=False))
        ))
        db.create_unique(u'fanju_restaurant_regions', ['restaurant_id', 'region_id'])

        # Adding model 'DishCategory'
        db.create_table(u'fanju_dishcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fanju.Restaurant'], null=True, blank=True)),
        ))
        db.send_create_signal(u'fanju', ['DishCategory'])

        # Adding model 'Dish'
        db.create_table(u'fanju_dish', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=135)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=1)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fanju.Restaurant'])),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('unit', self.gf('django.db.models.fields.CharField')(default=u'\u4efd', max_length=30)),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'fanju', ['Dish'])

        # Adding M2M table for field categories on 'Dish'
        db.create_table(u'fanju_dish_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dish', models.ForeignKey(orm[u'fanju.dish'], null=False)),
            ('dishcategory', models.ForeignKey(orm[u'fanju.dishcategory'], null=False))
        ))
        db.create_unique(u'fanju_dish_categories', ['dish_id', 'dishcategory_id'])

        # Adding model 'Menu'
        db.create_table(u'fanju_menu', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fanju.Restaurant'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('cropping', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('num_persons', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('average_price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=1)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 12, 0, 0))),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'fanju', ['Menu'])

        # Adding unique constraint on 'Menu', fields ['restaurant', 'status', 'name']
        db.create_unique(u'fanju_menu', ['restaurant_id', 'status', 'name'])

        # Adding model 'DishItem'
        db.create_table(u'fanju_dishitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fanju.Menu'])),
            ('dish', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fanju.Dish'])),
            ('num', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('order_no', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'fanju', ['DishItem'])

        # Adding model 'DishCategoryItem'
        db.create_table(u'fanju_dishcategoryitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fanju.Menu'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fanju.DishCategory'])),
            ('order_no', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'fanju', ['DishCategoryItem'])

        # Adding model 'Order'
        db.create_table(u'fanju_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', to=orm['fanju.User'])),
            ('meal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', to=orm['fanju.Meal'])),
            ('num_persons', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('payed_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('completed_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=12, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'fanju', ['Order'])

        # Adding model 'TransFlow'
        db.create_table(u'fanju_transflow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.OneToOneField')(related_name='flow', unique=True, to=orm['fanju.Order'])),
            ('alipay_trade_no', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'fanju', ['TransFlow'])

        # Adding model 'Relationship'
        db.create_table(u'fanju_relationship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from_user', to=orm['fanju.User'])),
            ('to_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_user', to=orm['fanju.User'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'fanju', ['Relationship'])

        # Adding unique constraint on 'Relationship', fields ['from_person', 'to_person']
        db.create_unique(u'fanju_relationship', ['from_person_id', 'to_person_id'])

        # Adding model 'Visitor'
        db.create_table(u'fanju_visitor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='host', to=orm['fanju.User'])),
            ('to_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='visitor', to=orm['fanju.User'])),
        ))
        db.send_create_signal(u'fanju', ['Visitor'])

        # Adding unique constraint on 'Visitor', fields ['from_person', 'to_person']
        db.create_unique(u'fanju_visitor', ['from_person_id', 'to_person_id'])

        # Adding model 'UserLocation'
        db.create_table(u'fanju_userlocation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lng', self.gf('django.db.models.fields.FloatField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'fanju', ['UserLocation'])

        # Adding model 'UserTag'
        db.create_table(u'fanju_usertag', (
            (u'tag_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['taggit.Tag'], unique=True, primary_key=True)),
            ('image_url', self.gf('django.db.models.fields.files.ImageField')(max_length=256)),
        ))
        db.send_create_signal(u'fanju', ['UserTag'])

        # Adding model 'TaggedUser'
        db.create_table(u'fanju_taggeduser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'fanju_taggeduser_tagged_items', to=orm['contenttypes.ContentType'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['fanju.UserTag'])),
        ))
        db.send_create_signal(u'fanju', ['TaggedUser'])

        # Adding model 'User'
        db.create_table(u'fanju_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('gender', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=256, null=True, blank=True)),
            ('cropping', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fanju.UserLocation'], unique=True, null=True, blank=True)),
            ('constellation', self.gf('django.db.models.fields.IntegerField')(default=-1, null=True, blank=True)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('college', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('industry', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('work_for', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('occupation', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('motto', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('weibo_id', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('weibo_access_token', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('apns_token', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'fanju', ['User'])

        # Adding M2M table for field groups on 'User'
        db.create_table(u'fanju_user_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'fanju.user'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(u'fanju_user_groups', ['user_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'User'
        db.create_table(u'fanju_user_user_permissions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'fanju.user'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(u'fanju_user_user_permissions', ['user_id', 'permission_id'])

        # Adding model 'UserPhoto'
        db.create_table(u'fanju_userphoto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='photos', to=orm['fanju.User'])),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=256)),
        ))
        db.send_create_signal(u'fanju', ['UserPhoto'])

        # Adding model 'UserMessage'
        db.create_table(u'fanju_usermessage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sent_from_user', to=orm['fanju.User'])),
            ('to_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sent_to_user', to=orm['fanju.User'])),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'fanju', ['UserMessage'])

        # Adding model 'Meal'
        db.create_table(u'fanju_meal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('introduction', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('start_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 5, 12, 0, 0))),
            ('start_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(19, 0))),
            ('privacy', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('min_persons', self.gf('django.db.models.fields.IntegerField')(default=8)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fanju.Region'], null=True, blank=True)),
            ('list_price', self.gf('django.db.models.fields.DecimalField')(default=30.0, null=True, max_digits=6, decimal_places=1, blank=True)),
            ('extra_requests', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('max_persons', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fanju.Restaurant'], null=True, blank=True)),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fanju.Menu'], null=True, blank=True)),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='host_user', null=True, to=orm['fanju.User'])),
            ('actual_persons', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'fanju', ['Meal'])

        # Adding model 'MealParticipants'
        db.create_table(u'fanju_mealparticipants', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fanju.Meal'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fanju.User'])),
        ))
        db.send_create_signal(u'fanju', ['MealParticipants'])

        # Adding model 'MealComment'
        db.create_table(u'fanju_mealcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fanju.User'], blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('meal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['fanju.Meal'])),
        ))
        db.send_create_signal(u'fanju', ['MealComment'])


    def backwards(self, orm):
        # Removing unique constraint on 'Visitor', fields ['from_person', 'to_person']
        db.delete_unique(u'fanju_visitor', ['from_person_id', 'to_person_id'])

        # Removing unique constraint on 'Relationship', fields ['from_person', 'to_person']
        db.delete_unique(u'fanju_relationship', ['from_person_id', 'to_person_id'])

        # Removing unique constraint on 'Menu', fields ['restaurant', 'status', 'name']
        db.delete_unique(u'fanju_menu', ['restaurant_id', 'status', 'name'])

        # Deleting model 'Region'
        db.delete_table(u'fanju_region')

        # Deleting model 'Restaurant'
        db.delete_table(u'fanju_restaurant')

        # Removing M2M table for field regions on 'Restaurant'
        db.delete_table('fanju_restaurant_regions')

        # Deleting model 'DishCategory'
        db.delete_table(u'fanju_dishcategory')

        # Deleting model 'Dish'
        db.delete_table(u'fanju_dish')

        # Removing M2M table for field categories on 'Dish'
        db.delete_table('fanju_dish_categories')

        # Deleting model 'Menu'
        db.delete_table(u'fanju_menu')

        # Deleting model 'DishItem'
        db.delete_table(u'fanju_dishitem')

        # Deleting model 'DishCategoryItem'
        db.delete_table(u'fanju_dishcategoryitem')

        # Deleting model 'Order'
        db.delete_table(u'fanju_order')

        # Deleting model 'TransFlow'
        db.delete_table(u'fanju_transflow')

        # Deleting model 'Relationship'
        db.delete_table(u'fanju_relationship')

        # Deleting model 'Visitor'
        db.delete_table(u'fanju_visitor')

        # Deleting model 'UserLocation'
        db.delete_table(u'fanju_userlocation')

        # Deleting model 'UserTag'
        db.delete_table(u'fanju_usertag')

        # Deleting model 'TaggedUser'
        db.delete_table(u'fanju_taggeduser')

        # Deleting model 'User'
        db.delete_table(u'fanju_user')

        # Removing M2M table for field groups on 'User'
        db.delete_table('fanju_user_groups')

        # Removing M2M table for field user_permissions on 'User'
        db.delete_table('fanju_user_user_permissions')

        # Deleting model 'UserPhoto'
        db.delete_table(u'fanju_userphoto')

        # Deleting model 'UserMessage'
        db.delete_table(u'fanju_usermessage')

        # Deleting model 'Meal'
        db.delete_table(u'fanju_meal')

        # Deleting model 'MealParticipants'
        db.delete_table(u'fanju_mealparticipants')

        # Deleting model 'MealComment'
        db.delete_table(u'fanju_mealcomment')


    models = {
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'fanju.dish': {
            'Meta': {'object_name': 'Dish'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['fanju.DishCategory']", 'symmetrical': 'False', 'blank': 'True'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '135'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '1'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fanju.Restaurant']"}),
            'unit': ('django.db.models.fields.CharField', [], {'default': "u'\\u4efd'", 'max_length': '30'})
        },
        u'fanju.dishcategory': {
            'Meta': {'object_name': 'DishCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fanju.Restaurant']", 'null': 'True', 'blank': 'True'})
        },
        u'fanju.dishcategoryitem': {
            'Meta': {'object_name': 'DishCategoryItem'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fanju.DishCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fanju.Menu']"}),
            'order_no': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'fanju.dishitem': {
            'Meta': {'object_name': 'DishItem'},
            'dish': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fanju.Dish']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fanju.Menu']"}),
            'num': ('django.db.models.fields.SmallIntegerField', [], {}),
            'order_no': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'fanju.meal': {
            'Meta': {'object_name': 'Meal'},
            'actual_persons': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'extra_requests': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'host_user'", 'null': 'True', 'to': u"orm['fanju.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'list_price': ('django.db.models.fields.DecimalField', [], {'default': '30.0', 'null': 'True', 'max_digits': '6', 'decimal_places': '1', 'blank': 'True'}),
            'max_persons': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fanju.Menu']", 'null': 'True', 'blank': 'True'}),
            'min_persons': ('django.db.models.fields.IntegerField', [], {'default': '8'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'meals'", 'to': u"orm['fanju.User']", 'through': u"orm['fanju.MealParticipants']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fanju.Region']", 'null': 'True', 'blank': 'True'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fanju.Restaurant']", 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 5, 12, 0, 0)'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(19, 0)'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'fanju.mealcomment': {
            'Meta': {'object_name': 'MealComment'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'from_person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fanju.User']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['fanju.Meal']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'fanju.mealparticipants': {
            'Meta': {'ordering': "['id']", 'object_name': 'MealParticipants'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fanju.Meal']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fanju.User']"})
        },
        u'fanju.menu': {
            'Meta': {'unique_together': "(('restaurant', 'status', 'name'),)", 'object_name': 'Menu'},
            'average_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '1'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 12, 0, 0)'}),
            'cropping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'dish_category_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['fanju.DishCategory']", 'through': u"orm['fanju.DishCategoryItem']", 'symmetrical': 'False'}),
            'dish_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['fanju.Dish']", 'through': u"orm['fanju.DishItem']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'num_persons': ('django.db.models.fields.SmallIntegerField', [], {}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fanju.Restaurant']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'fanju.order': {
            'Meta': {'object_name': 'Order'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '12', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'completed_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': u"orm['fanju.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': u"orm['fanju.Meal']"}),
            'num_persons': ('django.db.models.fields.IntegerField', [], {}),
            'payed_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        },
        u'fanju.region': {
            'Meta': {'object_name': 'Region'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'fanju.relationship': {
            'Meta': {'unique_together': "(('from_person', 'to_person'),)", 'object_name': 'Relationship'},
            'from_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_user'", 'to': u"orm['fanju.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'to_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_user'", 'to': u"orm['fanju.User']"})
        },
        u'fanju.restaurant': {
            'Meta': {'object_name': 'Restaurant'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.CharField', [], {'max_length': '6000', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '135'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['fanju.Region']", 'null': 'True', 'blank': 'True'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'restaurant'", 'unique': 'True', 'null': 'True', 'to': u"orm['fanju.User']"})
        },
        u'fanju.taggeduser': {
            'Meta': {'object_name': 'TaggedUser'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'fanju_taggeduser_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['fanju.UserTag']"})
        },
        u'fanju.transflow': {
            'Meta': {'object_name': 'TransFlow'},
            'alipay_trade_no': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'flow'", 'unique': 'True', 'to': u"orm['fanju.Order']"})
        },
        u'fanju.user': {
            'Meta': {'object_name': 'User'},
            'apns_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'college': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'constellation': ('django.db.models.fields.IntegerField', [], {'default': '-1', 'null': 'True', 'blank': 'True'}),
            'cropping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'followers'", 'symmetrical': 'False', 'through': u"orm['fanju.Relationship']", 'to': u"orm['fanju.User']"}),
            'gender': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fanju.UserLocation']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'motto': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'visitoring': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'visitors'", 'symmetrical': 'False', 'through': u"orm['fanju.Visitor']", 'to': u"orm['fanju.User']"}),
            'weibo_access_token': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'weibo_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'work_for': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'fanju.userlocation': {
            'Meta': {'object_name': 'UserLocation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'fanju.usermessage': {
            'Meta': {'object_name': 'UserMessage'},
            'from_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_from_user'", 'to': u"orm['fanju.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'to_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_to_user'", 'to': u"orm['fanju.User']"}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'fanju.userphoto': {
            'Meta': {'object_name': 'UserPhoto'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '256'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': u"orm['fanju.User']"})
        },
        u'fanju.usertag': {
            'Meta': {'object_name': 'UserTag', '_ormbases': [u'taggit.Tag']},
            'image_url': ('django.db.models.fields.files.ImageField', [], {'max_length': '256'}),
            u'tag_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['taggit.Tag']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'fanju.visitor': {
            'Meta': {'unique_together': "(('from_person', 'to_person'),)", 'object_name': 'Visitor'},
            'from_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'host'", 'to': u"orm['fanju.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'visitor'", 'to': u"orm['fanju.User']"})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['fanju']