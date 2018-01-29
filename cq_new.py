#coding=utf-8
import urllib
import urllib2
import re

url = 'https://www.qiushibaike.com/hot/'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
headers = {'User-Agent':user_agent}
request = urllib2.Request(url,headers = headers)
response = urllib2.urlopen(request)
#print response.read().decode('utf-8')
partten = '<div.*?author clearfix".*?><.*?content">.*?span>(.*?)</span>'
temp = re.compile(partten,re.S)
items = re.findall(temp,response.read())
for item in items:
    print item
