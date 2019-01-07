#!/bin/bash

today=`date +"%Y-%m-%d"`
cd  /cygdrive/d/cocolian/cocolian-wechat/python
python source.py
python images.py
echo  '========================'
cd /cygdrive/d/cocolian/cocolian-docs/
git pull
git add -A
echo 'update sources to '$today
git commit -m 'update sources to '$today 
git push origin master
echo  '========================'
cd /cygdrive/d/cocolian/cocolian-static
git pull
git add -A
echo  'update images to '$today
git commit -m 'update images to '$today
git push origin master
echo  '========================'
cd /cygdrive/d/cocolian/cocolian-wechat
git pull
git add -A
echo  'update scripts to '$today
git commit -m 'update scripts to '$today
git push origin master
echo  '========================'
cd /cygdrive/d/cocolian/cocolian-resources
git pull
git add -A
echo  'update resources to '$today
git commit -m 'update resources to '$today
git push origin master