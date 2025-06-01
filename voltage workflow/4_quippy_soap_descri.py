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

def get_pos_na_c(c_file,na_file):  #把钠原子和碳原子两个部分的结构合成一个包含满钠的结构文件
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
#print(D.shape)  #返回数组的形状，有几行几列


####利用sklearn进行聚类分析
k = 3  # k为需要分成的簇的数量
km = KMeans(n_clusters=k)
km.fit(D)

# 获取每个簇的中心点
centroids = km.cluster_centers_
print(centroids)

# 将每个坐标点对应的簇心索引存储到labels中
labels = km.labels_

# 分别获取每个簇的坐标点
cluster1 = D[labels == 0]
cluster2 = D[labels == 1]
cluster3 = D[labels == 2]

# 使用PCA将多维特征降至二维
pca = PCA(n_components=2)
reduced_mat = pca.fit_transform(D[:, 2:])   #所有点的降维
reduced_center = pca.fit_transform(centroids[:, 2:])    #簇中心点的降维
print(reduced_center)

# 将坐标点对应的簇心索引和值数据存储到reduced_feat_mat中
reduced_feat_mat = np.hstack((labels.reshape(-1, 1), D[:, :2], reduced_mat))
correspondence = np.hstack((D, reduced_feat_mat, labels.reshape(-1, 1)))  #找到降维前后数据的对应关系

# 分类记录，分类的局域环境记录到文件内
cluster1_index = []
cluster2_index = []
cluster3_index = []

for i in range(len(correspondence)):
    if correspondence[i][-1] == 0:
        cluster1_index.append(i)
    elif correspondence[i][-1] == 1:
        cluster2_index.append(i)
    elif correspondence[i][-1] == 2:
        cluster3_index.append(i)
#print(len(cluster1_index),len(cluster2_index),len(cluster3_index))
cluster_data = open(os.path.join(os.path.join(homepath,str(cutoff_range[0])),'cluster_classification.dat'), 'w')
cluster_data.write('cluster1 : ')
for i in cluster1_index:
    cluster_data.write(str(i) + '  ')
cluster_data.write('  \n')
cluster_data.write('cluster2 : ')
for i in cluster2_index:
    cluster_data.write(str(i) + '  ')
cluster_data.write('  \n')
cluster_data.write('cluster3 : ')
for i in cluster3_index:
    cluster_data.write(str(i) + '  ')
cluster_data.write('  \n')
cluster_data.close()


# 分别获取每个簇的坐标点
cluster1 = reduced_feat_mat[reduced_feat_mat[:, 0] == 0]
cluster2 = reduced_feat_mat[reduced_feat_mat[:, 0] == 1]
cluster3 = reduced_feat_mat[reduced_feat_mat[:, 0] == 2]
print(len(cluster1))
print(len(cluster2))
print(len(cluster3))
# 图形显示
plt.scatter(cluster1[:, 3], cluster1[:, 4], c='r', marker='o')
plt.scatter(cluster2[:, 3], cluster2[:, 4], c='g', marker='o')
plt.scatter(cluster3[:, 3], cluster3[:, 4], c='b', marker='o')
#plt.scatter(reduced_center[:, 0], reduced_center[:, 1], c='k', marker='^')
plt.savefig('pca.png')
#plt.show()








'''from quippy import descriptors
from ase import Atoms
cell = [[5.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 5.0]]
atoms = Atoms(n=8, lattice=cell, symbols=['C']*8,
              positions=[(0, 0, 0),
                         (0, 0, 2.5),
                         (2.5, 0, 0),
                         (2.5, 0, 2.5),
                         (0, 2.5, 0),
                         (0, 2.5, 2.5),
                         (2.5, 2.5, 0),
                         (2.5, 2.5, 2.5)])
soap = descriptors.Soap(l_max=3, r_cut=5.0, species=atoms.get_chemical_symbols())
desc = soap.calc(atoms)
print(desc.shape)'''