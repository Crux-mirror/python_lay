# -*- coding:UTF-8 -*-
import re

__author__ = 'crux'

''' re模块练习 '''

#macth练习
def re_match(pattern,s):
    ''' 总是从字符串头部开始匹配，返回字符串的match对象,匹配非开头部分字符串时，返回None
    字符串匹配，如果不匹配，返回None
    匹配返回原始字符串 group(0)==pattern'''
    re.match(pattern,s)



#sub练习
def re_sub(pattern,repl,s,count=0,flags=0):
    '''
    找到re匹配的所有子串，并用repl代替。可选参数
    count 必须为非负数，表示最大替换次数 0表示替换所有
    如果匹配成功，则返回替换后的字符串
    '''


#findall练习
def re_findall(pattern,s):
    '''
    从s中找到所有匹配的淄川，作为列表返回
    如果没有匹配，返回空数组，可用if判断 空数组为False
    '''

#search练习
def re_search(pattern,s,flags=0):
    """查找返回一个match对象，找不到返回None."""
    return re.search(pattern,s)


name = u'   因为回帖的人太少，说明没有多少人想听我说，或者说大家都对真相没有多少兴趣，来这<a href="http://jump2.bdimg.com/safecheck/index?url=x+Z5mMbGPAsY/M/Q/im9DR3tEqEFWbC4Yzg89xsWivTvlooZ+7Lq/iTMErHXu68VK4qTjgNeQuFPhkSMA4BCOOm/fZdF8lDP40ePTcjE3P+qplBjQfoaAchMZgfTf+uS"  class="ps_cb" target="_blank" onclick="$.stats.track(0,;$.stats"">贴吧</a>只不过是无聊或是扯淡的，那我还费那么大精力惹一群喷子喷我吗？<br>     如果没有超过100个回复想看的，我是不会发布《山海经》隐藏的真相的。<br>    我要看看有多少人愿意试着相信……'

d = re.compile('<a.*?>')
res = re.sub(d,'',name)
print res

