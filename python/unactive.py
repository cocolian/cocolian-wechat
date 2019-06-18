#!/usr/bin/python
#coding:utf-8

import re
import os
import time
import sys
import cgi
import chardet
import csv
import codecs
import wechat

## 名称比较
        
class NameComparator:
    
    def __init__(self):
        try:
            self.emoj = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            self.emoj = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

        self.chinese_punc = re.compile(u"[\s+\.\!\/\_\,\$\%\^\*\(\+\"\'\]\+\|\[\+\—\——\！\，\。\？\、\~\、\～\@\#\￥\%\…\。\&\*（）：；《）《》“”\(\)\»〔〕\-]")
        self.none_chinese = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
        
    def filter(self, desstr):
        res = desstr.replace(u'&nbsp;', u'')
        res = res.replace(u'&amp;', u'')
        res = re.sub(self.emoj, u'', res)
        res = re.sub(self.chinese_punc,u'', res)
        res = re.sub(self.none_chinese, u'', res) 
        res = re.sub(u' ', u'', res)
        return res
    
    def equals(self, ra, rb ):
        if ra is None or len(ra)==0:
            return False
        if rb is None or len(rb)==0:
            return False
        if ra.strip() == rb.strip() :
            return True                     
        a = self.filter(ra.strip())
        b = self.filter(rb.strip())
        if a == b :
            return True         
        return False;

class FrequenceExporter : 
    def __init__(self, room_name):       
        ## chat_path = u'D:\iphone\微信消息记录-jigsaw-payment'
        self.room = wechat.Room(room_name)        
        self.target_path = 'D:/cocolian/cocolian-static/data/frequence/' + room_name + '-' + time.strftime("%Y%m%d", time.localtime()) + ".csv"        
        self.freq ={}
        self.last = {}
        self.names = {}
        self.members = []
        self.comparator = NameComparator() 
        
    def export(self) :
        self._calculate()
        self._merge()
        self._write()
        print('unmatched names: ' + str(self.names))
        
    def _calculate(self) :      
        for chat in self.room.chats().items : 
            if chat.wechatNo in self.freq : 
                self.freq[chat.wechatNo] += 1 
            else :
                self.freq[chat.wechatNo] = 1        
            if chat.wechatNo in self.names : 
                self.names[chat.wechatNo].add(chat.nickName)
            else :
                self.names[chat.wechatNo] = set()
                self.names[chat.wechatNo].add(chat.nickName)
            self.last[chat.wechatNo] = chat.dateTime
            
    def _merge(self) :      
        for mem in self.room.members() :
            wechatNo = self._matchWechatNo(mem)
            if wechatNo is None : 
                mem['Frequence'] = 0
                mem['LastTime'] = ''
                mem['WechatNo'] = ''
                mem['names'] =  ''
            else : 
                mem['Frequence'] = self.freq[wechatNo]
                mem['LastTime'] = self.last[wechatNo]
                mem['names'] = str(self.names[wechatNo])
                mem['WechatNo'] = wechatNo
                del self.names[wechatNo]
            self.members.append(mem)
            
                
    def _write(self) :
        csvfile = codecs.open(self.target_path, 'w', encoding = 'utf-8', errors='ignore')   
        writer = csv.DictWriter(csvfile, extrasaction='ignore', fieldnames=['NickName','RemarkName','DisplayName', 'names', 'WechatNo','Frequence','LastTime'])           
        writer.writeheader()
        for mem in self.members:
            writer.writerow(mem)
        csvfile.flush()
        csvfile.close()
        print('Exported contract list to ' + self.target_path +'\n')
    
    def _matchWechatNo(self, mem) :
        for wechatNo,names in self.names.items() : 
            for name in names : 
                if self._matchName(mem, name) :
                    return wechatNo

    def _matchName(self, mem, name): 
        match_props = ['NickName', 'RemarkName', 'DisplayName', 'UserName']
        for prop in match_props :
            if self.comparator.equals(mem[prop], name) :
                return True
        return False
                
if __name__ == "__main__":    
   # for room_name in [ u'支付产品架构交流群', u'支付产品开发交流群']
        exporter = FrequenceExporter(u'支付产品架构交流群')
        exporter.export()

        exporter = FrequenceExporter( u'支付产品开发交流群')
        exporter.export()
