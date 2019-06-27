# -*- coding: utf-8 -*-
"""
Created on Mon May 27 10:00:55 2019

@author: llcheng6
"""



import numpy as np 
import pandas as pd
import os
#os.chdir('E:\关于学生作业评价\调研\学生作业实际案例\安信工软件1702_WEB前端开发基础_孔凡豹')
#path = 'E:\关于学生作业评价\调研\学生作业实际案例\安信工软件1702_WEB前端开发基础_孔凡豹\\similarityresult.csv'
#data = pd.read_csv('similarityresult.csv')

k, t = 5, 8               
s = read_document()  #不同学生的作业   
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
         

path = "E:\\关于学生作业评价\\调研\\学生作业实际案例\\安信工软件1702_WEB前端开发基础_孔凡豹\\预处理后文件"
fileList=os.listdir(path)
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
fl=open('E:\\关于学生作业评价\\调研\\学生作业实际案例\\安信工软件1702_WEB前端开发基础_孔凡豹\\copy_students.txt', 'w')
fl.write(str(copy_students))
fl.close()
x = pd.DataFrame(copy_students)
x.to_csv('E:\\关于学生作业评价\\调研\\学生作业实际案例\\安信工软件1702_WEB前端开发基础_孔凡豹\\similarityresult.csv', mode='a', header=False)

#print(copy_students)

#    copy_students.append(result.index[i])
     

nf = open('E:\\关于学生作业评价\\调研\\学生作业实际案例\\安信工软件1702_WEB前端开发基础_孔凡豹\\123\\111,"w",encoding="utf-8")       


import os
path = "E:\\关于学生作业评价\\调研\\学生作业实际案例\\安信工软件1702_WEB前端开发基础_孔凡豹\\学生作业压缩包"
os.mkdir(path+'\\学生作业预处理')












