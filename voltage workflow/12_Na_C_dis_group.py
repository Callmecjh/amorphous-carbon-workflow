import numpy as np
import math
import time
import os
import glob
import LASP_PythonLib
from LASP_PythonLib.structure_new import Str
from LASP_PythonLib.allstr_new import allstr as allstr_new
import shutil

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
 
def calc_coor_num(na_weidian,jingge_vector,filename):  #截断半径5埃内每个Na周围的Na配位数汇总
    cutoff=5
    file_info = open(os.path.join(os.path.join(home_path,'8_voltage_dis_group'),filename),'w')
    for j in range(len(na_weidian)):
        j_coor_num = 0
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
                if min(j_k_dis) < cutoff:
                    j_coor_num += 1
        file_info.write(' %s   %s   \n' %(j,j_coor_num))
    file_info.close()
 
def calc_min_Na_C(na_weidian,carbon_weidian ,jingge_vector,filename): 
    file_info = open(os.path.join(os.path.join(home_path,'8_voltage_dis_group'),filename),'w')
    for j in range(len(na_weidian)):
        j_dis=[]
        for k in range(len(carbon_weidian)):
            j_k_dis=[]
            for m in [-1, 0, 1]:
                for n in [-1, 0, 1]:
                    for o in [-1, 0, 1]:
                        shift_x = m * jingge_vector[0][0] + n * jingge_vector[1][0] + o * jingge_vector[2][0]
                        shift_y = m * jingge_vector[0][1] + n * jingge_vector[1][1] + o * jingge_vector[2][1]
                        shift_z = m * jingge_vector[0][2] + n * jingge_vector[1][2] + o * jingge_vector[2][2]
                        jk_distance = math.sqrt((na_weidian[j][0] - carbon_weidian[k][0] - shift_x) ** 2 + (na_weidian[j][1] - carbon_weidian[k][1] - shift_y) ** 2 + (na_weidian[j][2] - carbon_weidian[k][2] - shift_z) ** 2)
                        j_k_dis.append(jk_distance)
            j_dis.append(min(j_k_dis))
        file_info.write('  %s   %s  \n'%(j,min(j_dis)))
    file_info.close()

def get_Na_Na_info():  #根据配位数多少进行分组
    indata=open(os.path.join(os.path.join(home_path,'8_voltage_dis_group'),'Na-Na-peiwei-number.dat'),'r')
    content = indata.readlines()
    a=[];b=[]
    for i in range(len(content)):
        a.append(int(content[i].strip().split()[0]))
        b.append(int(content[i].strip().split()[1]))
    avg=sum(b)/len(b)
    group_short=[]
    group_long=[]
    for i in range(len(b)):
        if b[i] < avg:
            group_short.append(i)
        else:
            group_long.append(i)
    indata.close()
    group_divide=open(os.path.join(os.path.join(home_path,'8_voltage_dis_group'),'group_divide.dat'),'w')
    group_divide.write('group short: ')
    for i in group_short:
        group_divide.write('%s '%i)
    group_divide.write('\n')
    group_divide.write('group long: ')
    for i in group_long:
        group_divide.write('%s '%i)
    group_divide.write('\n')
    group_divide.close()
    print(group_short)
    print(group_long)
    return group_short,group_long
    
def get_Na_C_info():  #根据Na-C距离多少进行分组
    indata=open(os.path.join(os.path.join(home_path,'8_voltage_dis_group'),'Na-C-distance-number.dat'),'r')
    content = indata.readlines()
    a=[];b=[]
    for i in range(len(content)):
        a.append(int(content[i].strip().split()[0]))
        b.append(float(content[i].strip().split()[1]))
    avg=sum(b)/len(b)
    group_short=[]
    group_long=[]
    for i in range(len(b)):
        if b[i] < avg:
            group_short.append(i)
        else:
            group_long.append(i)
    indata.close()
    group_divide=open(os.path.join(os.path.join(home_path,'8_voltage_dis_group'),'group_divide_Na_C.dat'),'w')
    group_divide.write('group short: ')
    for i in group_short:
        group_divide.write('%s '%i)
    group_divide.write('\n')
    group_divide.write('group long: ')
    for i in group_long:
        group_divide.write('%s '%i)
    group_divide.write('\n')
    group_divide.close()
    print(group_short)
    print(group_long)
    return group_short,group_long

