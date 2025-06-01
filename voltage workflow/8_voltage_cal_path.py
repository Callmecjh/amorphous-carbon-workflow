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
    
def generate_vasp_file(path,na_weidain,carbon_weidian, jingge_vector,cluster1_index,cluster2_index,cluster3_index):
    if not glob.glob(os.path.join(path,'132')):
        os.mkdir(os.path.join(path,'132'))
    if not glob.glob(os.path.join(path,'213')):
        os.mkdir(os.path.join(path,'213'))
    if not glob.glob(os.path.join(path,'231')):
        os.mkdir(os.path.join(path,'231'))
    if not glob.glob(os.path.join(path,'312')):
        os.mkdir(os.path.join(path,'312'))
    if not glob.glob(os.path.join(path,'321')):
        os.mkdir(os.path.join(path,'321'))
    index_132=cluster1_index+cluster3_index+cluster2_index
    index_213=cluster2_index+cluster1_index+cluster3_index
    index_231=cluster2_index+cluster3_index+cluster1_index
    index_312=cluster3_index+cluster1_index+cluster2_index
    index_321=cluster3_index+cluster2_index+cluster1_index       
    for i in range(1,len(index_132)+1):
        na_site_1 = []
        for j in range(i):
            na_site_1.append(na_weidain[index_132[j]])
        filename = '%d.vasp'%i
        out_name = '%d.arc' % i
        pos_path = os.path.join(path,'132')
        poscar(pos_path, filename, na_site_1, carbon_weidian, jingge_vector)
        pos_arc(pos_path, filename, out_name)
    for i in range(1,len(index_213)+1):
        na_site_1 = []
        for j in range(i):
            na_site_1.append(na_weidain[index_213[j]])
        filename = '%d.vasp'%i
        out_name = '%d.arc' % i
        pos_path = os.path.join(path,'213')
        poscar(pos_path, filename, na_site_1, carbon_weidian, jingge_vector)
        pos_arc(pos_path, filename, out_name)
    for i in range(1,len(index_231)+1):
        na_site_1 = []
        for j in range(i):
            na_site_1.append(na_weidain[index_231[j]])
        filename = '%d.vasp'%i
        out_name = '%d.arc' % i
        pos_path = os.path.join(path,'231')
        poscar(pos_path, filename, na_site_1, carbon_weidian, jingge_vector)
        pos_arc(pos_path, filename, out_name)
    for i in range(1,len(index_312)+1):
        na_site_1 = []
        for j in range(i):
            na_site_1.append(na_weidain[index_312[j]])
        filename = '%d.vasp'%i
        out_name = '%d.arc' % i
        pos_path = os.path.join(path,'312')
        poscar(pos_path, filename, na_site_1, carbon_weidian, jingge_vector)
        pos_arc(pos_path, filename, out_name)
    for i in range(1,len(index_321)+1):
        na_site_1 = []
        for j in range(i):
            na_site_1.append(na_weidain[index_321[j]])
        filename = '%d.vasp'%i
        out_name = '%d.arc' % i
        pos_path = os.path.join(path,'321')
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
    cluster1_path=os.path.join(gene_path,'132')
    cluster2_path=os.path.join(gene_path,'213')
    cluster3_path=os.path.join(gene_path,'231')
    cluster4_path=os.path.join(gene_path,'312')
    cluster5_path=os.path.join(gene_path,'321')
    for i in range(1, cluster_num + 1):
        os.mkdir(os.path.join(cluster1_path,'%d-single' % i))
        os.mkdir(os.path.join(cluster1_path,'%d-ssw' % i))
        shutil.copy(os.path.join(cluster1_path,'%d.arc'%i),os.path.join(os.path.join(cluster1_path,'%d-single' % i),'input.arc'))
        shutil.copy(os.path.join(cluster1_path, '%d.arc' % i),os.path.join(os.path.join(cluster1_path, '%d-ssw' % i), 'input.arc'))
        shutil.copy(os.path.join(home_path, 'NaC.pot'), os.path.join(os.path.join(cluster1_path, '%d-single' % i), 'NaC.pot'))
        shutil.copy(os.path.join(home_path, 'NaC.pot'),os.path.join(os.path.join(cluster1_path, '%d-ssw' % i), 'NaC.pot'))
        shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster1_path, '%d-single' % i), 'lasp.slurm'))
        shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster1_path, '%d-ssw' % i), 'lasp.slurm'))
        shutil.copy(os.path.join(home_path, 'lasp-single.in'),os.path.join(os.path.join(cluster1_path, '%d-single' % i), 'lasp.in'))
        shutil.copy(os.path.join(home_path, 'lasp-ssw.in'),os.path.join(os.path.join(cluster1_path, '%d-ssw' % i), 'lasp.in'))
        os.remove(os.path.join(cluster1_path, '%d.arc'%i))
        os.remove(os.path.join(cluster1_path, '%d.vasp'%i))


    for i in range(1, cluster_num + 1):
        os.mkdir(os.path.join(cluster2_path,'%d-single' % i))
        os.mkdir(os.path.join(cluster2_path,'%d-ssw' % i))
        shutil.copy(os.path.join(cluster2_path,'%d.arc'%i),os.path.join(os.path.join(cluster2_path,'%d-single' % i),'input.arc'))
        shutil.copy(os.path.join(cluster2_path, '%d.arc' % i),os.path.join(os.path.join(cluster2_path, '%d-ssw' % i), 'input.arc'))
        shutil.copy(os.path.join(home_path, 'NaC.pot'), os.path.join(os.path.join(cluster2_path, '%d-single' % i), 'NaC.pot'))
        shutil.copy(os.path.join(home_path, 'NaC.pot'),os.path.join(os.path.join(cluster2_path, '%d-ssw' % i), 'NaC.pot'))
        shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster2_path, '%d-single' % i), 'lasp.slurm'))
        shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster2_path, '%d-ssw' % i), 'lasp.slurm'))
        shutil.copy(os.path.join(home_path, 'lasp-single.in'),os.path.join(os.path.join(cluster2_path, '%d-single' % i), 'lasp.in'))
        shutil.copy(os.path.join(home_path, 'lasp-ssw.in'),os.path.join(os.path.join(cluster2_path, '%d-ssw' % i), 'lasp.in'))
        os.remove(os.path.join(cluster2_path, '%d.arc'%i))
        os.remove(os.path.join(cluster2_path, '%d.vasp'%i))
    

    for i in range(1, cluster_num + 1):
        os.mkdir(os.path.join(cluster3_path,'%d-single' % i))
        os.mkdir(os.path.join(cluster3_path,'%d-ssw' % i))
        shutil.copy(os.path.join(cluster3_path,'%d.arc'%i),os.path.join(os.path.join(cluster3_path,'%d-single' % i),'input.arc'))
        shutil.copy(os.path.join(cluster3_path, '%d.arc' % i),os.path.join(os.path.join(cluster3_path, '%d-ssw' % i), 'input.arc'))
        shutil.copy(os.path.join(home_path, 'NaC.pot'), os.path.join(os.path.join(cluster3_path, '%d-single' % i), 'NaC.pot'))
        shutil.copy(os.path.join(home_path, 'NaC.pot'),os.path.join(os.path.join(cluster3_path, '%d-ssw' % i), 'NaC.pot'))
        shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster3_path, '%d-single' % i), 'lasp.slurm'))
        shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster3_path, '%d-ssw' % i), 'lasp.slurm'))
        shutil.copy(os.path.join(home_path, 'lasp-single.in'),os.path.join(os.path.join(cluster3_path, '%d-single' % i), 'lasp.in'))
        shutil.copy(os.path.join(home_path, 'lasp-ssw.in'),os.path.join(os.path.join(cluster3_path, '%d-ssw' % i), 'lasp.in'))
        os.remove(os.path.join(cluster3_path, '%d.arc'%i))
        os.remove(os.path.join(cluster3_path, '%d.vasp'%i))
    

    for i in range(1, cluster_num + 1):
        os.mkdir(os.path.join(cluster4_path,'%d-single' % i))
        os.mkdir(os.path.join(cluster4_path,'%d-ssw' % i))
        shutil.copy(os.path.join(cluster4_path,'%d.arc'%i),os.path.join(os.path.join(cluster4_path,'%d-single' % i),'input.arc'))
        shutil.copy(os.path.join(cluster4_path, '%d.arc' % i),os.path.join(os.path.join(cluster4_path, '%d-ssw' % i), 'input.arc'))
        shutil.copy(os.path.join(home_path, 'NaC.pot'), os.path.join(os.path.join(cluster4_path, '%d-single' % i), 'NaC.pot'))
        shutil.copy(os.path.join(home_path, 'NaC.pot'),os.path.join(os.path.join(cluster4_path, '%d-ssw' % i), 'NaC.pot'))
        shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster4_path, '%d-single' % i), 'lasp.slurm'))
        shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster4_path, '%d-ssw' % i), 'lasp.slurm'))
        shutil.copy(os.path.join(home_path, 'lasp-single.in'),os.path.join(os.path.join(cluster4_path, '%d-single' % i), 'lasp.in'))
        shutil.copy(os.path.join(home_path, 'lasp-ssw.in'),os.path.join(os.path.join(cluster4_path, '%d-ssw' % i), 'lasp.in'))
        os.remove(os.path.join(cluster4_path, '%d.arc'%i))
        os.remove(os.path.join(cluster4_path, '%d.vasp'%i))
    
    for i in range(1, cluster_num + 1):
        os.mkdir(os.path.join(cluster5_path,'%d-single' % i))
        os.mkdir(os.path.join(cluster5_path,'%d-ssw' % i))
        shutil.copy(os.path.join(cluster5_path,'%d.arc'%i),os.path.join(os.path.join(cluster5_path,'%d-single' % i),'input.arc'))
        shutil.copy(os.path.join(cluster5_path, '%d.arc' % i),os.path.join(os.path.join(cluster5_path, '%d-ssw' % i), 'input.arc'))
        shutil.copy(os.path.join(home_path, 'NaC.pot'), os.path.join(os.path.join(cluster5_path, '%d-single' % i), 'NaC.pot'))
        shutil.copy(os.path.join(home_path, 'NaC.pot'),os.path.join(os.path.join(cluster5_path, '%d-ssw' % i), 'NaC.pot'))
        shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster5_path, '%d-single' % i), 'lasp.slurm'))
        shutil.copy(os.path.join(home_path, 'lasp.slurm'),os.path.join(os.path.join(cluster5_path, '%d-ssw' % i), 'lasp.slurm'))
        shutil.copy(os.path.join(home_path, 'lasp-single.in'),os.path.join(os.path.join(cluster5_path, '%d-single' % i), 'lasp.in'))
        shutil.copy(os.path.join(home_path, 'lasp-ssw.in'),os.path.join(os.path.join(cluster5_path, '%d-ssw' % i), 'lasp.in'))
        os.remove(os.path.join(cluster5_path, '%d.arc'%i))
        os.remove(os.path.join(cluster5_path, '%d.vasp'%i))        
            
            
            
            
            
            
if __name__ == '__main__':
    start_time = time.time()
    cutoff_range = 6
    global home_path
    home_path = os.getcwd()
    na_file = 'na_center'  # 可储钠的钠位点信息
    carbon_file = 'POSCAR-C'     # 硬碳骨架结构
    #cutoff_range=[i for i in range(3,11)]   # 截断半径半径的个数和大小，要修改的位置
    na_weidain = get_na_info(na_file)
    carbon_weidian, jingge_vector = get_carbon_info(carbon_file)
    path = os.path.join(home_path,str(cutoff_range))
    if not glob.glob('7_voltage_path'):
        os.mkdir('7_voltage_path')
    cluster1_index, cluster2_index, cluster3_index = cluster_info(path)
    print(cluster1_index, cluster2_index, cluster3_index)
    gene_path=os.path.join(home_path,'7_voltage_path')   
    #generate_vasp_file(gene_path,)
    cluster_num=len(cluster1_index)+len(cluster2_index)+len(cluster3_index)
    generate_vasp_file(gene_path,na_weidain,carbon_weidian, jingge_vector,cluster1_index,cluster2_index,cluster3_index)
    file_prepare(home_path,gene_path,cluster_num)
    
    
    
    
