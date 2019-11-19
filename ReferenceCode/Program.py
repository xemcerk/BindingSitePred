#%%
import os
import xlwt 
import xlrd
import xlutils.copy
import math   # 导入 math 模块
import pandas as pd
from numpy import *  

#%%
# 第一个文件------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 第一个文件------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 第一个文件------------------------------------------------------------------------------------------------------------------------------------------------------------------
data = []
sum_value=[0]*6
sum_value_zong=[0]*6
averang_value=[0]*6
averang_value_zong=[0]*6
all_averang_value=[] 

# 文件路径
path_1= "ReferenceCode/File/1" 
path_zong= "ReferenceCode/File/HUIZONG" 

# 文件路径
files_1= os.listdir(path_1) 
files_zong= os.listdir("ReferenceCode/File/HUIZONG") 

# 这里是统计每个文件夹的文件个数
file_count_1= 0
file_count_zong= 0
 
for file in files_1: 
	file_count_1 = file_count_1+1 
for file in files_zong: 
	file_count_zong = file_count_zong+1 

#%%
# -----------------------------------------
# 第1步 
# 公式7
# Uv 是结果
# -----------------------------------------

for file in files_1: #遍历文件夹  
	f = open(path_1+"/"+file); #打开文件   
	for line in f: #遍历文件，一行行遍历，读取文本
		line_data=line.split() # line_data为每个文件中每行的数据切割后得到的数据
		if len(line_data): # 这里是去除空行， 
			if (str(line_data[0]).isdigit()):# 这里是去得到以数字开头的内容 
				data.append(line_data)# 满足 仅仅以数字开头的 行数据， 则添加到data列表里面	 	 
	for j in range(2,8): # 遍历 2 3 4 5 6 7 列
		for i in range(len(data)):	# 遍历 0~len(data)-1 行 
			sum_value[j-2]=sum_value[j-2]+float(data[i][j])	# 第j列的所有行的内容相加 
		averang_value[j-2]=sum_value[j-2]/len(data) # 得到平均值
	data=[] # 这里要清空data列表，因为单个文件都会进行列表添加append。而求平均值是对单个文件做的。 
	sum_value=[0]*6 # 因为sum_value是累加的内容，所以要清空数据 
	all_averang_value.append(averang_value[:])	# averang_value 是1行6列的数据，表示单个文件中所有行的平均值。因为有6列，所以为1行*6列  
	averang_value=[0]*6 
for j in range(0,6):
	for i in range(file_count_1): # 遍历78个平均值
		sum_value_zong[j]=sum_value_zong[j]+all_averang_value[i][j] # 累加
	averang_value_zong[j]=sum_value_zong[j]/file_count_1# 求平均值  
Ti=transpose(mat(all_averang_value))#6*78 
Uv=transpose(mat(averang_value_zong))#6*1 
print(Ti)

#%%
# -----------------------------------------
# 第2步 第3步 
# 公式9 公式8 
# Mahalanobis_Distance 是结果
# -----------------------------------------

Mahalanobis_Distance=mat([([0.0] * 6) for i in range(6)])#float型矩阵
sum_1=0 
Pv=file_count_1
for i in range(0,6):
	for j in range(0,6):
		for k in range(0,Pv): 
			sum_1=sum_1+(Ti[i,k]-Uv[i])*(Ti[j,k]-Uv[j]) 
		Mahalanobis_Distance[i,j]=sum_1/Pv
		sum_1=0 #这里必须要清0哦 

# -----------------------------------------
# 第4步
# 公式6
# Mahalanobis_Distance_Matrix 是 Mahalanobis_Distance 的逆矩阵
# Result=(R-Uv)T * Mahalanobis_Distance_Matrix * (R-Uv)
# Result  是公式6的结果，78个数据
# ----------------------------------------- 

# 这里是总的文件夹
files_zong= os.listdir("ReferenceCode/File/HUIZONG") #得到文件夹下的所有文件名称 
# 这里的求总文件里的Ti
data = []
sum_value=[0]*6 
averang_value=[0]*6 
all_averang_value=[] 

