#-*- coding:UTF-8 -*-

import urllib2
import urllib
import re

class Spider:
    #初始化变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        self.headers = {'User-Agent':self.user_agent}
        self.enable = False
        self.stories = []
    #获取一页的html
    def getPage(self,pageIndex):
        url = 'https://www.qiushibaike.com/text/page/'+str(pageIndex)
        request = urllib2.Request(url,headers=self.headers)
        try:
            response = urllib2.urlopen(request)
            codeHtml = response.read().decode('utf-8')
            return codeHtml
        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print u'连接失败，原因：',e.reason
                return None

    #通过正则表达式得到内容list
    def getRelist(self,pageIndex):
        codeHtml = self.getPage(pageIndex)
        if not codeHtml:
            print u'连接出错，页面加载失败。。。。'
            return None
        pattern =  re.compile('h2>(.*?)</h2>.*?<span>(.*?)</span.*?stats">.*?number">(.*?)</i>.*?<a .*?number">(.*?)</i>.*?</div>',re.S)
        items = re.findall(pattern,codeHtml)
        pageStories = []
        #每一页的段子集
        for item in items:
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR,'\n',item[1])
            pageStories.append([item[0].strip(),text.strip(),item[2].strip(),item[3].strip()])
        return pageStories
    #加载每一页到列表
    def loadPage(self):
        if self.enable == True:
            if len(self.stories)<2:
                pageStories = self.getRelist(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    #打印段子
    def catText(self,pageStories,page):
        for story in pageStories:
            inputs = raw_input()
            self.loadPage()
            if inputs == 'Q':
                self.enable = False
                return
            print u'第%d页\t发布人：%s\t赞：%s   评论：%s\n%s'%(page,story[0],story[2],story[3],story[1])

    #入口函数
    def start(self):
        print '正在读取嗅事百科，按回车查看新段子,Q退出'
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.catText(pageStories,nowPage)

spider = Spider()
spider.start()
