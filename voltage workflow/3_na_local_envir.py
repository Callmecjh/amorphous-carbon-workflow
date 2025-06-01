import numpy as np
import math
import time
import os
import glob


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

def ouput_local_envir(na_weidian,carbon_weidian,jingge_vector,cutoff_range):  #输出每个10埃截断半径局域环境，这里3，4，5，6，7的截断半径都输出做一个对比
    na_num=len(na_weidian)
    #cutoff_range=[i for i in range(3,11)]   #截断半径半径的个数和大小，要修改的位置
    for i in cutoff_range:
        if not glob.glob('%s'%(str(i))):
            os.mkdir('%s'%(str(i)))
    for i in range(len(na_weidian)):
        i_match = [[] for j in range(len(cutoff_range))]
        for j in range(len(carbon_weidian)):
            i_j_dis = []
            for m in [-1, 0, 1]:
                for n in [-1, 0, 1]:
                    for o in [-1, 0, 1]:
                        shift_x = m * jingge_vector[0][0] + n * jingge_vector[1][0] + o * jingge_vector[2][0]
                        shift_y = m * jingge_vector[0][1] + n * jingge_vector[1][1] + o * jingge_vector[2][1]
                        shift_z = m * jingge_vector[0][2] + n * jingge_vector[1][2] + o * jingge_vector[2][2]
                        ij_distance = math.sqrt((na_weidian[i][0] - carbon_weidian[j][0] - shift_x) ** 2 + (na_weidian[i][1] - carbon_weidian[j][1] - shift_y) ** 2 + (na_weidian[i][2] - carbon_weidian[j][2] - shift_z) ** 2)
                        i_j_dis.append(ij_distance)
            for k in range(len(cutoff_range)):
                if min(i_j_dis) < cutoff_range[k]:
                    i_match[k].append(carbon_weidian[j])
                else:
                    pass
        for k in range(len(cutoff_range)):
            path = os.path.join(home_path, str(cutoff_range[k]))
            poscar(path, str(i) + '.vasp', na_weidain[i], i_match[k], jingge_vector)


def poscar(path,filename,na_site,na_match,jingge_vector):  ###生成poscar文件
    output = open(os.path.join(path,filename),'w')
    output.write('poscar \n')
    output.write('1 \n')
    output.write('%s   %s   %s \n'%(str(jingge_vector[0][0]), str(jingge_vector[0][1]), str(jingge_vector[0][2])))
    output.write('%s   %s   %s \n' % (str(jingge_vector[1][0]), str(jingge_vector[1][1]), str(jingge_vector[1][2])))
    output.write('%s   %s   %s \n' % (str(jingge_vector[2][0]), str(jingge_vector[2][1]), str(jingge_vector[2][2])))
    if len(na_match) == 0:
        output.write('  Na \n')
        output.write('  1 \n' )
        output.write('Car \n')
        output.write('%s   %s   %s \n' % (str(na_site[0]), str(na_site[1]), str(na_site[2])))
    else:
        output.write('  Na  C \n')
        output.write('  1  %d \n' % (len(na_match)))
        output.write('Car \n')
        output.write('%s   %s   %s \n' % (str(na_site[0]), str(na_site[1]), str(na_site[2])))
        for i in range(len(na_match)):
            output.write('%s   %s   %s \n' % (str(na_match[i][0]), str(na_match[i][1]), str(na_match[i][2])))
    output.close()


if __name__ == '__main__':
    start_time = time.time()
    home_path = os.getcwd()
    na_file = 'na_center'   #可储钠的钠位点信息
    carbon_file = 'POSCAR-C'    #硬碳骨架结构
    get_pos_na_c(carbon_file,na_file)
    #cutoff_range=[i for i in range(3,11)]   #截断半径半径的个数和大小，要修改的位置
    cutoff_range = [6]
    na_weidain = get_na_info(na_file)
    carbon_weidian, jingge_vector = get_carbon_info(carbon_file)
    ouput_local_envir(na_weidain,carbon_weidian,jingge_vector,cutoff_range)    #生成所有的截断半径内的poscar文件
    end_time = time.time()
    print('total cost time: ', end_time - start_time)