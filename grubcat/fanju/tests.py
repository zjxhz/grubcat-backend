"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
import base64
import json
import os
import urllib2
        
class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}
#
# class JSonClientTest(TestCase):
#     opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
#     c = Client()
#     fixtures = ['test_data.json']
#
#     def get_base64_str(self, file_path):
#         f1 = open(file_path)
#         output='temp_base64.txt'
#         f2 = open(output, 'wb')
#
#         base64.encode(f1, f2)
#         f1.close()
#         f2.close()
#         f2 = open(output)
#         base64_str = f2.read()
#         f2.close()
#         os.remove(output)
#         return base64_str
#
#     def test_create_meal(self):
#         file_name='test.jpg'
#         base64_img=self.get_base64_str('/home/wayne/workspace/curl_tests/' + file_name)
#         data = {"host":"/api/v1/user/1/",
#                 "introduction":"test",
#                 "min_persons":5,
#                 "photo":{'file':base64_img,
#                          'content_type':'image/jpg',
#                          'name':file_name,
#                          },
#                 "list_price":32,
#                 "privacy":0,
#                 "restaurant":"/api/v1/restaurant/26/",
#                 "time":"2012-04-03T18:00:00",
#                 "topic":"what topic",
#                 "type":0,
#                 "order":{"table":"2",
#                          "dishes":[{"id":1,"quantity":2.5},{"id":2,"quantity":3}],
#                          "num_persons":-1
#                          }
#                 }
#         response = self.c.post('/api/v1/meal/',json.dumps(data), content_type='application/json')
#         self.assertEqual(response.status_code, 201, "Failed to create meal, code: %s" % response.status_code)

class ClientTest(TestCase):

    client = Client()

    def setUp(self):
        self.settings(DEBUG=True)

    def assertNotErrorPage(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('"error-page"', response.content)

    def test_index(self):
        r = self.client.get('/')
        self.assertNotErrorPage(r)

    def test_meal_list(self):
        r = self.client.get('/meal/')
        self.assertNotErrorPage(r)

    def test_user_list(self):
        r = self.client.get('/user/')
        self.assertNotErrorPage(r)