for file in files_zong: #遍历文件夹  
	f = open(path_zong+"/"+file); #打开文件   
	for line in f: #遍历文件，一行行遍历，读取文本
		line_data=line.split() # line_data为每个文件中每行的数据切割后得到的数据
		if len(line_data): # 这里是去除空行， 
			if (str(line_data[0]).isdigit()):# 这里是去得到以数字开头的内容 
				data.append(line_data)# 满足 仅仅以数字开头的 行数据， 则添加到data列表里面	 	 
	for j in range(2,8): # 遍历 2 3 4 5 6 7 列
		for i in range(len(data)):	# 遍历 0~len(data)-1 行 
			sum_value[j-2]=sum_value[j-2]+float(data[i][j])	# 第j列的所有行的内容相加 
		averang_value[j-2]=sum_value[j-2]/len(data) # 得到平均值
	data=[] # 这里要清空data列表，因为单个文件都会进行列表添加append。而求平均值是对单个文件做的。 
	sum_value=[0]*6 # 因为sum_value是累加的内容，所以要清空数据 
	all_averang_value.append(averang_value[:])	# averang_value 是1行6列的数据，表示单个文件中所有行的平均值。因为有6列，所以为1行*6列  
	averang_value=[0]*6 
Ti=transpose(mat(all_averang_value)) 
Mahalanobis_Distance_Matrix = (Mahalanobis_Distance).I
Result=[0]*file_count_zong

for i in range(file_count_zong):
	R=Ti[:,i]#6*1  
	Result[i]=(dot(dot(transpose(R-Uv),Mahalanobis_Distance_Matrix),(R-Uv))).tolist()

# -----------------------------------------
# 第5步 
# 公式5 
# ----------------------------------------- 
#这里的Pv还是小文件夹的文件数目,而不是总的文件夹的文件数目

Pv=file_count_1
rd = xlrd.open_workbook("processed_data_zong.xls")   # 打开文件
wt = xlutils.copy.copy(rd)   # 复制
sheets = wt.get_sheet(0)   # 读取第一个工作表
for i in range(0,file_count_zong):
	value=Result[i][0][0]
	result=(log(Pv))-(value/2)-(log((linalg.det(Mahalanobis_Distance))))/2
	sheets.write(i, 0, str(result))
	# print(result)
wt.save("processed_data_zong.xls")   # 保存

# 第二个文件------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 第二个文件------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 第二个文件------------------------------------------------------------------------------------------------------------------------------------------------------------------
data = []
sum_value=[0]*6
sum_value_zong=[0]*6
averang_value=[0]*6
averang_value_zong=[0]*6
all_averang_value=[] 

# 文件路径
path_2= "ReferenceCode/File/2" 
path_zong= "ReferenceCode/File/HUIZONG" 

# 文件路径
files_2= os.listdir("ReferenceCode/File/2") 
files_zong= os.listdir("ReferenceCode/File/HUIZONG") 

# 这里是统计每个文件夹的文件个数
file_count_2= 0
file_count_zong= 0
 
for file in files_2: 
	file_count_2 = file_count_2+1 
for file in files_zong: 
	file_count_zong = file_count_zong+1 

# -----------------------------------------
# 第1步 
# 公式7
# Uv 是结果
# -----------------------------------------

for file in files_2: #遍历文件夹  
	f = open(path_2+"/"+file); #打开文件   
	for line in f: #遍历文件，一行行遍历，读取文本
		line_data=line.split() # line_data为每个文件中每行的数据切割后得到的数据
		if len(line_data): # 这里是去除空行， 
			if (str(line_data[0]).isdigit()):# 这里是去得到以数字开头的内容 
				data.append(line_data)# 满足 仅仅以数字开头的 行数据， 则添加到data列表里面	 	 
	for j in range(2,8): # 遍历 2 3 4 5 6 7 列
		for i in range(len(data)):	# 遍历 0~len(data)-1 行 
			sum_value[j-2]=sum_value[j-2]+float(data[i][j])	# 第j列的所有行的内容相加 
		averang_value[j-2]=sum_value[j-2]/len(data) # 得到平均值
	data=[] # 这里要清空data列表，因为单个文件都会进行列表添加append。而求平均值是对单个文件做的。 
	sum_value=[0]*6 # 因为sum_value是累加的内容，所以要清空数据 
	all_averang_value.append(averang_value[:])	# averang_value 是1行6列的数据，表示单个文件中所有行的平均值。因为有6列，所以为1行*6列  
	averang_value=[0]*6 
for j in range(0,6):
	for i in range(file_count_2): # 遍历78个平均值
		sum_value_zong[j]=sum_value_zong[j]+all_averang_value[i][j] # 累加
	averang_value_zong[j]=sum_value_zong[j]/file_count_2# 求平均值  
