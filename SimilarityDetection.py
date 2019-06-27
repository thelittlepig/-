# -*- coding: utf-8 -*-
"""
Created on Thu May 16 13:55:35 2019

@author: llcheng6
"""

import os
import re
import zipfile
from unrar import rarfile
import numpy as np
import pandas as pd

#可通过更改当前工作目录，简化文件路径，此处为了试验方便未作此处理
#os.chdir(path)，#修改当前工作目录为‘path’
'''
############读取学生作业进行预处理，并存入到指定文件夹
path = "E:\\关于学生作业评价\\调研\\试验\\原始作业"
#path1 = "E:\\关于学生作业评价\\调研\\试验\\预处理后文件"
fileList=os.listdir(path)
for f in fileList:
    filePath = os.path.join(path,f)
    if os.path.isfile(filePath):
        f = open(filePath,encoding="utf-8")
        nf = open('E:\\关于学生作业评价\\调研\\试验\\预处理后文件\\'+filePath[-8:-5] +'_new.py',"w",encoding="utf-8")       
        while True:
            data  = f.readline()
            if data  == '':
                break
            else:
            #第一个字符为#或者是'，就pass，否则就打印这一行
                if (data[0] == '#') or (data[0] == " ' "):
                    pass
                else:                   
                    #删除空格，换行符
                    newStr = data.replace(" ","").replace("\t","").replace("\n","").strip()
                    #只提取大小写英文字母字母
                    sub_str = re.sub(u"([^\u0041-\u005a\u0061-\u007a])","",newStr)
                    nf.write(sub_str)
        f.close()
        nf.close()  
'''

def pretreatment_document(path):        
    
    isExists=os.path.exists(path+'\\学生作业预处理')
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path+'\\学生作业预处理')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        #print (path+'\\学生作业预处理'+' 目录已存在')
        pass
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

#os.chdir('E:\\关于学生作业评价\\调研\\学生作业实际案例\\代码\\作业提取')
#fileList=os.listdir()
#winHash = {}


def read_document(path1):
####将存放预处理文件的文件夹内所有文件内容合并到ns上
    fileList=os.listdir(path1)
    strList=[]

    for f in fileList:
        filePath = os.path.join(path1,f) 
        if os.path.isfile(filePath):
            file = open(filePath)
            filelines = file.readlines()
            s=""
            ns=""            
            for line in filelines:
                s=s+line
            ns="".join(s.split())
            strList.append(ns)            
            file.close()    
    return strList
    

'''
K=3
for i in range(len(ns)):
    if (i+K>len(ns)):
        break
    shingle = ns[i:i+K]
    kgram.append(shingle)

print (kgram)
print ("the number of k-gram:" + str(len(kgram)))
'''

###生成grams序列
def make_kgrams(s, k):
    grams = []
    start, end = 0, k
    while start < len(s) - k + 1:
        grams.append(s[start:end])
        start += 1
        end += 1
    return grams
'''
#参考博客使用的rolling生成哈希值法
def hash(grams):
    K=3
    Base=3
    hash=0
    HashList=[]
    firstShingle=grams[0]    
    for i in range(K):
        hash += ord(firstShingle[i])*(Base**(K-1-i))        
    HashList.append(hash)    
    for i in range(1,len(grams)):
        preshingle=grams[i-1]
        shingle = grams[i]
        hash = hash * Base - ord(preshingle[0])*Base**K + ord(shingle[K-1])
        HashList.append(hash)
    return HashList
'''

#简单生成hash值
def hash(text):
    hash = 0
    for i in range(len(text)):
        hash += ord(text[i]) * (17**(len(text) - i - 1))
    return hash

####取区间最小值
def right_weight_min(key=lambda x: x[0]):
    def r_min(l):
        cur_min, min_index, i = float('inf'), -1, 0 
        while i < len(l):
            if key(l[i]) <= cur_min:
                cur_min, min_index = key(l[i]), i
            i += 1
        return l[min_index]
    return r_min


##########winnow算法   
def winnow(k_grams, k, t):
    min = right_weight_min(lambda x: x[0])  
    fingerprints = {}
    hashes = [(hash(k_grams[i]), i) for i in range(len(k_grams))]
    windowSize = t - k + 1  
    w_start, w_end = 0, windowSize
    cur_min = None
    while w_end < len(hashes):
        window = hashes[w_start:w_end]
        new_min = min(window)
        if cur_min != new_min:
            fingerprints[new_min[1]] = new_min[0]
            cur_min = new_min
        w_start, w_end = w_start + 1, w_end + 1
    return fingerprints


def compute_similarity(k,t,path):
    s = read_document(path)  #不同学生的作业   
    similarity = np.identity(len(s))
    result = pd.DataFrame(similarity)
    x = []
    for i in range(len(s)):
        k_grams = make_kgrams(s[i], k)       
        fingerprint = winnow(k_grams, k, t)
        x.append(fingerprint)        
    for i in range(len(x)):
        for j in range(len(x)):
                T1 = set(x[i])
                T2 = set(x[j])
                intersection = T1 & T2
                similarity[i,j] = len(intersection)/len(T1)
                a = similarity[i,j]           
                result.iloc[i,j] = "%.2f%%" % (a * 100)     
    return result

def show_list(k,t,path1):              
    s = read_document(path1)  #不同学生的作业   
    similarity = np.identity(len(s))
    result = pd.DataFrame(similarity)
    x = []
    for i in range(len(s)):
        k_grams = make_kgrams(s[i], k)       
        fingerprint = winnow(k_grams, k, t)
        x.append(fingerprint)        
    for i in range(len(x)):
        for j in range(len(x)):
                T1 = set(x[i])
                T2 = set(x[j])
                intersection = T1 & T2
                similarity[i,j] = len(intersection)/len(T1)
    fileList=os.listdir(path1)
    result.index = fileList
    c = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N']
    copy_students = []
    copy_by=[]
    copy_count = 0
    for i in range(len(result)):
        if result.index[i] in copy_students:
            continue    
        for j in range(len(result[0])):
            if i == j :
                pass
    
            else:
                h = result.iloc[i,j]            
                ###根据重复度挑选出相关同学
                if h == 1:
                    copy_by.append(result.index[i])                
                    copy_students.append(result.index[j])
                    copy_count += 1  
        if result.index[i] in copy_by:        
            copy_students.append(result.index[i])
            copy_students.append(c.pop(1)) 
            copy_count += 1
    copy_students.insert(0,'A')
    copy_students.pop()
    cd = round(copy_count/len(s),4)
    copy_degree = "%.2f%%" % (cd * 100)
    copy_students.insert(0,copy_degree)
    return copy_students
    

# In[]

def main():
    k, t = 5, 8 ## t= k+w-1
    path = "E:\\关于学生作业评价\\调研\\学生作业实际案例\\安信工软件1702_WEB前端开发基础_孔凡豹\\学生作业"
    path1 = path +'\\学生作业预处理'
    pretreatment_document(path)
    result = compute_similarity(k,t,path1)    
    fileList=os.listdir(path1)
    #添加行列名（学生学号或姓名）
    result.columns = fileList
    result.index = fileList 
    result.to_csv(path+'\\similarityresult.csv',encoding='utf-8-sig')
    copy_students = show_list(k,t,path1)
    copy_list = pd.DataFrame(copy_students)
    copy_list.to_csv(path+'\\similarityresult.csv', mode='a', header=False)
    print('\n\t相似度检测完成！','\n检测报表存放位置：\n'+'\t'+path)

if __name__ == '__main__':    
    main()

