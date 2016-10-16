# coding: utf-8  
import urllib2
import cookielib
import re
from bs4 import BeautifulSoup
import socket
import urllib
import sys
import json

#
class SpiderOne(object):
    #编码判断
    def getCoding(self,strInput):
        #获取编码格式
        if isinstance(strInput, unicode):
            return "unicode"
        try:
            strInput.decode("utf8")
            return 'utf8'
        except:
            pass
        try:
            strInput.decode("gbk")
            return 'gbk'
        except:
            pass
    def tran2UTF8(self,strInput):
        #转化为utf8格式
        strCodingFmt = self.getCoding(strInput)
        if strCodingFmt == "utf8":
            return strInput
        elif strCodingFmt == "unicode":
            return strInput.encode("utf8")
        elif strCodingFmt == "gbk":
            return strInput.decode("gbk").encode("utf8")
    
    def insertBmobData(self,url,title,thumbnail,tags,content,yunInfo,torrent,magnet):
            requrl = 'http://cloud.bmob.cn/863972aa8cddda62/insertmoves'
            #基本配置
            #tags='mm'
            url=self.tran2UTF8(url)
            title=self.tran2UTF8(title)
            thumbnail=self.tran2UTF8(thumbnail)
            tags=self.tran2UTF8(tags)
            yunInfo=self.tran2UTF8(yunInfo)
            torrent=self.tran2UTF8(torrent)
    
            magnet=self.tran2UTF8(magnet)
            #content=self.tran2UTF8(content)
    
            table='Movies01'
            mfrom='电影首发站'
            values = {    "table":table,
                          "url":url,
                          "title":title,
                          "thumbnail":thumbnail,
                          "yunInfo":yunInfo,
                          "downInfo":'',
                          "yunUrl":'',
                          "torrent":torrent,
                          "magnet":magnet, 
                          "content":content, 
                          "yunAccount":'',
                          "mfrom":mfrom,
                          "classify":'',
                          "tags":tags
                                         }
            
            data = urllib.urlencode(values)
            response=urllib.urlopen(requrl,data)
            print response.read()
        #加入Bmob数据库  END
        
   
    #处理文章详情页
    def parseDetails(self,pageUrl,pageNumber):
        #baseUrl="http://www.mp4ba.com/show.php/%s"
        url=pageUrl
        socket.setdefaulttimeout(50) # 10 秒钟后超时 
        #创建请求的request
        response=urllib2.urlopen(url)
        if response.getcode()==200:            
            html_doc=response.read()
            soup = BeautifulSoup(html_doc, 'html.parser',from_encoding='utf-8')
            #判断页面上是否有百度云盘链接
            isyun=soup.find('a',href=re.compile(r"http://pan.baidu.com"))
            if isyun:
                print '本页面有百度云链接'
                print url
                print isyun
                #取得主内容区class="main shadow"
                showmain=soup.find('div',class_="main shadow")
                #标题h1
                title=showmain.find('h1').get_text()
                print title
                
                #处理标签class="affix"
                tags=''
                aTags=showmain.find('div',class_='affix').find_all('a',href=re.compile(r"tag/"))
                for a in aTags:
                    tags=tags.join(a.get_text())
                print tags
                
                
                #【3】解析文章内容
                #class="detail"
                content = showmain.find('div',class_="detail")
                content.find('div',class_='bdsharebuttonbox').decompose()
                content.find('div',class_='bdsharebuttonbox').decompose()
                content.find('script').decompose()
                #print content

    
                #解析文章中的所有图片地址
                #thumbnail默认值
                thumbnail='http://image.lfstorm.com/zx-logo.png-weixin'
                thumbnail=content.find('img')['src']
                #print thumbnail
                #处理yunInfo
                yunInfo =[]
                yunitem={
                    "url":"",
                    "text":"",
                }
                yunitem['url']=""
                yunitem['text']='文章中寻找'
                yunInfo.append(yunitem)
                
                #处理yunInfo
                magnet1 =[]
                magnetitem={
                    "url":"",
                    "text":"",
                }
                magnetitem['url']=''
                magnetitem['text']='暂未收录'
                magnet1.append(magnetitem)
                
                #处理yunInfo
                torrent1 =[]
                torrentitem={
                    "url":"",
                    "text":"",
                }
                torrentitem['url']=''
                torrentitem['text']='暂未收录'
                torrent1.append(torrentitem)
                yunInfo=json.dumps(yunInfo, encoding="UTF-8", ensure_ascii=False) 
                magnet=json.dumps(magnet1, encoding="UTF-8", ensure_ascii=False) 
                torrent=json.dumps(torrent1, encoding="UTF-8", ensure_ascii=False)
                print thumbnail
                print title
                print tags
                self.insertBmobData(url,title,thumbnail,tags,content,yunInfo,torrent,magnet)

            else:
                print "本页面没有百度云链接地址"
               
    
                #self.insertBmobData(indexUrl,thumbnail,post_title, post_content, downInfo,tags)
        #处理文章详情页 END
    
    
   
    
                   
    def craw(self,root_url):
	sys.getdefaultencoding()
	reload(sys)
	print sys.getdefaultencoding()
        baseUrl='http://www.dysfz.net/movie%s.html'
        #for pageNumber in range(7728,124854):
		#负责处理63689-80000
        for pageNumber in range(0,12100):
            pageUrl=baseUrl % pageNumber
            try:
                print '开始处理文章页面'
                self.parseDetails(pageUrl,pageNumber)
                print '处理文章页面结束'
            except Exception as e:
                print e
                print 'GetData[Fail];UrlAddress%s'%pageUrl
                   
       
    

if __name__=="__main__":
    indexUrl="http://pt.ishounimei.com/ziyuanliebiao.php"
    obj_spider = SpiderOne()
    obj_spider.craw(indexUrl)
   
    