Ti=transpose(mat(all_averang_value))#6*78 
Uv=transpose(mat(averang_value_zong))#6*1 
# print(Ti)
# -----------------------------------------
# 第2步 第3步 
# 公式9 公式8 
# Mahalanobis_Distance 是结果
# -----------------------------------------

Mahalanobis_Distance=mat([([0.0] * 6) for i in range(6)])#float型矩阵
sum_2=0 
Pv=file_count_2
for i in range(0,6):
	for j in range(0,6):
		for k in range(0,Pv): 
			sum_2=sum_2+(Ti[i,k]-Uv[i])*(Ti[j,k]-Uv[j]) 
		Mahalanobis_Distance[i,j]=sum_2/Pv
		sum_2=0 #这里必须要清0哦 

# -----------------------------------------
# 第4步
# 公式6
# Mahalanobis_Distance_Matrix 是 Mahalanobis_Distance 的逆矩阵
# Result=(R-Uv)T * Mahalanobis_Distance_Matrix * (R-Uv)
# Result  是公式6的结果，78个数据
# ----------------------------------------- 

# 这里是总的文件夹
files_zong= os.listdir("ReferenceCode/File/HUIZONG") #得到文件夹下的所有文件名称 
# 这里的求总文件里的Ti
data = []
sum_value=[0]*6 
averang_value=[0]*6 
all_averang_value=[] 

for file in files_zong: #遍历文件夹  
	f = open(path_zong+"/"+file); #打开文件   
	for line in f: #遍历文件，一行行遍历，读取文本
		line_data=line.split() # line_data为每个文件中每行的数据切割后得到的数据
		if len(line_data): # 这里是去除空行， 
			if (str(line_data[0]).isdigit()):# 这里是去得到以数字开头的内容 
				data.append(line_data)# 满足 仅仅以数字开头的 行数据， 则添加到data列表里面	 	 
	for j in range(2,8): # 遍历 2 3 4 5 6 7 列
		for i in range(len(data)):	# 遍历 0~len(data)-1 行 
			sum_value[j-2]=sum_value[j-2]+float(data[i][j])	# 第j列的所有行的内容相加 
		averang_value[j-2]=sum_value[j-2]/len(data) # 得到平均值
	data=[] # 这里要清空data列表，因为单个文件都会进行列表添加append。而求平均值是对单个文件做的。 
	sum_value=[0]*6 # 因为sum_value是累加的内容，所以要清空数据 
	all_averang_value.append(averang_value[:])	# averang_value 是1行6列的数据，表示单个文件中所有行的平均值。因为有6列，所以为1行*6列  
	averang_value=[0]*6 
Ti=transpose(mat(all_averang_value)) 
Mahalanobis_Distance_Matrix = (Mahalanobis_Distance).I
Result=[0]*file_count_zong

for i in range(file_count_zong):
	R=Ti[:,i]#6*1  
	Result[i]=(dot(dot(transpose(R-Uv),Mahalanobis_Distance_Matrix),(R-Uv))).tolist()

# -----------------------------------------
# 第5步 
# 公式5 
# ----------------------------------------- 
#这里的Pv还是小文件夹的文件数目,而不是总的文件夹的文件数目

Pv=file_count_2
rd = xlrd.open_workbook("processed_data_zong.xls")   # 打开文件
wt = xlutils.copy.copy(rd)   # 复制
sheets = wt.get_sheet(0)   # 读取第一个工作表
for i in range(0,file_count_zong):
	value=Result[i][0][0]
	result=(log(Pv))-(value/2)-(log((linalg.det(Mahalanobis_Distance))))/2
	sheets.write(i, 1, str(result))
	# print(result)
wt.save("processed_data_zong.xls")   # 保存

# 第三个文件------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 第三个文件------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 第三个文件------------------------------------------------------------------------------------------------------------------------------------------------------------------

data = []
sum_value=[0]*6
sum_value_zong=[0]*6
averang_value=[0]*6
averang_value_zong=[0]*6
all_averang_value=[] 

# 文件路径
path_3= "ReferenceCode/File/3" 
path_zong= "ReferenceCode/File/HUIZONG" 

# 文件路径
files_3= os.listdir("ReferenceCode/File/3") 
files_zong= os.listdir("ReferenceCode/File/HUIZONG") 

# 这里是统计每个文件夹的文件个数
file_count_3= 0
file_count_zong= 0
 
for file in files_3: 
	file_count_3 = file_count_3+1 
for file in files_zong: 
	file_count_zong = file_count_zong+1 

