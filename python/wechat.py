#coding=utf-8
import re
import os
import time
import sys
import cgi
import datetime 
import csv
from html.parser import HTMLParser
from html.entities import name2codepoint
from collections import namedtuple


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

        
class ChatList : 
    def __init__(self, source_path):
        self.items = [] # 所有的项目
        self._parse(source_path)
        
    def _parse(self, source_path) : 
        print("Load chats from : " + source_path +"\n")
        source = codecs.open(source_path, 'r', encoding = 'GBK', errors='ignore')
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
        pres_no = ''
        cur_name = u'None'
        cur_no = ''
        cur_count = 0 
        pres_count = 5
        for item in self.items : 
              if item.date == date and item.type == u'文本':
                if item.wechatNo == cur_no :
                    cur_count += 1 
                    if cur_count > pres_count :
                        pres_no = cur_no
                        pres_count = cur_count
                        cur_name = item.nickName 
                else :
                    cur_no = item.wechatNo 
                    cur_count = 0  
        return cur_name
    
    ## 获取当天的聊天记录列表
    def getItems(self, date):
        sub = []
        for item in self.items : 
            if item.date == date : 
                sub.append(item)
        return sub

        
## 聊天室
class Room: 
    # root_path = u'D:/iphone/李雄峰的 iPhone/微信消息记录/'
    def __init__(self, roomName, chatRootPath= u'D:/iphone/微信消息记录-jigsaw-payment/'):
        self.roomName = roomName 
        self.chatRootPath = chatRootPath

    def chats(self): 
        root_path = self.chatRootPath
        file_name = u'/表格格式/' + self.roomName + u'.xls'
        
        ## 寻找最近日期的xls文件
        ## 最新的文件路径
        last_folder = u' '
        for cur_folder in os.listdir(root_path):
            if cur_folder > last_folder  and  os.path.exists(root_path + cur_folder + file_name):
                last_folder = cur_folder            
        path = root_path + last_folder + file_name
        return ChatList(path)
        
    def members(self): 
        root_path = u'D:/cocolian/cocolian-static/data/member/'         
        ## 寻找最近日期的xls文件
        ## 最新的文件路径
        last_file = u' '
        for cur_file in os.listdir(root_path):
            if cur_file > last_file  and  cur_file.startswith(self.roomName):
                last_file = cur_file     
        return self._parseMembers(root_path+last_file)
        
    # 可用属性 
    # no,UserName, NickName, RemarkName, DisplayName,Sex,HeadImgUrl, 
    # VerifyFlag, OwnerUin, PYInitial,PYQuanPin,RemarkPYInitial,RemarkPYQuanPin,
    # StarFriend, AppAccountFlag, Statues,AttrStatus, Province, City, 
    # Alias,SnsFlag,UniFriend,KeyWord,EncryChatRoomId,IsOwner    
    def _parseMembers(self, source_path) : 
        print("Load members from : " + source_path +"\n")
        members = []
        ## source = codecs.open(source_path, 'r', encoding = 'gb2312', errors='ignore')
        with open(source_path, 'r', encoding = 'utf8', errors='ignore') as csvfile:
            f_csv = csv.reader(csvfile)
            headings = next(f_csv)
            Member = namedtuple('Member', headings)
            for r in f_csv:
                row = Member(*r)
                members.append(row._asdict())
        return members
        