#!/usr/bin/python
#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding( "utf8" )

import codecs

import itchat
from itchat.content import *

#name = ' '
roomslist = []

itchat.auto_login(hotReload=False)

itchat.dump_login_status() # 显示所有的群聊信息，默认是返回保存到通讯录中的群聊

room_name = u'支付产品架构交流群'

room = itchat.search_chatrooms(name='支付产品架构交流群')[0]

print('Updating room , UserName: ' + room.UserName +',' + room.NickName +'\n')

chat_room =  itchat.update_chatroom(room['UserName'], detailedMember=True)

print('Exporting room , UserName: ' + room.UserName +',' + room.NickName +'\n')

path = 'D:/' + room_name + '.txt'

target = codecs.open(path, 'w', encoding = 'utf-8', errors='ignore')	

target.write('UserName,\t NickName ,\t RemarkName,\tDisplayName \n')
for mem in chat_room['MemberList']:
	target.write(mem['UserName'] + ",\t" + mem['NickName']+ ",\t" + mem['RemarkName'] + ",\t"+ mem['DisplayName'] + '\n')	
	
target.flush()
target.close()

print('Exported contract list to ' + path +'\n')

# for n in roomslist:
#	ChatRoom = itchat.update_chatroom(getroom_message(n), detailedMember=True)
#	for mem in ChatRoom['MemberList']:
#		target.write(mem['Province']+"\t"+mem['NickName']+"\t"+mem['RemarkName']'\n')
# target.close()

# for i in ChatRoom:
#     print(i['MemberList']['ContactList'])
#     count += 1
# print(count)

# # @itchat.msg_register(TEXT)
# # def simple_reply(TEXT):
# #     print(msg.text)
# #
# # itchat.auto_login(enableCmdQR = False,hotReload = True)  # enableCmdQR=True这一参数为二维码在下面控制台中显示出来，而不是用图片显示
# # itchat.run()
# itchat.auto_login(enableCmdQR = False)
#
# # time.sleep()
# # itchat.logout()
# # friends = itchat.get_friends()
# # for i in friends:
# #     print(i)
# rooms = itchat.get_chatrooms()
# for i in rooms:
#     print(i['NickName'])
#     memberList = itchat.update_chatroom(i['NickName'])
#     print (memberList)
#
# #     room = itchat.update_chatroom(i['NickName'],detailedMember = True)
# #     print(room)
# #     # for i in room:
# #     #     print(i)