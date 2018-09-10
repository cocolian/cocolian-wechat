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


room_name = u'支付产品技术交流群'
# room_name = u'支付技术架构交流群'

try:
    emoj = re.compile(u'[\U00010000-\U0010ffff]')
except re.error:
    emoj = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

chinese_punc = re.compile(u"[\s+\.\!\/\_\,\$\%\^\*\(\+\"\'\]\+\|\[\+\—\——\！\，\。\？\、\~\、\～\@\#\￥\%\…\。\&\*（）：；《）《》“”\(\)\»〔〕\-]")

def filter_str(desstr):
    '''
    过滤表情
    '''
    res = re.sub(emoj, u'', desstr)
    res = re.sub(chinese_punc,u'', res)
    res = re.sub(u' ', u'', res)
    return res
    
def name_eq(ra,rb):
    if ra is None or len(ra)==0:
        return False
    if rb is None or len(rb)==0:
        return False
    a = filter_str(ra)
    b = filter_str(rb)
    if a == b :
        return True         
    return False;

def is_member_name(mem, name):
    if mem is None :
        return False
    if (name is None) or len(name)==0 : 
        return False;
    return name_eq(mem['UserName'],name) or name_eq(mem['NickName'],name) or name_eq(mem['RemarkName'],name) or name_eq(mem['DisplayName'],name)

################################################################

## 导出路径
root_path = u'D:/iphone/李雄峰的 iPhone/微信消息记录/'

## 最新的文件路径
last_folder = u' '

## 文件相对路径的位置
sub_path = u'/表格格式/'+ room_name + '.xls'

## 寻找最近日期的xls文件

for cur_folder in os.listdir(root_path):
    if cmp(cur_folder, last_folder)>0 and  os.path.exists(root_path + cur_folder + sub_path):
        last_folder = cur_folder

        
unpath = root_path + last_folder + sub_path

print('使用最新文件: '+ unpath +'\n')

## unpath = unicode(inpath, "utf8")

source=open(unpath)
            
freq ={}
last = {}
names = {}
try:
    for line in source:
        if len(line)>690 and line[63:67] == 'xl24':
            datetime=line[233:252]
            date = line[233:243]
            time = line[244:252]
            
            pos_end = line.find('</td>', 335)
            name = line[335: pos_end].decode('gbk', errors='ignore')
            

            pos_start = line.find('x:str>', pos_end+5) + 6
            pos_end = line.find('</td>', pos_start)
            wechat_no = line[pos_start:pos_end]           
            
            if (wechat_no is not None) and (name is not None) and (wechat_no is not None) :
                if freq.has_key(wechat_no) :
                    freq[wechat_no] += 1 
                else :
                    freq[wechat_no] = 1
                        
                last[wechat_no] = datetime 
                names[wechat_no] = name
finally:
     source.close()



roomslist = []

itchat.auto_login(hotReload=False)

itchat.dump_login_status() # 显示所有的群聊信息，默认是返回保存到通讯录中的群聊

friends = itchat.get_friends(update=True)

room = itchat.search_chatrooms(name=room_name)[0]


print('Updating room , UserName: ' + room.UserName +',' + room.NickName +'\n')

chat_room =  itchat.update_chatroom(room['UserName'], detailedMember=True)

print('Exporting room , UserName: ' + room.UserName +',' + room.NickName +'\n')

path = 'D:/' + room_name + '-all.txt'

target = codecs.open(path, 'w', encoding = 'utf-8', errors='ignore')    

target.write('UserName,\t NickName ,\t RemarkName,\tDisplayName,\twechat_no,\tname,\tfreq,\tLastTime \n')


for mem in chat_room['MemberList']:
    target.write(mem['UserName'] + ",\t" + mem['NickName']+ ",\t" + mem['RemarkName'] + ",\t"+ mem['DisplayName'] )
    matched = False;
    my_mem = itchat.search_friends(userName=mem['UserName'])    
    
    matched_no = None
    for wechat_no in names:
        if  is_member_name(mem, names[wechat_no]) :
            matched_no = wechat_no            
            break
        if  is_member_name(my_mem, names[wechat_no]):
            matched_no = wechat_no          
            break

    if matched_no is None :
        target.write(",\t,\t,\t,\t")
    else :                 
        target.write(",\t"+ matched_no + ",\t"+ names[matched_no] + ",\t" + str(freq[matched_no]) +",\t"+ last[matched_no] )
    
    target.write('\n')

target.flush()
target.close()
print('Exported contract list to ' + path +'\n')


print('完成导出：'+ path + ' \n')