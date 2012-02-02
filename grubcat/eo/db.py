# -*- coding: utf-8 -*-
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import random
import uuid
import os
import logging
import simplejson
from types import NoneType
from django.http import HttpResponse
from grubcat.eo.models import Restaurant
from grubcat.eo.models import Dish

def getWebPageContent(url, useProxy=True):
    if useProxy == True:
        proxy_support = urllib2.ProxyHandler({'http':'http://10.159.32.155:8080'})
        opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)  
    f = urllib2.urlopen(url)
    content = f.read()
    f.close()
    return content

def getRestaurantList(url):
    print 'fetching store list from ' + url
    html = getWebPageContent(url, True)
    print 'done, analyzing...'
    soup = BeautifulSoup(html)  
    storeInfoList = soup.findAll('div', {"class":"store-info"})
    for storeInfo in storeInfoList:
        storeLink = storeInfo.div.a['href']
        html = getWebPageContent(storeLink, False)
        soup = BeautifulSoup(html)
        r = Restaurant()
        r.name = soup.find('div', {"class":"store-title"}).find('h1').string
        # use nextSibling twice to skip some spaces
        r.address = soup.find('a', {"data-kind":"kb.hznewstore.detail.evaluate"}).parent.nextSibling.nextSibling.find('span').string
        averageCost = soup.find('p',{"class":"firstp"}).findAll('em')[0].string
        rating = soup.find('p',{"class":"firstp"}).findAll('em')[1].string
        r.average_cost = averageCost[0:len(averageCost) - 1]
        r.rating = rating[0:len(rating) - 1]
        # tel
        telUrl = soup.find('img',{"class":"tel"})['src']
        telImgPath = "eo/img/tel/" + str(uuid.uuid1()) + ".jpg";
        # urllib.urlretrieve(telUrl, telImgPath)
        output = open(telImgPath,'wb')
        output.write(urllib2.urlopen(telUrl).read())
        output.close()
        r.phone_img_url = telImgPath
        r.save()
        print "restaurant " + r.name + ', id: ' + str(r.id) + ' saved'
        dishNumber = 0;
        for dishSoup in soup.findAll('a', {"data-kind":"kb.hznewstore.detail.recommendmore"}):
            dishNumber = dishNumber + 1
            dish = Dish()
            dish.number = dishNumber
            dish.name = dishSoup.span.string
            dish.price = random.randint(3, 64) # random price
            print 'setting restaurant_id: ' + str(r.id)
            dish.restaurant_id = r.id
            dish.save()
            r.dish_set.add(dish)
        print str(dishNumber) + " dishes saved to DB"
        print

def deleteOldData():
    for fname in os.listdir('eo/img/tel/'):
        print 'removing ' + fname
        os.remove('eo/img/tel/' + fname)
    Restaurant.objects.all().delete()
    Dish.objects.all().delete()
    
def gendata(request):
    deleteOldData()    
    pageIndex=1
    while pageIndex <= 1:
        url='http://bendi.koubei.com/search/searchstore.html?city=2595&option.cpurl=1001402&option.navcat=1001402&page='+str(pageIndex)+'#anchor-search'
        getRestaurantList(url)
        pageIndex = pageIndex + 1
    return HttpResponse("Data generated to DB")

def updateLatLng(request):
    for r in Restaurant.objects.all():
        city = u'中国浙江省杭州市'
        city = urllib.quote(city.encode('utf-8'))
        name = urllib.quote(r.name.encode('utf-8'))
        url = 'http://ajax.googleapis.com/ajax/services/search/local?v=3.0&q="%s%s"' % (city, name)
        html = getWebPageContent(url, True)
        simplejson.loads(html)
        results = simplejson.loads(html)['responseData']['results']
        if results:
            firstMatch = results[0]
            r.longitude = float(firstMatch['lat'])
            r.latitude = float(firstMatch['lng'])
            if firstMatch.get('phoneNumbers') == NoneType:
                count = 1
                print 'emplty phone'
                for phoneNumber in firstMatch['phoneNumbers']:
                    if(count == 1):
                        r.tel = phoneNumber['number']
                    elif(count == 2):
                        r.tel2 = phoneNumber['number']
                    else:
                        break;
                    count = count + 1
            r.save()
        else:
            logging.warn('Cannot find lat and lng for %s' % r.id)
    return HttpResponse('OK check the console for detail')
    
