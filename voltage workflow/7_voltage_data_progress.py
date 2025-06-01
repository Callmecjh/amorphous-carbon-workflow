'''import numpy as np
import math
import time
import os
import glob
import LASP_PythonLib
from LASP_PythonLib.structure_new import Str
from LASP_PythonLib.allstr_new import allstr as allstr_new

def cluster_info(path):
    cluster_data = open(os.path.join(path,'cluster_classification.dat'))
    content = cluster_data.readlines()
    cluster1_index = []
    cluster2_index = []
    cluster3_index = []
    #for i in range(len(content)):
    one_content_new = content[0].replace(':','')
    one_content = one_content_new.strip().split()
    for i in range(1,len(one_content)):
        cluster1_index.append(int(one_content[i]))
    two_content_new = content[1].replace(':', '')
    two_content = two_content_new.strip().split()
    for i in range(1, len(two_content)):
        cluster2_index.append(int(two_content[i]))
    three_content_new = content[2].replace(':', '')
    three_content = three_content_new.strip().split()
    for i in range(1, len(three_content)):
        cluster3_index.append(int(three_content[i]))
    return cluster1_index,cluster2_index,cluster3_index

def energy_progress(path,cluster_num):
    energy=open(os.path.join(path,'energy.dat'),'w')
    for i in range(1,cluster_num+1):
        with open(os.path.join(os.path.join(path, '%d-single' % i), 'lasp.out'), 'r') as n:
            content = n.readlines()
            total_line = len(content)
            # nn_energy=str(content[total_line-3].split()[1])
            #print(str(content[total_line - 3].split()[0]))
            nn_energy_single = 'false'
            for j in range(total_line):
                text = content[j].split()
                if len(text) != 0 and str(text[0]) == 'Energy,force':
                    nn_energy_single = float(text[1])
                else:
                    pass
        with open(os.path.join(os.path.join(path, '%d-ssw' % i), 'lasp.out'), 'r') as n:
            content = n.readlines()
            total_line = len(content)
            # nn_energy=str(content[total_line-3].split()[1])
            #print(str(content[total_line - 3].split()[0]))
            nn_energy_ssw = 'false'
            for j in range(total_line):
                text = content[j].split()
                if len(text) != 0 and str(text[0]) == 'minimum':
                    nn_energy_ssw = float(text[5])
                else:
                    pass
        energy.write('%d    %f    %f  \n'%(i,nn_energy_single,nn_energy_ssw))
    energy.close()



if __name__ == '__main__':
    start_time = time.time()
    home_path = os.getcwd()
    gene_path = os.path.join(home_path, '%s_voltage' % (str(6)))
    path = os.path.join(home_path, str(6))
    cluster1_index, cluster2_index, cluster3_index = cluster_info(path)
    cluster1_num = len(cluster1_index)
    cluster2_num = len(cluster2_index)
    cluster3_num = len(cluster3_index)
    cluster1_path = os.path.join(gene_path, '1_cluster')
    cluster2_path = os.path.join(gene_path, '2_cluster')
    cluster3_path = os.path.join(gene_path, '3_cluster')
    energy_progress(cluster1_path, cluster1_num)
    energy_progress(cluster2_path, cluster2_num)
    energy_progress(cluster3_path, cluster3_num)'''


import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# 创建数据
x = np.arange(-1, 1, 0.2)
y = np.arange(-1, 1, 0.2)
z = np.arange(-1, 1, 0.2)
xx, yy, zz = np.meshgrid(x, y, z)

# 绘制3D图形
fig = plt.figure()
ax = Axes3D(fig)

ax.scatter(xx, yy, zz, c='r', marker='o')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()