# -----------------------------------------
# 第1步 
# 公式7
# Uv 是结果
# -----------------------------------------

for file in files_3: #遍历文件夹  
	f = open(path_3+"/"+file); #打开文件   
	for line in f: #遍历文件，一行行遍历，读取文本
		line_data=line.split() # line_data为每个文件中每行的数据切割后得到的数据
		if len(line_data): # 这里是去除空行， 
			if (str(line_data[0]).isdigit()):# 这里是去得到以数字开头的内容 
				data.append(line_data)# 满足 仅仅以数字开头的 行数据， 则添加到data列表里面	 	 
	for j in range(2,8): # 遍历 2 3 4 5 6 7 列
		for i in range(len(data)):	# 遍历 0~len(data)-1 行 
			sum_value[j-2]=sum_value[j-2]+float(data[i][j])	# 第j列的所有行的内容相加 
		averang_value[j-2]=sum_value[j-2]/len(data) # 得到平均值
	data=[] # 这里要清空data列表，因为单个文件都会进行列表添加append。而求平均值是对单个文件做的。 
	sum_value=[0]*6 # 因为sum_value是累加的内容，所以要清空数据 
	all_averang_value.append(averang_value[:])	# averang_value 是1行6列的数据，表示单个文件中所有行的平均值。因为有6列，所以为1行*6列  
	averang_value=[0]*6 
for j in range(0,6):
	for i in range(file_count_3): # 遍历78个平均值
		sum_value_zong[j]=sum_value_zong[j]+all_averang_value[i][j] # 累加
	averang_value_zong[j]=sum_value_zong[j]/file_count_3# 求平均值  
Ti=transpose(mat(all_averang_value))#6*78 
Uv=transpose(mat(averang_value_zong))#6*1 
# print(Ti)
# -----------------------------------------
# 第2步 第3步 
# 公式9 公式8 
# Mahalanobis_Distance 是结果
# -----------------------------------------

Mahalanobis_Distance=mat([([0.0] * 6) for i in range(6)])#float型矩阵
sum_3=0 
Pv=file_count_3
for i in range(0,6):
	for j in range(0,6):
		for k in range(0,Pv): 
			sum_3=sum_3+(Ti[i,k]-Uv[i])*(Ti[j,k]-Uv[j]) 
		Mahalanobis_Distance[i,j]=sum_3/Pv
		sum_3=0 #这里必须要清0哦 

# -----------------------------------------
# 第4步
# 公式6
# Mahalanobis_Distance_Matrix 是 Mahalanobis_Distance 的逆矩阵
# Result=(R-Uv)T * Mahalanobis_Distance_Matrix * (R-Uv)
# Result  是公式6的结果，78个数据
# ----------------------------------------- 

# 这里是总的文件夹
files_zong= os.listdir("ReferenceCode/File/HUIZONG") #得到文件夹下的所有文件名称 
# 这里的求总文件里的Ti
data = []
sum_value=[0]*6 
averang_value=[0]*6 
all_averang_value=[] 

for file in files_zong: #遍历文件夹  
	f = open(path_zong+"/"+file); #打开文件   
	for line in f: #遍历文件，一行行遍历，读取文本
		line_data=line.split() # line_data为每个文件中每行的数据切割后得到的数据
		if len(line_data): # 这里是去除空行， 
			if (str(line_data[0]).isdigit()):# 这里是去得到以数字开头的内容 
				data.append(line_data)# 满足 仅仅以数字开头的 行数据， 则添加到data列表里面	 	 
	for j in range(2,8): # 遍历 2 3 4 5 6 7 列
		for i in range(len(data)):	# 遍历 0~len(data)-1 行 
			sum_value[j-2]=sum_value[j-2]+float(data[i][j])	# 第j列的所有行的内容相加 
		averang_value[j-2]=sum_value[j-2]/len(data) # 得到平均值
	data=[] # 这里要清空data列表，因为单个文件都会进行列表添加append。而求平均值是对单个文件做的。 
	sum_value=[0]*6 # 因为sum_value是累加的内容，所以要清空数据 
	all_averang_value.append(averang_value[:])	# averang_value 是1行6列的数据，表示单个文件中所有行的平均值。因为有6列，所以为1行*6列  
	averang_value=[0]*6 
Ti=transpose(mat(all_averang_value)) 
Mahalanobis_Distance_Matrix = (Mahalanobis_Distance).I
Result=[0]*file_count_zong

