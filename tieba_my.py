# -*- coding:UTF-8 -*-

import re
import urllib2
import urllib

class Tool:
    removeAddr = re.compile('<a.*?a>| +')
    removeImg = re.compile('<img.*?>')
    removeBR = re.compile('<br><br>|<br>')
    def replace(self,x):
        x = re.sub(self.removeAddr,'',x)
        x = re.sub(self.removeBR,'\n',x)
        x =re.sub(self.removeImg,'',x)
        return x.strip()


class Shj:
    def __init__(self,bseURL,seeLz,floorTag):
        self.baseUrl = baseurl
        self.seeLz = '?see_lz='+str(seeLz)
        self.tool = Tool()
        self.file = None
        self.floorTag = floorTag
        self.floor = 1
        self.defaultTitle = u'百度贴吧'

    def getpage(self,pageNum):
        try:
            url = self.baseUrl+self.seeLz+'&pn='+str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print u'连接失败，错误原因：',e.reason
            return None
    def getPageNum(self,page):
        pattern = re.compile('<li class="l_reply_num".*?/span>.*?">(.*?)</span>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getTitle(self):
        page = self.getpage(1)
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getContent(self,page):
        pattern = re.compile('class="d_post_content j_d_post_content ">(.*?)</div>.*?<span class="tail-info">(.*?)</span>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            content = self.tool.replace(item[0])
            content = self.change_line(content)
            contents.append(content.encode('utf-8')+'\n')
        return contents

    def change_line(self,item):
        temp = []
        if len(item)> 40:
            for index in range(len(item)):
                if (item[index] != '\n'):
                    if index%40 == 0:
                        temp.append('\n')
                    temp.append(item[index])
        return ''.join(temp)


    def setFileTitle(self,title):
        if title is not None:
            self.file = open(title+'.txt','w')
        else:
            self.file = open(self.defaultTitle+'.txt','w')
    def w2txt(self,items):
        for item in items:
            if self.floorTag =='1':
                floorLine = '\n'+str(self.floor)+u"---------------------------------------------------------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1
    def start(self):
        indexPage = self.getpage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle()
        self.setFileTitle(title)
        if pageNum ==None:
            print 'URL已失效，请重试'
            return
        try:
            print '该帖子共有'+str(pageNum)+'页'
            for i in range(1,int(pageNum)+1):
                print '正在写入第'+str(i)+'页'
                page = self.getpage(i)
                contents = self.getContent(page)
                self.w2txt(contents)
        except IOError,e:
            print '写入异常,原因：',e.message
        finally:
            print '写入任务完成'
            self.file.close()



baseurl = 'https://tieba.baidu.com/p/4348888676'
seeLz = raw_input('是否只获取楼主信息，是输入1，否输入0\n')
floorTag = raw_input('是否写入楼层信息，是输入1，否输入0\n')
shj = Shj(baseurl,seeLz,floorTag)
shj.start()