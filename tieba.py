# -*- coding:UTF-8 -*-

import urllib2
import urllib
import re

#处理页面标签类
class Tool:
    #去除img标签，7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddr = re.compile('<a.*?/a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<p.*?')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeAddr,'',x)
        x = re.sub(self.removeExtraTag,'',x)
        x = re.sub(self.removeImg,'',x)
        x = re.sub(self.replaceBR,'\n',x)
        x = re.sub(self.replaceLine,'\n',x)
        x = re.sub(self.replacePara,'\n',x)
        x = re.sub(self.replaceTD,'\t',x)
        return x.strip()

class BDTB:
    #初始化，基地址、参数
    def __init__(self,baseUrl,seeLZ):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz='+str(seeLZ)
        self.tool = Tool()
        self.file = None
        self.floor = 1
        self.defaultTitle = u'百度贴吧'
      #  self.floorTag = floorTag
    #传入页码，获取Html
    def getPage(self,pageNum):
        try:
            url = self.baseURL+self.seeLZ+'&pn='+str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print u'连接失败，错误原因：',e.reason
                return None
    #获取帖子标题
    def getTitle(self,page):
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None
    #获取帖子页数
    def getPageNum(self,page):
        pattern = re.compile('<li class=l_reply_num.*?><span.*?>(.*?)</span>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None
    #获取每一层楼的内容，传入页面内容
    def getContent(self,page):
        pattern = re.compile('d_post_content j_d_post_content ">(.*?)</div>',re.S)
        items = re.findall(pattern,page)
        for item in items:
            print self.tool.replace(item)

baseURL = 'https://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseURL,1)
s = bdtb.getTitle(bdtb.getPage(1))
bdtb.getContent(bdtb.getPage(1))