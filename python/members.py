#!/usr/bin/python
#coding:utf-8

import re
import os
import io
import time
import sys
import cgi
import itertools
import codecs
import itchat
import csv
from itchat.content import *


################################################################

class RoomExporter : 
    def __init__(self):
        # room_name = u'支付产品技术交流群'
        # room_name = u'支付技术架构交流群'
        ## 导出路径
        self.root_path = u'D:/cocolian/cocolian-static/data/member/'
        self.properties = ['UserName','NickName','RemarkName','DisplayName', 'Sex', 'HeadImgUrl','VerifyFlag', 'OwnerUin', 'PYInitial', 'PYQuanPin', 'RemarkPYInitial', 'RemarkPYQuanPin', 'StarFriend', 'AppAccountFlag', 'Statues', 'AttrStatus', 'Province', 'City', 'Alias', 'SnsFlag', 'UniFriend', 'KeyWord', 'EncryChatRoomId', 'IsOwner']
    
    def export(self, room_names) :      
        itchat.auto_login(hotReload=False)
        itchat.dump_login_status() # 显示所有的群聊信息，默认是返回保存到通讯录中的群聊
        friends = itchat.get_friends(update=True)
        for room_name in room_names : 
            room = itchat.search_chatrooms(name = room_name)[0]
            print('Updating room , UserName: ' + room.UserName +',' + room.NickName +'\n')
            chat_room =  itchat.update_chatroom(room['UserName'], detailedMember=True)          
            path = self.root_path + room['NickName'] + time.strftime("%Y%m%d", time.localtime()) + ".csv"           
            csvfile = codecs.open(path, 'w', encoding = 'utf-8', errors='ignore')   
            writer = csv.DictWriter(csvfile, extrasaction='ignore', fieldnames=self.properties)           
            writer.writeheader()
            for mem in chat_room['MemberList'] :
                writer.writerow(mem)
            csvfile.flush()
            csvfile.close()
            print('Exported contract list to ' + path +'\n')
        print('完成导出! \n')
        return
 
 
if __name__ == "__main__":      
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
    exporter = RoomExporter()
    exporter.export([u'支付产品技术交流群', u'支付产品开发交流群', u'支付产品架构交流群'])
