"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
import urllib
import urllib2
import simplejson
from django.test.client import Client

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

class JSonClientTest(TestCase):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())

    #dumps data to json format and send to url
    def sendJSon(self, url, data):
        data_json = simplejson.dumps(data)
        req = urllib2.Request(url, data_json, {'content-type': 'application/json'})
        #req = urllib2.Request("http://localhost:8000/get_restaurant_list_by_geo/?longitude=30.273025&latitude=120.163314&range=500")
        response_stream = self.opener.open(req)
        response = response_stream.read()
        return response

    def login(self, username, password):
        url = "http://localhost:8000/user_login/"
        data={"username":username, "password":password}
        reqest = urllib2.Request(url, urllib.urlencode(data))
        response_stream = self.opener.open(reqest)
        response = response_stream.read()
        print response
        return response
        
    def test_create_order(self):
        c = Client()
        response = c.post("/user_login/",{"username":"xuaxu", "password":"1qaz2wsx"})
        print response.content
        '''self.login("xuaxu","1qaz2wsx")
        url = "http://localhost:8000/make_order/"
        data={"restaurant_id":25, "num_persons":2, "table_name":2}
        dishes=[{"dish_id":1,"quantity":1},
                {"dish_id":2,"quantity":3},
                {"dish_id":3,"quantity":2.5},
                {"dish_id":4,"quantity":0.5},]
        data["dishes"]=dishes
        print self.sendJSon(url, data)'''
        