for i in range(file_count_zong):
	R=Ti[:,i]#6*1  
	Result[i]=(dot(dot(transpose(R-Uv),Mahalanobis_Distance_Matrix),(R-Uv))).tolist()

# -----------------------------------------
# 第5步 
# 公式5 
# ----------------------------------------- 
#这里的Pv还是小文件夹的文件数目,而不是总的文件夹的文件数目

Pv=file_count_3
rd = xlrd.open_workbook("processed_data_zong.xls")   # 打开文件
wt = xlutils.copy.copy(rd)   # 复制
sheets = wt.get_sheet(0)   # 读取第一个工作表
for i in range(0,file_count_zong):
	value=Result[i][0][0]
	result=(log(Pv))-(value/2)-(log((linalg.det(Mahalanobis_Distance))))/2
	sheets.write(i, 2, str(result))
	# print(result)
wt.save("processed_data_zong.xls")   # 保存

# 第四个文件------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 第四个文件------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 第四个文件------------------------------------------------------------------------------------------------------------------------------------------------------------------

data = []
sum_value=[0]*6
sum_value_zong=[0]*6
averang_value=[0]*6
averang_value_zong=[0]*6
all_averang_value=[] 

# 文件路径
path_4= "ReferenceCode/File/4" 
path_zong= "ReferenceCode/File/HUIZONG" 

# 文件路径
files_4= os.listdir("ReferenceCode/File/4") 
files_zong= os.listdir("ReferenceCode/File/HUIZONG") 

# 这里是统计每个文件夹的文件个数
file_count_4= 0
file_count_zong= 0
 
for file in files_4: 
	file_count_4 = file_count_4+1 
for file in files_zong: 
	file_count_zong = file_count_zong+1 

# -----------------------------------------
# 第1步 
# 公式7
# Uv 是结果
# -----------------------------------------

for file in files_4: #遍历文件夹  
	f = open(path_4+"/"+file); #打开文件   
	for line in f: #遍历文件，一行行遍历，读取文本
		line_data=line.split() # line_data为每个文件中每行的数据切割后得到的数据
		if len(line_data): # 这里是去除空行， 
			if (str(line_data[0]).isdigit()):# 这里是去得到以数字开头的内容 
				data.append(line_data)# 满足 仅仅以数字开头的 行数据， 则添加到data列表里面	 	 
	for j in range(2,8): # 遍历 2 3 4 5 6 7 列
		for i in range(len(data)):	# 遍历 0~len(data)-1 行 
			sum_value[j-2]=sum_value[j-2]+float(data[i][j])	# 第j列的所有行的内容相加 
		averang_value[j-2]=sum_value[j-2]/len(data) # 得到平均值
	data=[] # 这里要清空data列表，因为单个文件都会进行列表添加append。而求平均值是对单个文件做的。 
	sum_value=[0]*6 # 因为sum_value是累加的内容，所以要清空数据 
	all_averang_value.append(averang_value[:])	# averang_value 是1行6列的数据，表示单个文件中所有行的平均值。因为有6列，所以为1行*6列  
	averang_value=[0]*6 
for j in range(0,6):
	for i in range(file_count_4): # 遍历78个平均值
		sum_value_zong[j]=sum_value_zong[j]+all_averang_value[i][j] # 累加
	averang_value_zong[j]=sum_value_zong[j]/file_count_4# 求平均值  
Ti=transpose(mat(all_averang_value))#6*78 
Uv=transpose(mat(averang_value_zong))#6*1 
# print(Ti)
# -----------------------------------------
# 第2步 第3步 
# 公式9 公式8 
# Mahalanobis_Distance 是结果
# -----------------------------------------

Mahalanobis_Distance=mat([([0.0] * 6) for i in range(6)])#float型矩阵
sum_4=0 
Pv=file_count_4
for i in range(0,6):
	for j in range(0,6):
		for k in range(0,Pv): 
			sum_4=sum_4+(Ti[i,k]-Uv[i])*(Ti[j,k]-Uv[j]) 
		Mahalanobis_Distance[i,j]=sum_4/Pv
		sum_4=0 #这里必须要清0哦 

# -----------------------------------------
# 第4步
# 公式6
# Mahalanobis_Distance_Matrix 是 Mahalanobis_Distance 的逆矩阵
# Result=(R-Uv)T * Mahalanobis_Distance_Matrix * (R-Uv)
# Result  是公式6的结果，78个数据
# ----------------------------------------- 

