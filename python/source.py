#coding=utf-8
import re
import os
import time
import sys
import cgi
import datetime 

import wechat
import codecs

class Exporter : 
    def __init__(self, room_name, target_folder):        
        self.target_folder = target_folder
        self.room = wechat.Room(room_name)
    
    ## 计算目标文件路径
    def targetPath(self, date) : 
        return '~/cocolian/cocolian-docs/source/'+ self.target_folder+'/_posts/'+ date + '-chat.markdown'
        

    def export(self, exp_days, to_date):
        ## 默认导出最近10天的聊天记录
        chatList = self.room.chats()
        thedate = to_date - datetime.timedelta(days=exp_days)

        while thedate < to_date : 
            datestr = thedate.strftime("%Y-%m-%d")
            self.__exportMarkdown(chatList, datestr, self.targetPath(datestr))
            thedate = thedate + datetime.timedelta(days = 1)
        return
    
    ## 输出markdown
    def __exportMarkdown(self, chatList, thedate, path) :  
        pres_name = chatList.getSpeaker(thedate) 
        items = chatList.getItems(thedate)
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
    to_date = datetime.datetime.now().date()
    if len(sys.argv)==3 :   
        to_date = datetime.datetime.strptime(sys.argv[2], "%Y%m%d").date()
    exporter = Exporter(u'支付产品技术交流群', 'proddev')
    exporter.export(exp_days,to_date)  
    exporter = Exporter(u'支付产品开发交流群', 'devarch')
    exporter.export(exp_days,to_date)
    exporter = Exporter(u'支付产品架构交流群', 'prodarch')
    exporter.export(exp_days,to_date)
