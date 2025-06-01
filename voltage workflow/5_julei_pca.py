
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from mpl_toolkits.mplot3d import Axes3D


def get_data(path,filename):
    vector_file = open(os.path.join(path,filename),'r')
    content = vector_file.readlines()
    x_data = []
    y_target = []
    z_target = []
    for i in range(len(content)):
        i_content = content[i].replace(',','').replace('[','').replace(']','')
        i_content_new = i_content.split()
        x_data.append([float(i_content_new[0]),float(i_content_new[1]),float(i_content_new[2])])
        y_target.append(float(i_content_new[3]))
        z_target.append(float(i_content_new[4]))
    vector_file.close()
    return x_data,y_target,z_target



if __name__ == '__main__':
    home_path = os.getcwd()
    cutoff_range = 6
    path = os.path.join(home_path,str(cutoff_range))
    coords = np.loadtxt(os.path.join(path,"coords.txt"))
    val1 = np.loadtxt(os.path.join(path, "val1.txt"))
    val2 = np.loadtxt(os.path.join(path, "val2.txt"))
    # 将val1和val2数组按照列方向合并为一个特征矩阵feat_mat
    feat_mat = np.hstack((val1.reshape(-1, 1), val2.reshape(-1, 1), coords))
    print(feat_mat)
    #print(feat_mat[0])
    # 构建KMeans模型，将数据分为k个簇
    k = 3  # k为需要分成的簇的数量
    km = KMeans(n_clusters=k)
    km.fit(feat_mat)

    # 获取每个簇的中心点
    centroids = km.cluster_centers_
    print(centroids)

    # 将每个坐标点对应的簇心索引存储到labels中
    labels = km.labels_

    # 分别获取每个簇的坐标点
    cluster1 = feat_mat[labels == 0]
    cluster2 = feat_mat[labels == 1]
    cluster3 = feat_mat[labels == 2]
    #print(len(cluster1),len(cluster2),len(cluster3))
    #print(cluster1)
    #print(cluster2)
    #print(cluster3)


    # 使用PCA将三维特征降至二维
    pca = PCA(n_components=2)
    reduced_mat = pca.fit_transform(feat_mat[:, 2:])   #所有点的降维
    reduced_center = pca.fit_transform(centroids[:, 2:])    #簇中心点的降维
    print(reduced_center)

    # 将坐标点对应的簇心索引和值数据存储到reduced_feat_mat中
    reduced_feat_mat = np.hstack((labels.reshape(-1, 1), feat_mat[:, :2], reduced_mat))
    correspondence = np.hstack((feat_mat, reduced_feat_mat, labels.reshape(-1, 1)))  #找到降维前后数据的对应关系

    #print("原始数据（三维）与聚类后的数据（二维）的对应关系：")
    #print(np.hstack((correspondence[:, :5], correspondence[:, 5:7], correspondence[:, 7:])))
    #print(correspondence)

    # 分类记录
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
    cluster_data = open(os.path.join(os.path.join(home_path, str(6)), 'cluster_classification.dat'), 'w')
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
    plt.scatter(cluster1[:, 3], cluster1[:, 4], c='r', marker='o',s=80)
    plt.scatter(cluster2[:, 3], cluster2[:, 4], c='g', marker='o',s=80)
    plt.scatter(cluster3[:, 3], cluster3[:, 4], c='b', marker='o',s=80)
    plt.scatter(reduced_center[:, 0], reduced_center[:, 1], c='k', marker='^')
    plt.yticks(fontsize=20)
    plt.xticks(fontsize=20)
    
    
    ax = plt.gca()
    ax.spines['top'].set_linewidth(4)
    ax.spines['right'].set_linewidth(4)
    ax.spines['left'].set_linewidth(4)
    ax.spines['bottom'].set_linewidth(4)
    plt.savefig('pca-wenzhang.png')
    plt.show()






