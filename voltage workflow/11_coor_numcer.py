import numpy as np
import math
import time
import os
import glob


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
    
def calc_coor_num(na_weidian,jingge_vector,filename): 
    #length_range=[0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]
    length_range=np.linspace(0.5, 6.5, 31)
    print(length_range)
    file_info = open(filename,'w')
    for i in range(len(length_range)):
        coor_num = 0
        for j in range(len(na_weidian)):
            for k in range(len(na_weidian)):
                if j != k:
                    j_k_dis = []
                    for m in [-1, 0, 1]:
                        for n in [-1, 0, 1]:
                            for o in [-1, 0, 1]:
                                shift_x = m * jingge_vector[0][0] + n * jingge_vector[1][0] + o * jingge_vector[2][0]
                                shift_y = m * jingge_vector[0][1] + n * jingge_vector[1][1] + o * jingge_vector[2][1]
                                shift_z = m * jingge_vector[0][2] + n * jingge_vector[1][2] + o * jingge_vector[2][2]
                                jk_distance = math.sqrt((na_weidian[j][0] - na_weidian[k][0] - shift_x) ** 2 + (na_weidian[j][1] - na_weidian[k][1] - shift_y) ** 2 + (na_weidian[j][2] - na_weidian[k][2] - shift_z) ** 2)
                                j_k_dis.append(jk_distance)
                    if min(j_k_dis) < length_range[i]:
                        coor_num += 1
                    else:
                        pass
        file_info.write(' %s   %s   \n'%(length_range[i],coor_num/len(na_weidian)))
    file_info.close()
    

   
    
if __name__ == '__main__':
    start_time = time.time()
    home_path = os.getcwd()
    na_file_1 = 'na_center_1'   #可储钠的钠位点信息
    na_file_2 = 'na_center_2'
    na_file_3 = 'na_center_3'
    carbon_file = 'POSCAR-C'    #硬碳骨架结构
    na_weidian_1 = get_na_info(na_file_1)
    na_weidian_2 = get_na_info(na_file_2)
    na_weidian_3 = get_na_info(na_file_3)
    carbon_weidian, jingge_vector = get_carbon_info(carbon_file)
    calc_coor_num(na_weidian_1,jingge_vector,'coor_num_1.dat')
    calc_coor_num(na_weidian_2,jingge_vector,'coor_num_2.dat')
    calc_coor_num(na_weidian_3,jingge_vector,'coor_num_3.dat')
    end_time = time.time()
    print('total cost time: ', end_time-start_time)
    
    
    
    
    
    
    