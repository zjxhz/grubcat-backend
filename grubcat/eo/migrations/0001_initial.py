# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table(u'company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=135)),
        ))
        db.send_create_signal('eo', ['Company'])

        # Adding model 'RestaurantTag'
        db.create_table(u'restaurant_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
        ))
        db.send_create_signal('eo', ['RestaurantTag'])

        # Adding model 'Region'
        db.create_table(u'region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('eo', ['Region'])

        # Adding model 'Restaurant'
        db.create_table(u'restaurant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=135)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('tel2', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('introduction', self.gf('django.db.models.fields.CharField')(max_length=6000, blank=True)),
            ('phone_img_url', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('average_cost', self.gf('django.db.models.fields.IntegerField')()),
            ('rating', self.gf('django.db.models.fields.IntegerField')()),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Company'])),
        ))
        db.send_create_signal('eo', ['Restaurant'])

        # Adding M2M table for field tags on 'Restaurant'
        db.create_table(u'restaurant_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('restaurant', models.ForeignKey(orm['eo.restaurant'], null=False)),
            ('restauranttag', models.ForeignKey(orm['eo.restauranttag'], null=False))
        ))
        db.create_unique(u'restaurant_tags', ['restaurant_id', 'restauranttag_id'])

        # Adding M2M table for field regions on 'Restaurant'
        db.create_table(u'restaurant_regions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('restaurant', models.ForeignKey(orm['eo.restaurant'], null=False)),
            ('region', models.ForeignKey(orm['eo.region'], null=False))
        ))
        db.create_unique(u'restaurant_regions', ['restaurant_id', 'region_id'])

        # Adding model 'RestaurantInfo'
        db.create_table(u'restaurant_info', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('restaurant', self.gf('django.db.models.fields.related.OneToOneField')(related_name='info', unique=True, to=orm['eo.Restaurant'])),
            ('average_cost', self.gf('django.db.models.fields.FloatField')()),
            ('average_rating', self.gf('django.db.models.fields.FloatField')()),
            ('good_rating_percentage', self.gf('django.db.models.fields.FloatField')()),
            ('divider', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('eo', ['RestaurantInfo'])

        # Adding model 'RatingPic'
        db.create_table(u'rating_pic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Restaurant'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal('eo', ['RatingPic'])

        # Adding model 'Menu'
        db.create_table(u'menu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('restaurant', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['eo.Restaurant'], unique=True)),
            ('cover', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('menu_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('eo', ['Menu'])

        # Adding model 'DishTag'
        db.create_table(u'dish_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('eo', ['DishTag'])

        # Adding model 'DishCategory'
        db.create_table(u'dish_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(related_name='categories', to=orm['eo.Menu'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.DishCategory'], null=True)),
        ))
        db.send_create_signal('eo', ['DishCategory'])

        # Adding model 'Dish'
        db.create_table(u'dish', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=135)),
            ('pic', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Restaurant'])),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dishes', null=True, to=orm['eo.Menu'])),
            ('ingredient', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('cooking', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('taste', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('uom', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('has_other_uom', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('available', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_mandatory', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_recommended', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('eo', ['Dish'])

        # Adding M2M table for field tags on 'Dish'
        db.create_table(u'dish_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dish', models.ForeignKey(orm['eo.dish'], null=False)),
            ('dishtag', models.ForeignKey(orm['eo.dishtag'], null=False))
        ))
        db.create_unique(u'dish_tags', ['dish_id', 'dishtag_id'])

        # Adding M2M table for field categories on 'Dish'
        db.create_table(u'dish_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dish', models.ForeignKey(orm['eo.dish'], null=False)),
            ('dishcategory', models.ForeignKey(orm['eo.dishcategory'], null=False))
        ))
        db.create_unique(u'dish_categories', ['dish_id', 'dishcategory_id'])

        # Adding model 'DishOtherUom'
        db.create_table(u'dish_other_uom', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=0)),
            ('uom', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('dish', self.gf('django.db.models.fields.related.ForeignKey')(related_name='other_uom', to=orm['eo.Dish'])),
        ))
        db.send_create_signal('eo', ['DishOtherUom'])

        # Adding model 'Rating'
        db.create_table(u'rating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_ratings', to=orm['auth.User'])),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ratings', to=orm['eo.Restaurant'])),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=4096)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('rating', self.gf('django.db.models.fields.FloatField')()),
            ('average_cost', self.gf('django.db.models.fields.FloatField')()),
            ('auto_share', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('eo', ['Rating'])

        # Adding M2M table for field dishes on 'Rating'
        db.create_table('rating_dishes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('rating', models.ForeignKey(orm['eo.rating'], null=False)),
            ('dish', models.ForeignKey(orm['eo.dish'], null=False))
        ))
        db.create_unique('rating_dishes', ['rating_id', 'dish_id'])

        # Adding model 'Order'
        db.create_table(u'order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Restaurant'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', to=orm['eo.UserProfile'])),
            ('num_persons', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('total_price', self.gf('django.db.models.fields.FloatField')()),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('confirmed_time', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('completed_time', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('table', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('eo', ['Order'])

        # Adding model 'OrderDishes'
        db.create_table(u'order_dishes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Order'])),
            ('dish', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Dish'])),
            ('quantity', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('eo', ['OrderDishes'])

        # Adding model 'Relationship'
        db.create_table(u'relationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from_user', to=orm['eo.UserProfile'])),
            ('to_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_user', to=orm['eo.UserProfile'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('eo', ['Relationship'])

        # Adding model 'UserLocation'
        db.create_table(u'user_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lng', self.gf('django.db.models.fields.FloatField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('eo', ['UserLocation'])

        # Adding model 'UserProfile'
        db.create_table(u'user_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('gender', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=256)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.UserLocation'], unique=True, null=True)),
            ('constellation', self.gf('django.db.models.fields.IntegerField')(default=-1, null=True)),
            ('birthday', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('college', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('work_for', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('occupation', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
        ))
        db.send_create_signal('eo', ['UserProfile'])

        # Adding M2M table for field favorite_restaurants on 'UserProfile'
        db.create_table('favorite_restaurants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['eo.userprofile'], null=False)),
            ('restaurant', models.ForeignKey(orm['eo.restaurant'], null=False))
        ))
        db.create_unique('favorite_restaurants', ['userprofile_id', 'restaurant_id'])

        # Adding M2M table for field recommended_following on 'UserProfile'
        db.create_table('recommended_following', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_userprofile', models.ForeignKey(orm['eo.userprofile'], null=False)),
            ('to_userprofile', models.ForeignKey(orm['eo.userprofile'], null=False))
        ))
        db.create_unique('recommended_following', ['from_userprofile_id', 'to_userprofile_id'])

        # Adding model 'UserMessage'
        db.create_table(u'user_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sent_from_user', to=orm['eo.UserProfile'])),
            ('to_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sent_to_user', to=orm['eo.UserProfile'])),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('eo', ['UserMessage'])

        # Adding model 'BestRatingDish'
        db.create_table(u'best_rating_dish', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='best_rating_dishes', to=orm['eo.Restaurant'])),
            ('dish', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Dish'])),
            ('times', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('eo', ['BestRatingDish'])

        # Adding model 'Meal'
        db.create_table(u'meal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Restaurant'])),
            ('order', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['eo.Order'], unique=True, null=True)),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('introduction', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('list_price', self.gf('django.db.models.fields.IntegerField')()),
            ('photo', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(related_name='host_user', null=True, to=orm['eo.UserProfile'])),
            ('actual_persons', self.gf('django.db.models.fields.IntegerField')(default=1, null=True)),
            ('min_persons', self.gf('django.db.models.fields.IntegerField')()),
            ('max_persons', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('privacy', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('eo', ['Meal'])

        # Adding M2M table for field participants on 'Meal'
        db.create_table(u'meal_participants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meal', models.ForeignKey(orm['eo.meal'], null=False)),
            ('userprofile', models.ForeignKey(orm['eo.userprofile'], null=False))
        ))
        db.create_unique(u'meal_participants', ['meal_id', 'userprofile_id'])

        # Adding model 'MealComment'
        db.create_table(u'meal_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['eo.Meal'])),
            ('from_person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.UserProfile'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=42)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 6, 16, 0, 0))),
        ))
        db.send_create_signal('eo', ['MealComment'])

        # Adding model 'MealInvitation'
        db.create_table(u'meal_invitation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invitation_from_user', to=orm['eo.UserProfile'])),
            ('to_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invitation_to_user', to=orm['eo.UserProfile'])),
            ('meal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eo.Meal'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 6, 16, 0, 0))),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('eo', ['MealInvitation'])

        # Adding model 'ImageTest'
        db.create_table('eo_imagetest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('cropping', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('eo', ['ImageTest'])


    def backwards(self, orm):
        # Deleting model 'Company'
        db.delete_table(u'company')

        # Deleting model 'RestaurantTag'
        db.delete_table(u'restaurant_tag')

        # Deleting model 'Region'
        db.delete_table(u'region')

        # Deleting model 'Restaurant'
        db.delete_table(u'restaurant')

        # Removing M2M table for field tags on 'Restaurant'
        db.delete_table('restaurant_tags')

        # Removing M2M table for field regions on 'Restaurant'
        db.delete_table('restaurant_regions')

        # Deleting model 'RestaurantInfo'
        db.delete_table(u'restaurant_info')

        # Deleting model 'RatingPic'
        db.delete_table(u'rating_pic')

        # Deleting model 'Menu'
        db.delete_table(u'menu')

        # Deleting model 'DishTag'
        db.delete_table(u'dish_tag')

        # Deleting model 'DishCategory'
        db.delete_table(u'dish_category')

        # Deleting model 'Dish'
        db.delete_table(u'dish')

        # Removing M2M table for field tags on 'Dish'
        db.delete_table('dish_tags')

        # Removing M2M table for field categories on 'Dish'
        db.delete_table('dish_categories')

        # Deleting model 'DishOtherUom'
        db.delete_table(u'dish_other_uom')

        # Deleting model 'Rating'
        db.delete_table(u'rating')

        # Removing M2M table for field dishes on 'Rating'
        db.delete_table('rating_dishes')

        # Deleting model 'Order'
        db.delete_table(u'order')

        # Deleting model 'OrderDishes'
        db.delete_table(u'order_dishes')

        # Deleting model 'Relationship'
        db.delete_table(u'relationship')

        # Deleting model 'UserLocation'
        db.delete_table(u'user_location')

        # Deleting model 'UserProfile'
        db.delete_table(u'user_profile')

        # Removing M2M table for field favorite_restaurants on 'UserProfile'
        db.delete_table('favorite_restaurants')

        # Removing M2M table for field recommended_following on 'UserProfile'
        db.delete_table('recommended_following')

        # Deleting model 'UserMessage'
        db.delete_table(u'user_message')

        # Deleting model 'BestRatingDish'
        db.delete_table(u'best_rating_dish')

        # Deleting model 'Meal'
        db.delete_table(u'meal')

        # Removing M2M table for field participants on 'Meal'
        db.delete_table('meal_participants')

        # Deleting model 'MealComment'
        db.delete_table(u'meal_comment')

        # Deleting model 'MealInvitation'
        db.delete_table(u'meal_invitation')

        # Deleting model 'ImageTest'
        db.delete_table('eo_imagetest')


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
        'eo.bestratingdish': {
            'Meta': {'object_name': 'BestRatingDish', 'db_table': "u'best_rating_dish'"},
            'dish': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Dish']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'best_rating_dishes'", 'to': "orm['eo.Restaurant']"}),
            'times': ('django.db.models.fields.IntegerField', [], {})
        },
        'eo.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '135'})
        },
        'eo.dish': {
            'Meta': {'object_name': 'Dish', 'db_table': "u'dish'"},
            'available': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eo.DishCategory']", 'symmetrical': 'False'}),
            'cooking': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'has_other_uom': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'is_mandatory': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'is_recommended': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dishes'", 'null': 'True', 'to': "orm['eo.Menu']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '135'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'pic': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Restaurant']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eo.DishTag']", 'symmetrical': 'False'}),
            'taste': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'uom': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'eo.dishcategory': {
            'Meta': {'object_name': 'DishCategory', 'db_table': "u'dish_category'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'categories'", 'to': "orm['eo.Menu']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.DishCategory']", 'null': 'True'})
        },
        'eo.dishotheruom': {
            'Meta': {'object_name': 'DishOtherUom', 'db_table': "u'dish_other_uom'"},
            'dish': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'other_uom'", 'to': "orm['eo.Dish']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '0'}),
            'uom': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'eo.dishtag': {
            'Meta': {'object_name': 'DishTag', 'db_table': "u'dish_tag'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'eo.imagetest': {
            'Meta': {'object_name': 'ImageTest'},
            'cropping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'eo.meal': {
            'Meta': {'object_name': 'Meal', 'db_table': "u'meal'"},
            'actual_persons': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'host_user'", 'null': 'True', 'to': "orm['eo.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'list_price': ('django.db.models.fields.IntegerField', [], {}),
            'max_persons': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'min_persons': ('django.db.models.fields.IntegerField', [], {}),
            'order': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['eo.Order']", 'unique': 'True', 'null': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eo.UserProfile']", 'symmetrical': 'False'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'privacy': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Restaurant']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'eo.mealcomment': {
            'Meta': {'object_name': 'MealComment', 'db_table': "u'meal_comment'"},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
            'from_person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['eo.Meal']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 16, 0, 0)'})
        },
        'eo.mealinvitation': {
            'Meta': {'object_name': 'MealInvitation', 'db_table': "u'meal_invitation'"},
            'from_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invitation_from_user'", 'to': "orm['eo.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Meal']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 16, 0, 0)'}),
            'to_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invitation_to_user'", 'to': "orm['eo.UserProfile']"})
        },
        'eo.menu': {
            'Meta': {'object_name': 'Menu', 'db_table': "u'menu'"},
            'cover': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'restaurant': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['eo.Restaurant']", 'unique': 'True'})
        },
        'eo.order': {
            'Meta': {'object_name': 'Order', 'db_table': "u'order'"},
            'completed_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'confirmed_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['eo.UserProfile']"}),
            'dishes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eo.Dish']", 'through': "orm['eo.OrderDishes']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_persons': ('django.db.models.fields.IntegerField', [], {}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Restaurant']"}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'table': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'total_price': ('django.db.models.fields.FloatField', [], {})
        },
        'eo.orderdishes': {
            'Meta': {'object_name': 'OrderDishes', 'db_table': "u'order_dishes'"},
            'dish': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Dish']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Order']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {})
        },
        'eo.rating': {
            'Meta': {'object_name': 'Rating', 'db_table': "u'rating'"},
            'auto_share': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'average_cost': ('django.db.models.fields.FloatField', [], {}),
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'dishes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eo.Dish']", 'db_table': "'rating_dishes'", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'to': "orm['eo.Restaurant']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_ratings'", 'to': "orm['auth.User']"})
        },
        'eo.ratingpic': {
            'Meta': {'object_name': 'RatingPic', 'db_table': "u'rating_pic'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Restaurant']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'eo.region': {
            'Meta': {'object_name': 'Region', 'db_table': "u'region'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'eo.relationship': {
            'Meta': {'object_name': 'Relationship', 'db_table': "u'relationship'"},
            'from_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_user'", 'to': "orm['eo.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'to_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_user'", 'to': "orm['eo.UserProfile']"})
        },
        'eo.restaurant': {
            'Meta': {'object_name': 'Restaurant', 'db_table': "u'restaurant'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'average_cost': ('django.db.models.fields.IntegerField', [], {}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Company']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.CharField', [], {'max_length': '6000', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '135'}),
            'phone_img_url': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eo.Region']", 'symmetrical': 'False'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eo.RestaurantTag']", 'symmetrical': 'False'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'tel2': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'})
        },
        'eo.restaurantinfo': {
            'Meta': {'object_name': 'RestaurantInfo', 'db_table': "u'restaurant_info'"},
            'average_cost': ('django.db.models.fields.FloatField', [], {}),
            'average_rating': ('django.db.models.fields.FloatField', [], {}),
            'divider': ('django.db.models.fields.IntegerField', [], {}),
            'good_rating_percentage': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'restaurant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'info'", 'unique': 'True', 'to': "orm['eo.Restaurant']"})
        },
        'eo.restauranttag': {
            'Meta': {'object_name': 'RestaurantTag', 'db_table': "u'restaurant_tag'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        'eo.userlocation': {
            'Meta': {'object_name': 'UserLocation', 'db_table': "u'user_location'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'eo.usermessage': {
            'Meta': {'object_name': 'UserMessage', 'db_table': "u'user_message'"},
            'from_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_from_user'", 'to': "orm['eo.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'to_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_to_user'", 'to': "orm['eo.UserProfile']"}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'eo.userprofile': {
            'Meta': {'object_name': 'UserProfile', 'db_table': "u'user_profile'"},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '256'}),
            'birthday': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'college': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'constellation': ('django.db.models.fields.IntegerField', [], {'default': '-1', 'null': 'True'}),
            'favorite_restaurants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_favorite'", 'symmetrical': 'False', 'db_table': "'favorite_restaurants'", 'to': "orm['eo.Restaurant']"}),
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_to'", 'symmetrical': 'False', 'through': "orm['eo.Relationship']", 'to': "orm['eo.UserProfile']"}),
            'gender': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.UserLocation']", 'unique': 'True', 'null': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'recommended_following': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eo.UserProfile']", 'db_table': "'recommended_following'", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'work_for': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'})
        }
    }

    complete_apps = ['eo']