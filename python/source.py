#coding=utf-8
import re
import os
import time
import sys
import cgi
import datetime 
from html.parser import HTMLParser
from html.entities import name2codepoint

## reload(sys) 
## sys.setdefaultencoding('utf8')

import codecs



class Item:
    def __init__(self):
        self.wechatId = ''      # 微信Id
        self.dateTime = ''      # 发言时间
        self.nickName = ''      # 昵称
        self.wechatNo = ''      # 微信号
        self.status = ''        # 状态
        self.type   = ''        # 类型
        self.content = ''       # 发言内容
        self.link   = ''        # 如果类型是“网页”，这里是链接的地址；
    
    ## 是否是当天的聊天记录
    @property
    def date(self): 
        return self.dateTime[0:10] 

    @property
    def time(self):
        return self.dateTime[11:].strip()
    
    @property
    def imagePath(self):
        return 'http://static.cocolian.cn/img/'+ self.date.replace('-', '')+'_'+ self.time.replace(':','') + '.png'

        
class Parser : 
    def __init__(self):
        self.items = [] # 所有的项目
        
    def parse(self, source_path) : 
        source = codecs.open(source_path, 'r', encoding = 'gb2312', errors='ignore')
        ## 聊天内容总数；
        line_count = 0; 
        ## 发言频率, 连续发言5次以上，就当做嘉宾了。 
        ## 计算发言最多的人，作为嘉宾
        pres_name = 'PaymentGroup'
        cur_name = 'PaymentGroup'
        cur_count = 0 
        pres_count = 5
        is_link = False
        item = Item()
        for line in source :
            ## 网页 类型的连接地址是放在单独的一行
             if is_link : 
               pos_end = line.find('</td>')
               item.link = cgi.escape(line[0:pos_end])
               is_link = False          
             if len(line)>690 and line[63:67] == 'xl24':                    
                item = Item()
                pos_start = line.find('x:str>', 0) + 6
                pos_end = line.find('</td>', pos_start)
                item.wechatId = line[pos_start:pos_end]
                
                pos_start = line.find('x:str>', pos_end+5) + 6
                pos_end = line.find('</td>', pos_start)
                item.dateTime = line[pos_start:pos_end]             

                pos_start = line.find('x:str>', pos_end+5) + 6
                pos_end = line.find('</td>', pos_start)
                item.nickName = line[pos_start:pos_end]

                pos_start = line.find('x:str>', pos_end+5) + 6
                pos_end = line.find('</td>', pos_start)
                item.wechatNo = line[pos_start:pos_end]

                pos_start = line.find('x:str>', pos_end+5) + 6
                pos_end = line.find('</td>', pos_start)
                item.status = line[pos_start:pos_end]

                pos_start = line.find('x:str>', pos_end+5) + 6
                pos_end = line.find('</td>', pos_start)
                item.type = line[pos_start:pos_end]
                
                if item.type == u'网页':
                    pos_start = line.find('x:str>', pos_end+5) + 6
                    item.content = cgi.escape(line[pos_start:])
                    is_link = True
                else :
                    pos_start = line.find('x:str>', pos_end+5) + 6
                    pos_end = line.find('</td>', pos_start)
                    item.content = cgi.escape(line[pos_start:pos_end])
                    is_line = False
                self.items.append(item)
                
        source.close()
        return
        
    ## 嘉宾
    def getSpeaker(self, date): 
        ## 发言频率, 连续发言5次以上，就当做嘉宾了。 
        ## 计算发言最多的人，作为嘉宾
        pres_name = 'PaymentGroup'
        cur_name = 'PaymentGroup'
        cur_count = 0 
        pres_count = 5
        for item in self.items : 
              if item.date == date and item.type == u'文本':
                if item.nickName == cur_name :
                    cur_count += 1 
                    if cur_count > pres_count :
                        pres_name = cur_name
                        pres_count = cur_count
                else :
                    cur_name = item.nickName 
                    cur_count = 0 
        return pres_name
    
    ## 获取当天的聊天记录列表
    def getItems(self, date):
        sub = []
        for item in self.items : 
            if item.date == date : 
                sub.append(item)
        return sub


class Exporter : 
    def __init__(self, file_name, target_folder):        
        self.root_path = u'D:/iphone/微信消息记录-jigsaw-payment/'
        # self.root_path = u'D:/iphone/李雄峰的 iPhone/微信消息记录/'
        self.target_folder = target_folder
        self.file_name = file_name
        self.parser = Parser()
    
    ## 计算目标文件路径
    def targetPath(self, date) : 
        return 'D:/cocolian/cocolian-docs/source/'+ self.target_folder+'/_posts/'+ date + '-chat.markdown'
        
    ## 寻找最近日期的xls文件
    ## 最新的文件路径
    def sourcePath(self) :
        last_folder = u' '
        for cur_folder in os.listdir(self.root_path):
            if cur_folder > last_folder  and  os.path.exists(self.root_path + cur_folder + self.file_name):
                last_folder = cur_folder            
        return self.root_path + last_folder + self.file_name

    def export(self, exp_days):
        ## 默认导出最近10天的聊天记录
        source_path = self.sourcePath();      
        print('从文件导出：'+ source_path +'\n')      
        self.parser.parse(source_path);
        thedate = datetime.datetime.now().date() - datetime.timedelta(days=exp_days)

        while thedate < datetime.datetime.now().date() : 
            datestr = thedate.strftime("%Y-%m-%d")
            self.__exportMarkdown(datestr, self.targetPath(datestr))
            thedate = thedate + datetime.timedelta(days = 1)
        return
    
    ## 输出markdown
    def __exportMarkdown(self, thedate, path) :  
        pres_name = self.parser.getSpeaker(thedate) 
        items = self.parser.getItems(thedate)
        if len(items) < 2 :
            return
            
        target = codecs.open(path, 'w', encoding = 'utf-8', errors='ignore')
        target.write(u'---\n')              
        target.write(u'layout:     source \n')                        
        target.write(u'title:      "' + thedate + '-WeChat"\n')
        target.write(u'date:       '+  thedate +' 12:00:00\n')
        target.write(u'author:     '+ pres_name +'\n')
        target.write(u'lines:      '+ str(len(items)) +' \n') 
        target.write(u'tag:       [chat]\n')                        
        target.write(u'---\n')              

        is_link = False
        
        for item in items : 
            is_link = False
            target.write(u'> ')
            target.write(item.time)
            target.write(u'  ')
            target.write(item.nickName)
            target.write(u'  \n   \n')              
            if item.type == u'文本':
                target.write(item.content + u'  \n   \n')
            if item.type == u'网页':
                target.write(u'['+item.content+'](' + item.link + ')' + u'  \n   \n')
            if item.type == u'图片':                        
                target.write('!['+ item.dateTime + ']('+ item.imagePath + ') \n   \n')
            if item.type == u'照相壁纸':                        
                target.write('!['+ item.dateTime + ']('+ item.imagePath + ') \n   \n')


        target.flush()
        target.close()

        print('完成导出：'+ path +'\n')
        return
    
if __name__ == "__main__":      
    exp_days = 10 
    if len(sys.argv)==2 :
        exp_days = int(sys.argv[1])
    exporter = Exporter(u'/表格格式/支付产品技术交流群.xls', 'proddev')
    exporter.export(exp_days)  
    exporter = Exporter(u'/表格格式/支付产品开发交流群.xls', 'devarch')
    exporter.export(exp_days)
    exporter = Exporter(u'/表格格式/支付产品架构交流群.xls', 'prodarch')
    exporter.export(exp_days)