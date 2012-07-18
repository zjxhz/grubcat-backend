# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        other_category = orm.DishCategory.objects.get(pk=1)
        other_category.name=u'其它'
        other_category.save()
        for dish in orm.Dish.objects.filter(categories__isnull=True):
            dish.categories.add(other_category)
            dish.save()

        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."

    def backwards(self, orm):
        "Write your backwards methods here."

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
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eo.DishCategory']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '135'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Restaurant']"}),
            'unit': ('django.db.models.fields.CharField', [], {'default': "u'\\u4efd'", 'max_length': '30'})
        },
        'eo.dishcategory': {
            'Meta': {'object_name': 'DishCategory', 'db_table': "u'dish_category'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '45'})
        },
        'eo.imagetest': {
            'Meta': {'object_name': 'ImageTest'},
            'cropping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'eo.meal': {
            'Meta': {'object_name': 'Meal', 'db_table': "u'meal'"},
            'actual_persons': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'dishes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eo.Dish']", 'through': "orm['eo.MealDishes']", 'symmetrical': 'False'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'host_user'", 'null': 'True', 'to': "orm['eo.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'liked_meals'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['eo.UserProfile']"}),
            'list_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'max_persons': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'min_persons': ('django.db.models.fields.IntegerField', [], {}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'meals'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['eo.UserProfile']"}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'privacy': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Restaurant']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'eo.mealcomment': {
            'Meta': {'object_name': 'MealComment', 'db_table': "u'meal_comment'"},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
            'from_person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['eo.Meal']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 4, 0, 0)'})
        },
        'eo.mealdishes': {
            'Meta': {'object_name': 'MealDishes', 'db_table': "u'meal_dishes'"},
            'dish': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Dish']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Meal']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {})
        },
        'eo.mealinvitation': {
            'Meta': {'object_name': 'MealInvitation', 'db_table': "u'meal_invitation'"},
            'from_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invitation_from_user'", 'to': "orm['eo.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eo.Meal']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 4, 0, 0)'}),
            'to_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invitation_to_user'", 'to': "orm['eo.UserProfile']"})
        },
        'eo.order': {
            'Meta': {'object_name': 'Order', 'db_table': "u'order'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '12', 'unique': 'True', 'null': 'True'}),
            'completed_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['eo.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['eo.Meal']"}),
            'num_persons': ('django.db.models.fields.IntegerField', [], {}),
            'paid_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
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
            'tel2': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'restaurant'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
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
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'work_for': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'})
        }
    }

    complete_apps = ['eo']
    symmetrical = True