def generate_vasp_file_Na_C(path,na_weidian,carbon_weidian, jingge_vector,cluster1_index,cluster2_index):
    if not glob.glob(os.path.join(path,'12_C')):
        os.mkdir(os.path.join(path,'12_C'))
    if not glob.glob(os.path.join(path,'21_C')):
        os.mkdir(os.path.join(path,'21_C'))
    index_12=cluster1_index+cluster2_index
    index_21=cluster2_index+cluster1_index  
    for i in range(1,len(index_12)+1):
        na_site_1 = []
        for j in range(i):
            na_site_1.append(na_weidian[index_12[j]])
        filename = '%d.vasp'%i
        out_name = '%d.arc' % i
        pos_path = os.path.join(path,'12_C')
        poscar(pos_path, filename, na_site_1, carbon_weidian, jingge_vector)
        pos_arc(pos_path, filename, out_name)
    for i in range(1,len(index_21)+1):
        na_site_1 = []
        for j in range(i):
            na_site_1.append(na_weidian[index_21[j]])
        filename = '%d.vasp'%i
        out_name = '%d.arc' % i
        pos_path = os.path.join(path,'21_C')
        poscar(pos_path, filename, na_site_1, carbon_weidian, jingge_vector)
        pos_arc(pos_path, filename, out_name)
    
def generate_vasp_file(path,na_weidian,carbon_weidian, jingge_vector,cluster1_index,cluster2_index):
    if not glob.glob(os.path.join(path,'12')):
        os.mkdir(os.path.join(path,'12'))
    if not glob.glob(os.path.join(path,'21')):
        os.mkdir(os.path.join(path,'21'))
    index_12=cluster1_index+cluster2_index
    index_21=cluster2_index+cluster1_index  
    for i in range(1,len(index_12)+1):
        na_site_1 = []
        for j in range(i):
            na_site_1.append(na_weidian[index_12[j]])
        filename = '%d.vasp'%i
        out_name = '%d.arc' % i
        pos_path = os.path.join(path,'12')
        poscar(pos_path, filename, na_site_1, carbon_weidian, jingge_vector)
        pos_arc(pos_path, filename, out_name)
    for i in range(1,len(index_21)+1):
        na_site_1 = []
        for j in range(i):
            na_site_1.append(na_weidian[index_21[j]])
        filename = '%d.vasp'%i
        out_name = '%d.arc' % i
        pos_path = os.path.join(path,'21')
        poscar(pos_path, filename, na_site_1, carbon_weidian, jingge_vector)
        pos_arc(pos_path, filename, out_name)

def poscar(path, filename, na_site, carbon_weidian, jingge_vector):  ###生成poscar文件
    output = open(os.path.join(path, filename), 'w')
    output.write('poscar \n')
    output.write('1 \n')
    output.write('%s   %s   %s \n' % (str(jingge_vector[0][0]), str(jingge_vector[0][1]), str(jingge_vector[0][2])))
    output.write('%s   %s   %s \n' % (str(jingge_vector[1][0]), str(jingge_vector[1][1]), str(jingge_vector[1][2])))
    output.write('%s   %s   %s \n' % (str(jingge_vector[2][0]), str(jingge_vector[2][1]), str(jingge_vector[2][2])))
    car_num = len(carbon_weidian)
    na_num = len(na_site)
    output.write(' C   Na \n')
    output.write(' %d  %d \n'%(car_num,na_num))
    output.write('Car \n')
    for i in range(len(carbon_weidian)):
        output.write('%s   %s   %s \n' % (str(carbon_weidian[i][0]), str(carbon_weidian[i][1]), str(carbon_weidian[i][2])))
    for i in range(len(na_site)):
        output.write('%s   %s   %s \n' % (str(na_site[i][0]), str(na_site[i][1]), str(na_site[i][2])))
    output.close()        

def pos_arc(path,file_name,out_name):
    AllStr = allstr_new()
    name=os.path.join(path,file_name)
    out_name_new = os.path.join(path,out_name)
    AllStr.BuildCoordSet_fromPOSCAR(filename=name)
    AllStr.Gen_arc(range(len(AllStr)), out_name_new, 2)    
 
