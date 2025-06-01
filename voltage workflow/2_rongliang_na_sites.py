# -*- coding: utf-8 -*-
import numpy as np
import math
import time
from multiprocessing import Pool
from tqdm import tqdm
from numba import jit
import copy
import os
import multiprocessing as mp

def get_initial_config(filename):  # 默认只有一种碳元素,碳元素在首位
    pos_info = open(filename, 'r')
    for i in range(2):  # poscar前面两行不要
        line = pos_info.readline()
    vec_x = [];
    vec_y = [];
    vec_z = []
    line = pos_info.readline().split()  # 晶格矢量的三行
    vec_x.append(float(line[0]));
    vec_x.append(float(line[1]));
    vec_x.append(float(line[2]))
    line = pos_info.readline().split()
    vec_y.append(float(line[0]));
    vec_y.append(float(line[1]));
    vec_y.append(float(line[2]))
    line = pos_info.readline().split()
    vec_z.append(float(line[0]));
    vec_z.append(float(line[1]));
    vec_z.append(float(line[2]))
    jingge_vec = [vec_x, vec_y, vec_z]
    line = pos_info.readline()
    line = pos_info.readline()
    atom_num = int(line.split()[0])
    line = pos_info.readline()
    atom_coor_x = [];
    atom_coor_y = [];
    atom_coor_z = [];
    for i in range(atom_num):
        line = pos_info.readline()
        atom_coor_x.append(float(line.split()[0]))
        atom_coor_y.append(float(line.split()[1]))
        atom_coor_z.append(float(line.split()[2]))
    atom_coor = [atom_coor_x, atom_coor_y, atom_coor_z]
    pos_info.close()
    return jingge_vec, atom_num, atom_coor
    
def get_max_na(content,jingge_vec):
    a_len=math.sqrt(jingge_vec[0][0]**2+jingge_vec[0][1]**2+jingge_vec[0][2]**2)
    b_len=math.sqrt(jingge_vec[1][0]**2+jingge_vec[1][1]**2+jingge_vec[1][2]**2)
    c_len=math.sqrt(jingge_vec[2][0]**2+jingge_vec[2][1]**2+jingge_vec[2][2]**2)
    # lattice = content
    lattice = []
    for i in content:
        f_content = i.split(',')
        diamer = int(float(f_content[-1].split(']')[0])*10)/10
        vec_a = int(float(f_content[0].split('[')[1])*10)/10
        vec_b = int(float(f_content[1])*10)/10
        vec_c = int(float(f_content[2])*10)/10   
        lattice.append([vec_a,vec_b,vec_c])
    na_number = []
    na_center = []
    for i in lattice:
        if len(na_center)==0:
            na_center.append(i)
        else:
            tag = False
            for center in na_center:
                distance_list=[]
                for m in [-1, 0, 1]:
                    for n in [-1, 0, 1]:
                        for o in [-1, 0, 1]:
                            shift_x = m * a_len + n * 0.0 + o * 0.0
                            shift_y = m * 0.0 + n * b_len + o * 0.0
                            shift_z = m * 0.0 + n * 0.0 + o * c_len
                            distance = math.sqrt((center[0] - i[0] - shift_x) ** 2 + (center[1] - i[1] - shift_y) ** 2 + (center[2] - i[2] - shift_z) ** 2)
                            distance_list.append(distance)
                if min(distance_list) < 3.0:
                    tag = False
                    break
                else:
                    tag = True
            if tag:
                na_center.append(i)
            na_number.append(len(na_center))
    na_center_file = open('na_center','w')
    for i in na_center:
        vec_a_1 = i[0]
        vec_b_1 = i[1]
        vec_c_1 = i[2]
        na_center_file.write(str(vec_a_1) + '  ' + str(vec_b_1) + '  ' + str(vec_c_1) + '\n')
    na_center_file.close()
    return na_number  

filename='POSCAR-C'
pore_info = open('pore_center_info', 'r')
content = pore_info.readlines()
jingge_vec, atom_num, atom_coor=get_initial_config(filename)

st_time = time.time()
a = get_max_na(content,jingge_vec)  
e_time = time.time()
print("total time ", e_time - st_time)
a = a.pop()
print(a)
file=open('na_number','w')
file.write(str(a)+'\n')
file.close()
