from ase.build import bulk
from ase.constraints import ExpCellFilter
from ase.optimize.precon import PreconLBFGS
import numpy as np
import quippy
from quippy.descriptors import Descriptor
import scipy.linalg
import matplotlib.pyplot as plt
from ase.io import read,write
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from mpl_toolkits.mplot3d import Axes3D


def get_pos_na_c(c_file,na_file):
    outdata=open('POSCAR-Na-C','w')
    indata_c=open('POSCAR-C','r')
    indata_na=open('na_center','r')
    content_c=indata_c.readlines()
    content_na=indata_na.readlines()
    na_num=len(content_na)
    c_num=len(content_c)-8
    for i in range(5):
        outdata.write(content_c[i])
    outdata.write(' C  Na \n')
    outdata.write(' %d  %d \n'%(c_num,na_num))
    outdata.write('Car \n')
    for i in range(8,len(content_c)):
        outdata.write(content_c[i])
    for i in range(len(content_na)):
        outdata.write(content_na[i])
    outdata.close()
    indata_c.close()
    indata_na.close()
    

def get_na_info(file):  #得到钠位点的所有坐标,使用笛卡尔坐标
    indata=open(file,'r')
    content=indata.readlines()
    na_num=len(content)
    na_weidain=[]  #坐标列表
    for i in range(len(content)):
        i_na_site=[]
        i_na_site.append(float(content[i].strip().split()[0]))
        i_na_site.append(float(content[i].strip().split()[1]))
        i_na_site.append(float(content[i].strip().split()[2]))
        na_weidain.append(i_na_site)
    return na_weidain

def get_carbon_info(file):  #使用笛卡尔坐标，读poscar文件
    indata = open(file, 'r')
    content = indata.readlines()
    carbon_num = len(content) - 8
    carbon_weidian = []
    for i in range(carbon_num):
        i_carbon_site = []
        i_carbon_site.append(float(content[i + 8].strip().split()[0]))
        i_carbon_site.append(float(content[i + 8].strip().split()[1]))
        i_carbon_site.append(float(content[i + 8].strip().split()[2]))
        carbon_weidian.append(i_carbon_site)
    jingge_vectorx = []
    jingge_vectory = []
    jingge_vectorz = []
    jingge_vectorx.append(float(content[2].strip().split()[0]));jingge_vectorx.append(float(content[2].strip().split()[1]));jingge_vectorx.append(float(content[2].strip().split()[2]))
    jingge_vectory.append(float(content[3].strip().split()[0]));jingge_vectory.append(float(content[3].strip().split()[1]));jingge_vectory.append(float(content[3].strip().split()[2]))
    jingge_vectorz.append(float(content[4].strip().split()[0]));jingge_vectorz.append(float(content[4].strip().split()[1]));jingge_vectorz.append(float(content[4].strip().split()[2]))
    jingge_vector=[jingge_vectorx,jingge_vectory,jingge_vectorz]
    return carbon_weidian, jingge_vector
    
    
homepath=os.getcwd()
na_file = 'na_center'   #可储钠的钠位点信息
carbon_file = 'POSCAR-C'    #硬碳骨架结构
get_pos_na_c(carbon_file,na_file)
    #cutoff_range=[i for i in range(3,11)]   #截断半径半径的个数和大小，要修改的位置
cutoff_range = [6]
na_weidain = get_na_info(na_file)
carbon_weidian, jingge_vector = get_carbon_info(carbon_file)

na_num=len(na_weidain)
c_num=len(carbon_weidian)


#cutoff=6
total_num=c_num+na_num
### hard carbon model
structure = read('POSCAR-Na-C')
#print(structure)
#structure.rattle(0.5)

desc = Descriptor("soap l_max=9 n_max=9 cutoff=6.0 atom_sigma=0.5 element='Na'")
element = ['Na']
#desc = Descriptor("soap cutoff=5.5 cutoff_transition_width=0.5 n_max=9 l_max=9 atom_sigma=0.55 n_Z=1 n_species=4 species_Z={11, 12, 25, 8}")

D1 = desc.calc(structure)['data'][c_num:total_num]   #将结构的对应原子序号的原子居于结构转化为结构描述符
#print(len(D1));print(len(D1['data']))
print(D1)   #转化成结构描述符后的特征矩阵，m*n的矩阵，m就是原子数量，n是对居于结构的特征描述符的个数
D = np.r_[D1]  #只是将数组之间的逗号去除，或者数组连接
print(D)
#labels = np.array([1] * len(D1))  #对矩阵内的每一组数据进行一个标签
#print(labels)
print(D.shape)  #返回数组的形状，有几行几列

# 使用PCA将多维特征降至二维
pca = PCA(n_components=2)
reduced_mat = pca.fit_transform(D[:, 2:]) 
print(reduced_mat.shape) 
print(reduced_mat) 
print(type(reduced_mat))

##提取配位数数据
indata=open(os.path.join(os.path.join(homepath,'8_voltage_dis_group'),'Na-Na-peiwei-number.dat'))
indata1=open(os.path.join(os.path.join(homepath,'8_voltage_dis_group'),'Na-C-distance-number.dat'))
content=indata.readlines()
content1=indata1.readlines()
a=[];b=[]
for i in range(len(content)):
    a.append(int(content[i].strip().split()[1]))
    b.append(float(content1[i].strip().split()[1]))

n=reduced_mat.shape[0]
add_matrix = []
for i in range(n):
    add_matrix.append([a[i]])
add_matrix1 = []
for i in range(n):
    add_matrix1.append([b[i]])
new_matrix = np.hstack((reduced_mat, add_matrix))      
new_matrix1 = np.hstack((reduced_mat, add_matrix1))   
print(new_matrix)
print(new_matrix1)  

x1 = new_matrix[:, 0]  # 取出第一列数据作为横坐标
y1 = new_matrix[:, 1]  # 取出第二列数据作为纵坐标
colors1 = new_matrix[:, 2]  # 取出第三列数据作为颜色

plt.scatter(x1, y1, c=colors1)
plt.colorbar()
plt.savefig('na_na_coor.png')
plt.close()

plt.figure()
 
x2 = new_matrix1[:, 0]  # 取出第一列数据作为横坐标
y2 = new_matrix1[:, 1]  # 取出第二列数据作为纵坐标
colors2 = new_matrix1[:, 2]  # 取出第三列数据作为颜色

plt.scatter(x2, y2, c=colors2)
plt.colorbar()
plt.savefig('na_C_coor.png') 
plt.close()
'''ones = np.ones((reduced_mat.shape[0], 1))
ones1 = np.ones((reduced_mat.shape[0], 1))
new_matrix = np.hstack((reduced_mat, ones)) 
new_matrix1 = np.hstack((reduced_mat, ones1)) 
print(new_matrix)
print(new_matrix1)'''
