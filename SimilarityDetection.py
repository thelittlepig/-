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
import shutil

#可通过更改当前工作目录，简化文件路径，此处为了试验方便未作此处理
#os.chdir(path)，#修改当前工作目录为‘path’

#type设置为多变量

def pretreatment_document(path,type):                
    FileList=os.listdir(path)
    #isExists=os.path.exists(path+'\\学生作业预处理')
    try:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path+'\\学生作业预处理')
        os.makedirs(path + '\\解压文件')
    except FileExistsError as e:
        # 存在则删除目录，再重新创建
        print(e+'目录已存在：'+path+'\\学生作业预处理')
        shutil.rmtree(path+'\\学生作业预处理')
        os.makedirs(path + '\\学生作业预处理')
        print('目录已重新创建')
        pass        
    
    num_illegal = 0 #计算异常文件个数
#异常类型
#1.学生提交作业既不是压缩包，又不是type指定类型的单个文件
#2.学生提交作业是压缩包，但压缩包内没有对应类型文件作业
#3.学生提交作业压缩包内，有多份type指定类型的作业文件（暂时可列为异常作业）
#4.学生有正确的作业文件，但内容为空，或经过预处理后变为空（少数，部分学生作业全为注释等）  
#5.学生作业压缩包内，文件夹的名字有type（极少数）
    
    for i in range(len(FileList)):        
        fileType = os.path.splitext(FileList[i])[-1]
        filePath = os.path.join(path,FileList[i])      
        
        Compressedfile_flag = 0 #压缩包的有无问题
        Numberofhms = 0 #压缩包内有几份作业
        
        if fileType == '.rar':
            f = rarfile.RarFile(filePath)
            Compressedfile_flag = 1 
        elif fileType == '.zip':
            f = zipfile.ZipFile(filePath)
            Compressedfile_flag = 1           
        elif fileType == type:
            hw_f = open(filePath, 'r', encoding='ISO-8859-1')
            Numberofhms += 1
            Contentexists = pretreatment_homework(path,filePath,hw_f,Compressedfile_flag,Numberofhms)
            # 异常4，报告作业内容异常并计数
            if Contentexists == 0:
                print(FileList[i] +"作业内容异常，内容可能为空或全为注释")
                num_illegal += 1 
            else:
                #作业内容正常
                pass       
        # 异常1，报告异常文件并计数
        else:   
            print(FileList[i]+"  异常，不是压缩包或"+type+"文件")
            num_illegal += 1
            continue     
        
        if Compressedfile_flag == 1 :                      
            for j in range(len(f.namelist())):                      
                ##学生作业类型有 .py,.html,.txt,.docx等
                if os.path.splitext(f.namelist()[j])[-1] == type:   
                    hw_name = f.namelist()[j]
                    Numberofhms += 1
                else:
                    pass                                                         
            if Numberofhms == 0: # 异常2，报告异常文件并计数
                print(FileList[i]+"  异常，压缩包内没有需要的"+type+"文件")
                num_illegal += 1                
            elif Numberofhms == 1:                   
                hw_f= open(f.extract(hw_name, path=path + "\\解压文件"),encoding='ISO-8859-1')
                Contentexists = pretreatment_homework(path,filePath,hw_f,Compressedfile_flag,Numberofhms)
                # 异常4，报告作业内容异常并计数
                if Contentexists == 0:
                    print(FileList[i] +"作业内容异常，内容可能为空或全为注释")
                    num_illegal += 1
                else:
                    #作业内容正常
                    pass
                #hw_f = f.open(hw_name,'r')
            #异常3,多份作业                         
            else:                
                print(FileList[i]+"  异常，压缩包内有多份"+type+"作业文件")
                num_illegal += 1
            hw_f.close()
    print("异常作业数量： " + str(num_illegal ))  # -2的原因：预处理文件夹和解压缩文件夹
             


def pretreatment_homework(path,filePath,hw_f,Compressedfile_flag,Numberofhms):     
    '''
    if Compressedfile_flag == 0 and Numberofhms == 1:
        nf = open(path+'\\学生作业预处理\\'+filePath[-7:-4],"w",encoding="utf-8")                   
    elif Compressedfile_flag == 1 and Numberofhms == 1:    
        nf = open(path+'\\学生作业预处理\\'+filePath[-7:-4],"w",encoding="utf-8")           
    else:#Compressedfile_flag == 1 and Numberofhms >= 1 多份作业情况已列为异常
        pass
    '''
    nf = open(path+'\\学生作业预处理\\'+filePath[-7:-4],"w",encoding="utf-8")
    str_nf = ''
    for line in hw_f:
        # 去掉注释行，不同类型代码的注释符不一样
        # py作业第一个字符为#或者是'，就pass
        if (line[0] != '#') and (line[0] != " ' "):
            # 删除空格，换行符等
            newStr = line.replace(" ", "").replace("\r", "").replace("\t", "").replace("\n", "").strip()
            sub_str = re.sub(u"([^\u0041-\u005a\u0061-\u007a])", "", newStr)    # 只提取大小写英文字母字母
            str_nf += sub_str
            nf.write(sub_str)
    if str_nf == '':
        Content = 0
    else:
        Content = 1
    nf.close()
    return Content

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
        for j in range(len(result[0])):
            if i == j :
                pass
            else:
                h = result.iloc[i,j]            
                ###根据重复度挑选出相关同学
                if h == 1:
                    if result.index[i] not in copy_students:
                        copy_students.append(result.index[i])
                        copy_by.append(result.index[i])
                        copy_count += 1 
                    if result.index[j] not in copy_students:
                        copy_students.append(result.index[j])
                        copy_count += 1     
        if result.index[i] in copy_by:        
            copy_students.append(c.pop(1)) 
    copy_students.insert(0,'A')
    copy_students.pop()
    cd = round(copy_count/len(s),4)
    copy_degree = "%.2f%%" % (cd * 100)
    copy_students.insert(0,copy_degree)
    return copy_students    

# In[]
def main():
    k, t = 5, 8 ## t= k+w-1
    path = r"C:\Users\Administrator\Desktop\试验"
    type = '.py'
    path1 = path +'\\学生作业预处理'
    pretreatment_document(path,type)
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
    # 删除临时文件
    path2 = path+'\\解压文件'
    shutil.rmtree(path1)
    shutil.rmtree(path2)

if __name__ == '__main__':    
    main()