# 这里是总的文件夹
files_zong= os.listdir("ReferenceCode/File/HUIZONG") #得到文件夹下的所有文件名称 
# 这里的求总文件里的Ti
data = []
sum_value=[0]*6 
averang_value=[0]*6 
all_averang_value=[] 

for file in files_zong: #遍历文件夹  
	f = open(path_zong+"/"+file); #打开文件   
	for line in f: #遍历文件，一行行遍历，读取文本
		line_data=line.split() # line_data为每个文件中每行的数据切割后得到的数据
		if len(line_data): # 这里是去除空行， 
			if (str(line_data[0]).isdigit()):# 这里是去得到以数字开头的内容 
				data.append(line_data)# 满足 仅仅以数字开头的 行数据， 则添加到data列表里面	 	 
	for j in range(2,8): # 遍历 2 3 4 5 6 7 列
		for i in range(len(data)):	# 遍历 0~len(data)-1 行 
			sum_value[j-2]=sum_value[j-2]+float(data[i][j])	# 第j列的所有行的内容相加 
		averang_value[j-2]=sum_value[j-2]/len(data) # 得到平均值
	data=[] # 这里要清空data列表，因为单个文件都会进行列表添加append。而求平均值是对单个文件做的。 
	sum_value=[0]*6 # 因为sum_value是累加的内容，所以要清空数据 
	all_averang_value.append(averang_value[:])	# averang_value 是1行6列的数据，表示单个文件中所有行的平均值。因为有6列，所以为1行*6列  
	averang_value=[0]*6 
Ti=transpose(mat(all_averang_value)) 
Mahalanobis_Distance_Matrix = (Mahalanobis_Distance).I
Result=[0]*file_count_zong

for i in range(file_count_zong):
	R=Ti[:,i]#6*1  
	Result[i]=(dot(dot(transpose(R-Uv),Mahalanobis_Distance_Matrix),(R-Uv))).tolist()

# -----------------------------------------
# 第5步 
# 公式5 
# ----------------------------------------- 
#这里的Pv还是小文件夹的文件数目,而不是总的文件夹的文件数目

Pv=file_count_4
rd = xlrd.open_workbook("processed_data_zong.xls")   # 打开文件
wt = xlutils.copy.copy(rd)   # 复制
sheets = wt.get_sheet(0)   # 读取第一个工作表
for i in range(0,file_count_zong):
	value=Result[i][0][0]
	result=(log(Pv))-(value/2)-(log((linalg.det(Mahalanobis_Distance))))/2
	sheets.write(i, 3, str(result))
	# print(result)
wt.save("processed_data_zong.xls")   # 保存

# 处理完了四个小文件了！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
# 处理完了四个小文件了！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
# 处理完了四个小文件了！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！

# 这里进行查找每行元素中的最大值的位置
rd = xlrd.open_workbook("processed_data_zong.xls")   # 打开文件
wt = xlutils.copy.copy(rd)   # 复制
sheets = wt.get_sheet(0)   # 读取第一个工作表
table_data =xlrd.open_workbook("processed_data_zong.xls").sheet_by_name('Sheet1')
n=table_data.nrows
for i in range(0,n):
	row_values =table_data.row_values(i)#从0开始，4为第5列 
	# print(row_values)
	index_value=row_values[0:4].index(max(row_values[0:4]))+1 # 最大值索引
	sheets.write(i, 5, str(index_value))
wt.save("processed_data_zong.xls")   # 保存

# 找到最大值位置了！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
# 找到最大值位置了！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
# 找到最大值位置了！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
# 这里进行比较
# 打印输出结果
rd = xlrd.open_workbook("processed_data_zong.xls")   # 打开文件
wt = xlutils.copy.copy(rd)   # 复制
sheets = wt.get_sheet(0)   # 读取第一个工作表
table_data =xlrd.open_workbook("processed_data_zong.xls").sheet_by_name('Sheet1')
n=table_data.nrows
for i in range(0,n):
	row_values =table_data.row_values(i)#从0开始，4为第5列  
	E_value=row_values[4]
	F_value=row_values[5]
	if float(E_value) != float(F_value) :
		sheets.write(i, 6, E_value)
		sheets.write(i, 7, F_value)
wt.save("processed_data_zong.xls")   # 保存
E_col_values =table_data.col_values(6)
F_col_values =table_data.col_values(7)
print('打印统计的结果')
E_col_values_count=pd.value_counts(E_col_values)
F_col_values_count=pd.value_counts(F_col_values)
print('E_col_values_count')
print(E_col_values_count)
print('F_col_values_count')
print(F_col_values_count)