def file_prepare(home_path,gene_path,cluster_num):
    cluster1_path=os.path.join(gene_path,'12')
    cluster2_path=os.path.join(gene_path,'21')   
    for i in range(1, cluster_num + 1):
        os.mkdir(os.path.join(cluster1_path,'%d-single' % i))
        #os.mkdir(os.path.join(cluster1_path,'%d-ssw' % i))
        shutil.copy(os.path.join(cluster1_path,'%d.arc'%i),os.path.join(os.path.join(cluster1_path,'%d-single' % i),'input.arc'))
        #shutil.copy(os.path.join(cluster1_path, '%d.arc' % i),os.path.join(os.path.join(cluster1_path, '%d-ssw' % i), 'input.arc'))
        shutil.copy(os.path.join(home_path, 'NaC.pot'), os.path.join(os.path.join(cluster1_path, '%d-single' % i), 'NaC.pot'))
        #shutil.copy(os.path.join(home_path, 'NaC.pot'),os.path.join(os.path.join(cluster1_path, '%d-ssw' % i), 'NaC.pot'))
        shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster1_path, '%d-single' % i), 'lasp.slurm'))
        #shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster1_path, '%d-ssw' % i), 'lasp.slurm'))
        shutil.copy(os.path.join(home_path, 'lasp-single.in'),os.path.join(os.path.join(cluster1_path, '%d-single' % i), 'lasp.in'))
        #shutil.copy(os.path.join(home_path, 'lasp-ssw.in'),os.path.join(os.path.join(cluster1_path, '%d-ssw' % i), 'lasp.in'))
        os.remove(os.path.join(cluster1_path, '%d.arc'%i))
        os.remove(os.path.join(cluster1_path, '%d.vasp'%i))

    for i in range(1, cluster_num + 1):
        os.mkdir(os.path.join(cluster2_path,'%d-single' % i))
        #os.mkdir(os.path.join(cluster2_path,'%d-ssw' % i))
        shutil.copy(os.path.join(cluster2_path,'%d.arc'%i),os.path.join(os.path.join(cluster2_path,'%d-single' % i),'input.arc'))
        #shutil.copy(os.path.join(cluster2_path, '%d.arc' % i),os.path.join(os.path.join(cluster2_path, '%d-ssw' % i), 'input.arc'))
        shutil.copy(os.path.join(home_path, 'NaC.pot'), os.path.join(os.path.join(cluster2_path, '%d-single' % i), 'NaC.pot'))
        #shutil.copy(os.path.join(home_path, 'NaC.pot'),os.path.join(os.path.join(cluster2_path, '%d-ssw' % i), 'NaC.pot'))
        shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster2_path, '%d-single' % i), 'lasp.slurm'))
        #shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster2_path, '%d-ssw' % i), 'lasp.slurm'))
        shutil.copy(os.path.join(home_path, 'lasp-single.in'),os.path.join(os.path.join(cluster2_path, '%d-single' % i), 'lasp.in'))
        #shutil.copy(os.path.join(home_path, 'lasp-ssw.in'),os.path.join(os.path.join(cluster2_path, '%d-ssw' % i), 'lasp.in'))
        os.remove(os.path.join(cluster2_path, '%d.arc'%i))
        os.remove(os.path.join(cluster2_path, '%d.vasp'%i))
    
