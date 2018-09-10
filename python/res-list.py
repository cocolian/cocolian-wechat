#coding=utf-8
import re
import os
import time
import sys
import cgi
import datetime 
import collections

reload(sys) 
sys.setdefaultencoding('utf8')

import codecs


## 导出资料
names = collections.OrderedDict()
names['bin']  = '卡bin和重要数据'
names['law']  ='政策法规'
names['book'] ='必读书籍'
names['nifa'] ='互金协会'
names['pbc']  ='央行'
names['cup']  ='银联'
names['nucc'] ='网联'
names['aml'] = '反洗钱'
names['product']='产品文档'
names['vision']='行业报告'
names['pingplusplus']='Ping++'
names['blockchain']='区块链'
names['design']='技术文档'
names['alibaba']='Alibaba'
names['barclays']='巴克莱银行'
names['nlp']='自然语言处理'
names['provisions']='备付金报表'
names['rcbfcc']='农信银'

target_path = r'D:/cocolian/cocolian-docs/resources/index.html'
target = codecs.open(target_path, 'w', encoding = 'utf-8', errors='ignore')
target.write(u'---\n')              
target.write(u'layout:     resources \n')                        
target.write(u'date:       '+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ' \n')
target.write(u'---\n')              

root_path = u'D:/cocolian/cocolian-resources/'

for (folder_name, folder_desc) in names.items() : 
    target.write(u'<h2>'+ folder_desc+ '</h2>\n')
    folder_path = root_path + folder_name
    if os.path.isdir(folder_path):
        for num, cur_file in enumerate(sorted(os.listdir(folder_path))):
            cur_path = folder_path + '/'+ cur_file 
            if os.path.isfile(cur_path) : 
                target.write(u'<li><a href="https://res.cocolian.cn/' + folder_name + '/' + cur_file + '">' + cur_file + '</a></li>\n')

target.write(u'<hr/>\n')


target.flush()
target.close()