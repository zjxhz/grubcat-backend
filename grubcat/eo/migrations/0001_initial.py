# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Region'
        db.create_table('eo_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('eo', ['Region'])

        # Adding model 'Restaurant'
        db.create_table('eo_restaurant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='restaurant', unique=True, null=True, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=135)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('introduction', self.gf('django.db.models.fields.CharField')(max_length=6000, blank=True)),
        ))
        db.send_create_signal('eo', ['Restaurant'])

        # Adding M2M table for field regions on 'Restaurant'
        db.create_table('eo_restaurant_regions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('restaurant', models.ForeignKey(orm['eo.restaurant'], null=False)),
            ('region', models.ForeignKey(orm['eo.region'], null=False))
        ))
        db.create_unique('eo_restaurant_regions', ['restaurant_id', 'region_id'])

        # Adding model 'DishCategory'
        db.create_table('eo_dishcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Restaurant'], null=True, blank=True)),
        ))
        db.send_create_signal('eo', ['DishCategory'])

        # Adding model 'Dish'
        db.create_table('eo_dish', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=135)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=1)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Restaurant'])),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('unit', self.gf('django.db.models.fields.CharField')(default=u'\u4efd', max_length=30)),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('eo', ['Dish'])

        # Adding M2M table for field categories on 'Dish'
        db.create_table('eo_dish_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dish', models.ForeignKey(orm['eo.dish'], null=False)),
            ('dishcategory', models.ForeignKey(orm['eo.dishcategory'], null=False))
        ))
        db.create_unique('eo_dish_categories', ['dish_id', 'dishcategory_id'])

        # Adding model 'Menu'
        db.create_table('eo_menu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Restaurant'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('cropping', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('num_persons', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('average_price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=1)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 6, 0, 0))),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('eo', ['Menu'])

        # Adding unique constraint on 'Menu', fields ['restaurant', 'status', 'name']
        db.create_unique('eo_menu', ['restaurant_id', 'status', 'name'])

        # Adding model 'DishItem'
        db.create_table('eo_dishitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Menu'])),
            ('dish', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Dish'])),
            ('num', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('order_no', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('eo', ['DishItem'])

        # Adding model 'DishCategoryItem'
        db.create_table('eo_dishcategoryitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Menu'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.DishCategory'])),
            ('order_no', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('eo', ['DishCategoryItem'])

        # Adding model 'Order'
        db.create_table('eo_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', to=orm['eo.UserProfile'])),
            ('meal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', to=orm['eo.Meal'])),
            ('num_persons', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('payed_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('completed_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=12, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('eo', ['Order'])

        # Adding model 'TransFlow'
        db.create_table('eo_transflow', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.OneToOneField')(related_name='flow', unique=True, to=orm['eo.Order'])),
            ('alipay_trade_no', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('eo', ['TransFlow'])

        # Adding model 'Relationship'
        db.create_table('eo_relationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from_user', to=orm['eo.UserProfile'])),
            ('to_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_user', to=orm['eo.UserProfile'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('eo', ['Relationship'])

        # Adding unique constraint on 'Relationship', fields ['from_person', 'to_person']
        db.create_unique('eo_relationship', ['from_person_id', 'to_person_id'])

        # Adding model 'Visitor'
        db.create_table('eo_visitor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='host', to=orm['eo.UserProfile'])),
            ('to_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='visitor', to=orm['eo.UserProfile'])),
        ))
        db.send_create_signal('eo', ['Visitor'])

        # Adding unique constraint on 'Visitor', fields ['from_person', 'to_person']
        db.create_unique('eo_visitor', ['from_person_id', 'to_person_id'])

        # Adding model 'UserLocation'
        db.create_table('eo_userlocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lng', self.gf('django.db.models.fields.FloatField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('eo', ['UserLocation'])

        # Adding model 'UserTag'
        db.create_table('eo_usertag', (
            ('tag_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['taggit.Tag'], unique=True, primary_key=True)),
            ('image_url', self.gf('django.db.models.fields.files.ImageField')(max_length=256)),
        ))
        db.send_create_signal('eo', ['UserTag'])

        # Adding model 'TaggedUser'
        db.create_table('eo_taggeduser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='eo_taggeduser_tagged_items', to=orm['contenttypes.ContentType'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['eo.UserTag'])),
        ))
        db.send_create_signal('eo', ['TaggedUser'])

        # Adding model 'UserProfile'
        db.create_table('eo_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('gender', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=256, null=True)),
            ('cropping', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.UserLocation'], unique=True, null=True, blank=True)),
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
        db.send_create_signal('eo', ['UserProfile'])

        # Adding M2M table for field favorite_restaurants on 'UserProfile'
        db.create_table('eo_userprofile_favorite_restaurants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['eo.userprofile'], null=False)),
            ('restaurant', models.ForeignKey(orm['eo.restaurant'], null=False))
        ))
        db.create_unique('eo_userprofile_favorite_restaurants', ['userprofile_id', 'restaurant_id'])

        # Adding M2M table for field recommended_following on 'UserProfile'
        db.create_table('eo_userprofile_recommended_following', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_userprofile', models.ForeignKey(orm['eo.userprofile'], null=False)),
            ('to_userprofile', models.ForeignKey(orm['eo.userprofile'], null=False))
        ))
        db.create_unique('eo_userprofile_recommended_following', ['from_userprofile_id', 'to_userprofile_id'])

        # Adding model 'UserPhoto'
        db.create_table('eo_userphoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='photos', to=orm['eo.UserProfile'])),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=256)),
        ))
        db.send_create_signal('eo', ['UserPhoto'])

        # Adding model 'UserMessage'
        db.create_table('eo_usermessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sent_from_user', to=orm['eo.UserProfile'])),
            ('to_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sent_to_user', to=orm['eo.UserProfile'])),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('eo', ['UserMessage'])

        # Adding model 'Meal'
        db.create_table('eo_meal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('introduction', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('start_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 5, 6, 0, 0))),
            ('start_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(19, 0))),
            ('privacy', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('min_persons', self.gf('django.db.models.fields.IntegerField')(default=8)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Region'], null=True, blank=True)),
            ('list_price', self.gf('django.db.models.fields.DecimalField')(default=30.0, null=True, max_digits=6, decimal_places=1, blank=True)),
            ('extra_requests', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('max_persons', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Restaurant'], null=True, blank=True)),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Menu'], null=True, blank=True)),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='host_user', null=True, to=orm['eo.UserProfile'])),
            ('actual_persons', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('eo', ['Meal'])

        # Adding model 'MealParticipants'
        db.create_table('eo_mealparticipants', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Meal'])),
            ('userprofile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.UserProfile'])),
        ))
        db.send_create_signal('eo', ['MealParticipants'])

        # Adding model 'MealComment'
        db.create_table('eo_mealcomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.UserProfile'], blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('meal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['eo.Meal'])),
        ))
        db.send_create_signal('eo', ['MealComment'])


    def backwards(self, orm):
        # Removing unique constraint on 'Visitor', fields ['from_person', 'to_person']
        db.delete_unique('eo_visitor', ['from_person_id', 'to_person_id'])

        # Removing unique constraint on 'Relationship', fields ['from_person', 'to_person']
        db.delete_unique('eo_relationship', ['from_person_id', 'to_person_id'])

        # Removing unique constraint on 'Menu', fields ['restaurant', 'status', 'name']
        db.delete_unique('eo_menu', ['restaurant_id', 'status', 'name'])

        # Deleting model 'Region'
        db.delete_table('eo_region')

        # Deleting model 'Restaurant'
        db.delete_table('eo_restaurant')

        # Removing M2M table for field regions on 'Restaurant'
        db.delete_table('eo_restaurant_regions')

        # Deleting model 'DishCategory'
        db.delete_table('eo_dishcategory')

        # Deleting model 'Dish'
        db.delete_table('eo_dish')

        # Removing M2M table for field categories on 'Dish'
        db.delete_table('eo_dish_categories')

        # Deleting model 'Menu'
        db.delete_table('eo_menu')

        # Deleting model 'DishItem'
        db.delete_table('eo_dishitem')

        # Deleting model 'DishCategoryItem'
        db.delete_table('eo_dishcategoryitem')

        # Deleting model 'Order'
        db.delete_table('eo_order')

        # Deleting model 'TransFlow'
        db.delete_table('eo_transflow')

        # Deleting model 'Relationship'
        db.delete_table('eo_relationship')

        # Deleting model 'Visitor'
        db.delete_table('eo_visitor')

        # Deleting model 'UserLocation'
        db.delete_table('eo_userlocation')

        # Deleting model 'UserTag'
        db.delete_table('eo_usertag')

        # Deleting model 'TaggedUser'
        db.delete_table('eo_taggeduser')

        # Deleting model 'UserProfile'
        db.delete_table('eo_userprofile')

        # Removing M2M table for field favorite_restaurants on 'UserProfile'
        db.delete_table('eo_userprofile_favorite_restaurants')

        # Removing M2M table for field recommended_following on 'UserProfile'
        db.delete_table('eo_userprofile_recommended_following')

        # Deleting model 'UserPhoto'
        db.delete_table('eo_userphoto')

        # Deleting model 'UserMessage'
        db.delete_table('eo_usermessage')

        # Deleting model 'Meal'
        db.delete_table('eo_meal')

        # Deleting model 'MealParticipants'
        db.delete_table('eo_mealparticipants')

        # Deleting model 'MealComment'
        db.delete_table('eo_mealcomment')


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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'eo.dish': {
            'Meta': {'object_name': 'Dish'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eo.DishCategory']", 'symmetrical': 'False'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '135'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '1'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Restaurant']"}),
            'unit': ('django.db.models.fields.CharField', [], {'default': "u'\\u4efd'", 'max_length': '30'})
        },
        'eo.dishcategory': {
            'Meta': {'object_name': 'DishCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Restaurant']", 'null': 'True', 'blank': 'True'})
        },
        'eo.dishcategoryitem': {
            'Meta': {'object_name': 'DishCategoryItem'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.DishCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Menu']"}),
            'order_no': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'eo.dishitem': {
            'Meta': {'object_name': 'DishItem'},
            'dish': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Dish']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Menu']"}),
            'num': ('django.db.models.fields.SmallIntegerField', [], {}),
            'order_no': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'eo.meal': {
            'Meta': {'object_name': 'Meal'},
            'actual_persons': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'extra_requests': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'host_user'", 'null': 'True', 'to': "orm['eo.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'list_price': ('django.db.models.fields.DecimalField', [], {'default': '30.0', 'null': 'True', 'max_digits': '6', 'decimal_places': '1', 'blank': 'True'}),
            'max_persons': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Menu']", 'null': 'True', 'blank': 'True'}),
            'min_persons': ('django.db.models.fields.IntegerField', [], {'default': '8'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'meals'", 'to': "orm['eo.UserProfile']", 'through': "orm['eo.MealParticipants']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Region']", 'null': 'True', 'blank': 'True'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Restaurant']", 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 5, 6, 0, 0)'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(19, 0)'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'eo.mealcomment': {
            'Meta': {'object_name': 'MealComment'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'from_person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.UserProfile']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['eo.Meal']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'eo.mealparticipants': {
            'Meta': {'ordering': "['id']", 'object_name': 'MealParticipants'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Meal']"}),
            'userprofile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.UserProfile']"})
        },
        'eo.menu': {
            'Meta': {'unique_together': "(('restaurant', 'status', 'name'),)", 'object_name': 'Menu'},
            'average_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '1'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 6, 0, 0)'}),
            'cropping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'dish_category_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eo.DishCategory']", 'through': "orm['eo.DishCategoryItem']", 'symmetrical': 'False'}),
            'dish_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eo.Dish']", 'through': "orm['eo.DishItem']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'num_persons': ('django.db.models.fields.SmallIntegerField', [], {}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Restaurant']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'eo.order': {
            'Meta': {'object_name': 'Order'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '12', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'completed_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['eo.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['eo.Meal']"}),
            'num_persons': ('django.db.models.fields.IntegerField', [], {}),
            'payed_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        },
        'eo.region': {
            'Meta': {'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'eo.relationship': {
            'Meta': {'unique_together': "(('from_person', 'to_person'),)", 'object_name': 'Relationship'},
            'from_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_user'", 'to': "orm['eo.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'to_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_user'", 'to': "orm['eo.UserProfile']"})
        },
        'eo.restaurant': {
            'Meta': {'object_name': 'Restaurant'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.CharField', [], {'max_length': '6000', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '135'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eo.Region']", 'symmetrical': 'False'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'restaurant'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        },
        'eo.taggeduser': {
            'Meta': {'object_name': 'TaggedUser'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eo_taggeduser_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['eo.UserTag']"})
        },
        'eo.transflow': {
            'Meta': {'object_name': 'TransFlow'},
            'alipay_trade_no': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'flow'", 'unique': 'True', 'to': "orm['eo.Order']"})
        },
        'eo.userlocation': {
            'Meta': {'object_name': 'UserLocation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'eo.usermessage': {
            'Meta': {'object_name': 'UserMessage'},
            'from_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_from_user'", 'to': "orm['eo.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'to_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_to_user'", 'to': "orm['eo.UserProfile']"}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'eo.userphoto': {
            'Meta': {'object_name': 'UserPhoto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '256'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': "orm['eo.UserProfile']"})
        },
        'eo.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'apns_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '256', 'null': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'college': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'constellation': ('django.db.models.fields.IntegerField', [], {'default': '-1', 'null': 'True', 'blank': 'True'}),
            'cropping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'favorite_restaurants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_favorite'", 'blank': 'True', 'to': "orm['eo.Restaurant']"}),
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'followers'", 'symmetrical': 'False', 'through': "orm['eo.Relationship']", 'to': "orm['eo.UserProfile']"}),
            'gender': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.UserLocation']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'motto': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'recommended_following': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['eo.UserProfile']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'visitoring': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'visitors'", 'symmetrical': 'False', 'through': "orm['eo.Visitor']", 'to': "orm['eo.UserProfile']"}),
            'weibo_access_token': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'weibo_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'work_for': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'eo.usertag': {
            'Meta': {'object_name': 'UserTag', '_ormbases': ['taggit.Tag']},
            'image_url': ('django.db.models.fields.files.ImageField', [], {'max_length': '256'}),
            'tag_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['taggit.Tag']", 'unique': 'True', 'primary_key': 'True'})
        },
        'eo.visitor': {
            'Meta': {'unique_together': "(('from_person', 'to_person'),)", 'object_name': 'Visitor'},
            'from_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'host'", 'to': "orm['eo.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'visitor'", 'to': "orm['eo.UserProfile']"})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['eo']