def file_prepare_Na_C(home_path,gene_path,cluster_num):
    cluster1_path=os.path.join(gene_path,'12_C')
    cluster2_path=os.path.join(gene_path,'21_C')   
    for i in range(1, cluster_num + 1):
        os.mkdir(os.path.join(cluster1_path,'%d-single' % i))
        #os.mkdir(os.path.join(cluster1_path,'%d-ssw' % i))
        shutil.copy(os.path.join(cluster1_path,'%d.arc'%i),os.path.join(os.path.join(cluster1_path,'%d-single' % i),'input.arc'))
        #shutil.copy(os.path.join(cluster1_path, '%d.arc' % i),os.path.join(os.path.join(cluster1_path, '%d-ssw' % i), 'input.arc'))
        shutil.copy(os.path.join(home_path, 'NaC.pot'), os.path.join(os.path.join(cluster1_path, '%d-single' % i), 'NaC.pot'))
        #shutil.copy(os.path.join(home_path, 'NaC.pot'),os.path.join(os.path.join(cluster1_path, '%d-ssw' % i), 'NaC.pot'))
        shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster1_path, '%d-single' % i), 'lasp.slurm'))
        #shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster1_path, '%d-ssw' % i), 'lasp.slurm'))
        shutil.copy(os.path.join(home_path, 'lasp-single.in'),os.path.join(os.path.join(cluster1_path, '%d-single' % i), 'lasp.in'))
        #shutil.copy(os.path.join(home_path, 'lasp-ssw.in'),os.path.join(os.path.join(cluster1_path, '%d-ssw' % i), 'lasp.in'))
        os.remove(os.path.join(cluster1_path, '%d.arc'%i))
        os.remove(os.path.join(cluster1_path, '%d.vasp'%i))

    for i in range(1, cluster_num + 1):
        os.mkdir(os.path.join(cluster2_path,'%d-single' % i))
        #os.mkdir(os.path.join(cluster2_path,'%d-ssw' % i))
        shutil.copy(os.path.join(cluster2_path,'%d.arc'%i),os.path.join(os.path.join(cluster2_path,'%d-single' % i),'input.arc'))
        #shutil.copy(os.path.join(cluster2_path, '%d.arc' % i),os.path.join(os.path.join(cluster2_path, '%d-ssw' % i), 'input.arc'))
        shutil.copy(os.path.join(home_path, 'NaC.pot'), os.path.join(os.path.join(cluster2_path, '%d-single' % i), 'NaC.pot'))
        #shutil.copy(os.path.join(home_path, 'NaC.pot'),os.path.join(os.path.join(cluster2_path, '%d-ssw' % i), 'NaC.pot'))
        shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster2_path, '%d-single' % i), 'lasp.slurm'))
        #shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster2_path, '%d-ssw' % i), 'lasp.slurm'))
        shutil.copy(os.path.join(home_path, 'lasp-single.in'),os.path.join(os.path.join(cluster2_path, '%d-single' % i), 'lasp.in'))
        #shutil.copy(os.path.join(home_path, 'lasp-ssw.in'),os.path.join(os.path.join(cluster2_path, '%d-ssw' % i), 'lasp.in'))
        os.remove(os.path.join(cluster2_path, '%d.arc'%i))
        os.remove(os.path.join(cluster2_path, '%d.vasp'%i))
    
 
if __name__ == '__main__':
    start_time = time.time()
    global home_path
    home_path = os.getcwd()
    if not glob.glob(os.path.join(home_path,'8_voltage_dis_group')):
        os.mkdir(os.path.join(home_path,'8_voltage_dis_group'))
    na_file = 'na_center'
    carbon_file = 'POSCAR-C'    #硬碳骨架结构
    na_weidian = get_na_info(na_file)
    carbon_weidian, jingge_vector = get_carbon_info(carbon_file)
    filename='Na-Na-peiwei-number.dat'
    calc_coor_num(na_weidian,jingge_vector,filename)
    filename1='Na-C-distance-number.dat'
    calc_min_Na_C(na_weidian,carbon_weidian ,jingge_vector,filename1)
    group_short,group_long=get_Na_Na_info()
    path=os.path.join(home_path,'8_voltage_dis_group')
    generate_vasp_file(path,na_weidian,carbon_weidian, jingge_vector,group_short,group_long)
    cluster_num=len(group_short)+len(group_long)
    file_prepare(home_path,path,cluster_num)     
    group_short_na_c,group_long_na_c=get_Na_C_info()
    cluster_num=len(group_short_na_c)+len(group_long_na_c)
    print(len(group_short_na_c),len(group_long_na_c))
    generate_vasp_file_Na_C(path,na_weidian,carbon_weidian, jingge_vector,group_short_na_c,group_long_na_c)
    file_prepare_Na_C(home_path,path,cluster_num)
    end_time = time.time()
    print('total cost time: ', end_time-start_time)
