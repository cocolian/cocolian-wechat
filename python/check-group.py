#!/usr/bin/python
#coding:utf-8

import re
import os
import time
import sys
import cgi
import chardet
import itertools

reload(sys)
sys.setdefaultencoding( "utf8" )

import codecs

import itchat
from itchat.content import *


def mem_equal(src, dest):
    return src['UserName'] == dest['UserName']

src_room_name = u'金融@头条'
# room_name = u'支付技术架构交流群'

dest_room_names = [u'支付产品技术交流群', u'支付产品架构交流群', u'支付产品开发交流群']

itchat.auto_login(hotReload=False)

itchat.dump_login_status() # 显示所有的群聊信息，默认是返回保存到通讯录中的群聊

friends = itchat.get_friends(update=True)

src_room = itchat.search_chatrooms(name=src_room_name)[0]

src_room =  itchat.update_chatroom(src_room['UserName'], detailedMember=True)

print('Exporting room , UserName: ' + src_room.UserName +',' + src_room.NickName +'\n')

dest_rooms = []

for room_name in dest_room_names : 
    dest_room = itchat.search_chatrooms(name=room_name)[0]
    dest_room =  itchat.update_chatroom(dest_room['UserName'], detailedMember=True)
    dest_rooms.append(dest_room)
    print('Exporting room , UserName: ' + dest_room.UserName +',' + dest_room.NickName +'\n')

for mem in src_room['MemberList']:
    same = [] 
    for room in dest_rooms : 
        for dest in room['MemberList']:
            if mem_equal(mem, dest): 
                same.append(room)
                break
    if len(same) >0 :
        print(mem['NickName']+ "[" + mem['RemarkName'] + "]["+ mem['DisplayName']+'] : ')
        for room in same :
            print('  ' + room['NickName'])
        print('\n')

print('完成！')