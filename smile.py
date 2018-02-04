#-*- coding: UTF-8 -*-

import urllib2
import urllib
import re


#爬虫类
class Spider:
    #初始化方法，定义变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        #初始化headers
        self.headers = {'User-Agent':self.user_agent}
        #存放段子的变量，每一个元素是每一页的段子子集
        self.stories = []
        #存放程序是否继续运行的变量
        self.enable = False
    #传送某一页的索引活页页面代码
    def getPage(self,pageIndex):
        try:
            url = 'https://www.qiushibaike.com/text/page/'+str(pageIndex)
            #构建请求的request
            request = urllib2.Request(url,headers=self.headers)
            #利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            #页面转码
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print '连接失败：',e.reason
                return None
    #传入某一页代码，返回不带图片的段子列表
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print '页面加载失败.....'
            return None
        pattern = re.compile('h2>(.*?)</h2>.*?<span>(.*?)</span.*?stats">.*?number">(.*?)</i>.*?<a .*?number">(.*?)</i>.*?</div>',re.S)
        items = re.findall(pattern,pageCode)
        #用来存储每页的段子集
        pageStories = []
        #遍历正则表达式匹配的信息
        for item in items:
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR,'\n',item[1])
            pageStories.append([item[0].strip(),text.strip(),item[2].strip(),item[3].strip()])
        return pageStories

    #加载提取额页面的内容，加到列表中
    def loadPage(self):
        #如果当前未看的页数小于2页，则加载新的一页
        if self.enable == True:
            if len(self.stories)<2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    #调用方法，每次回车输出一个段子
    def getOneStory(self,pageStories,page):
        for story in pageStories:
            inputs = raw_input()
            self.loadPage()
            if (inputs == 'Q')|(inputs == 'q'):
                self.enable = False
                return
            print u'第%d页\t发布人：%s\t赞：%s   评论：%s\n%s'%(page,story[0],story[2],story[3],story[1])

    #开始方法
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
                self.getOneStory(pageStories,nowPage)

spider = Spider()
spider.start()
