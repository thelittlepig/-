# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:54:09 2019

@author: llcheng6
"""

import os
import re
import zipfile
from unrar import rarfile

def pretreatment_document(path):        
    os.mkdir(path+'\\学生作业预处理')
    FileList=os.listdir(path)
    for i in range(len(FileList)):  
        filePath = os.path.join(path,FileList[i])      
        if 'rar' in FileList[i]:
            f = rarfile.RarFile(filePath)
            for i in range(len(f.namelist())):          
                ##手动换学生作业类型 .py,.html,.txt,.docx等
                if '.html' in f.namelist()[i]:
                    hw_name = f.namelist()[i]
                else:
                    pass              
                # 问题：学生压缩包内没有对应类型文件作业，hw_name 没有被赋值
                #问题：如果有多份符合格式的作业，代码执行只能取到最后一份作业  

        elif 'zip' in FileList[i]:
            f = zipfile.ZipFile(filePath) 
            for i in range(len(f.namelist())):          
                ##手动换学生作业类型 .py,.html,.txt,.docx等
                if '.html' in f.namelist()[i]:
                    hw_name = f.namelist()[i]
                else:
                    pass
                # 问题：学生压缩包内没有对应类型文件作业，hw_name 没有被赋值
                #问题：如果有多份符合格式的作业，代码执行只能取到最后一份作业   
        else:
            #问题：下载学生提交的作业，如果不是压缩包格式暂时直接跳过
            continue
        hw_f = f.open(hw_name,'r')        
        nf = open(path+'\\学生作业预处理\\'+filePath[-7:-4],"w",encoding="utf-8")       
        while True:
            data  = hw_f.readline().decode('ISO-8859-1') #不同文件
            if data  == '':
                break
            else:
            #去掉注释行，不同类型代码的注释符不一样
            #py作业第一个字符为#或者是'，就pass
                if (data[0] == '#') or (data[0] == " ' "):
                    pass
                else:                   
                    #删除空格，换行符等
                    newStr = data.replace(" ","").replace("\r","").replace("\t","").replace("\n","").strip()
                    #只提取大小写英文字母字母
                    #后续可优化
                    sub_str = re.sub(u"([^\u0041-\u005a\u0061-\u007a])","",newStr)
                    nf.write(sub_str)
        hw_f.close()
        nf.close() 
