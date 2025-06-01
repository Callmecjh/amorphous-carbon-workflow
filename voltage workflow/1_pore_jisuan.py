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

# 获取格子大小，原子个数，原子坐标
# return :jingge_vec 格子大小, atom_num 原子个数, atom_coor原子坐标列表
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


# 空间划分，获取位于孔洞内的格子
# 局部变量： mesh_length 格子间隔
#           semi_diamer = 2.5 最近原子距离
# return ：possible_pore_center 最近原子的距离小于要求的格子坐标列表
@jit(nopython=True)
def pore_find(param_list):
    (jingge_vec, atom_num, atom_coor, i_mesh_region) = param_list
    mesh_length = 0.2
    semi_diamer = 2.5
    jingge_a = math.sqrt(jingge_vec[0][0] ** 2 + jingge_vec[0][1] ** 2 + jingge_vec[0][2] ** 2)
    jingge_b = math.sqrt(jingge_vec[1][0] ** 2 + jingge_vec[1][1] ** 2 + jingge_vec[1][2] ** 2)
    jingge_c = math.sqrt(jingge_vec[2][0] ** 2 + jingge_vec[2][1] ** 2 + jingge_vec[2][2] ** 2)
    possible_pore_center = []
    mesh_a = int(jingge_a // mesh_length + 1)
    mesh_b = int(jingge_b // mesh_length + 1)
    mesh_c = int(jingge_c // mesh_length + 1)
    for i in i_mesh_region:  # 间隔0.2取点
        for j in np.linspace(0.0, jingge_b, mesh_b):
            for k in np.linspace(0.0, jingge_c, mesh_c):
                ijk_all_dis = []
                for l in range(atom_num):
                    ijk_l_dis = []
                    for m in [-1, 0, 1]:
                        for n in [-1, 0, 1]:
                            for o in [-1, 0, 1]:
                                shift_x = m * jingge_vec[0][0] + n * jingge_vec[1][0] + o * jingge_vec[2][0]
                                shift_y = m * jingge_vec[0][1] + n * jingge_vec[1][1] + o * jingge_vec[2][1]
                                shift_z = m * jingge_vec[0][2] + n * jingge_vec[1][2] + o * jingge_vec[2][2]
                                ij_distance = math.sqrt(
                                    (i - atom_coor[0][l] - shift_x) ** 2 + (j - atom_coor[1][l] - shift_y) ** 2 + (
                                                k - atom_coor[2][l] - shift_z) ** 2)
                                ijk_l_dis.append(ij_distance)
                    ijk_all_dis.append(min(ijk_l_dis))
                if min(ijk_all_dis) < semi_diamer:
                    pass
                else:
                    possible_pore_center.append([i, j, k, min(ijk_all_dis)])
    return possible_pore_center


# 多进程划分
# 局部变量
def m_process(param):
    (mesh_length, cores, jingge_vec, atom_num, atom_coor) = param
    jingge_a = math.sqrt(jingge_vec[0][0] ** 2 + jingge_vec[0][1] ** 2 + jingge_vec[0][2] ** 2)
    jingge_b = math.sqrt(jingge_vec[1][0] ** 2 + jingge_vec[1][1] ** 2 + jingge_vec[1][2] ** 2)
    jingge_c = math.sqrt(jingge_vec[2][0] ** 2 + jingge_vec[2][1] ** 2 + jingge_vec[2][2] ** 2)
    mesh_a = int(jingge_a // mesh_length + 1)
    num_cores = cores
    # 划分格子进行多进程计算
    parallel_list = np.linspace(0.0, jingge_a, mesh_a).tolist()
    #print(type(parallel_list), parallel_list)
    # 任务列
    if mesh_a % num_cores == 0:  # 余数为0，可整除
        single_lenth = mesh_a // (num_cores)  # 单个列表的长度
        mesh_a_region = []
        for i in range(num_cores):
            mesh_a_region.append(parallel_list[i * single_lenth:(i + 1) * single_lenth])
    else:
        single_length = mesh_a // (num_cores)
        reside_length = mesh_a % (num_cores)
        # left_reside = mesh_a - (num_cores*single_length);
        # right_reside = (single_length+1)*num_cores - mesh_a
        if single_length > reside_length:
            mesh_a_region = []
            for i in range(num_cores):
                if i == num_cores - 1:
                    mesh_a_region.append(parallel_list[i * single_length:])
                else:
                    mesh_a_region.append(parallel_list[i * single_length:(i + 1) * single_length])
        else:
            mesh_a_region = []
            single_length = single_length + 1
            core = math.ceil(mesh_a / single_length)
            for i in range(core):
                if i == core - 1:
                    mesh_a_region.append(parallel_list[i * single_length:])
                else:
                    mesh_a_region.append(parallel_list[i * single_length:(i + 1) * single_length])
    paralist = []
    for i in mesh_a_region:
        paralist.append(i)

    # 多进程池
    param_list = [(jingge_vec, atom_num, atom_coor, i_mesh_region) for i_mesh_region in paralist]
    st_time = time.time()
    with Pool(num_cores) as p:
        r = list(p.imap(pore_find, param_list))
    p.close()
    p.join()
    e_time = time.time()
    #print("循环时间", e_time - st_time)
    #
    pore_center = open('pore_center_info', 'w')
    for i in r:
        for j in i:
            pore_center.write(str(j) + '\n')
    pore_center.close()
    pore_info = open('pore_center_info', 'r')
    content = pore_info.readlines()
    return content

## 格点扩展成7领域
def get_pore_number(content):
    pore_center_list = []
    six_list = []
    for i in content:
        f_content = i.split(',')
        diamer = int(float(f_content[-1].split(']')[0]) * 10) / 10
        vec_a = int(float(f_content[0].split('[')[1]) * 10) / 10
        vec_b = int(float(f_content[1]) * 10) / 10
        vec_c = int(float(f_content[2]) * 10) / 10
        a1 = round(vec_a + 0.2, 1)
        a2 = round(vec_a - 0.2, 1)
        b1 = round(vec_b + 0.2, 1)
        b2 = round(vec_b - 0.2, 1)
        c1 = round(vec_c + 0.2, 1)
        c2 = round(vec_c - 0.2, 1)
        six0 = str(vec_a) + '_' + str(vec_b) + '_' + str(vec_c)
        six1 = str(a1) + '_' + str(vec_b) + '_' + str(vec_c)
        six2 = str(a2) + '_' + str(vec_b) + '_' + str(vec_c)
        six3 = str(vec_a) + '_' + str(b1) + '_' + str(vec_c)
        six4 = str(vec_a) + '_' + str(b2) + '_' + str(vec_c)
        six5 = str(vec_a) + '_' + str(vec_b) + '_' + str(c1)
        six6 = str(vec_a) + '_' + str(vec_b) + '_' + str(c2)
        six_list.append([six0, six1, six2, six3, six4, six5, six6, diamer])
        pore_center_list.append([diamer, six0])
    with open('testaf.txt', 'w') as ww:
        ww.writelines(str(pore_center_list))
    with open('testsix.txt', 'w') as ww:
        ww.writelines(str(six_list))
    return six_list


## 递归搜寻邻域
save_nmb = mp.Manager().list()
# save_nmb = []
save_nmb2 = []


def smr(li):
    smt_li = li
    sol = smt_li[0]
    del smt_li[0]
    next_li = copy.deepcopy(smt_li)
    del_i = 0
    for index, value in enumerate(smt_li):
        last = 0
        sol_last = sol.pop()
        v_last = value.pop()
        if set(sol) & set(value):
            if v_last > sol_last:
                last = v_last
            else:
                last = sol_last
            sol = list(set(sol) | set(value))
            del next_li[del_i]
            del_i = del_i
        else:
            del_i = del_i + 1
            last = sol_last
        sol.append(last)
    save_nmb.append(sol)
    if next_li:
        smr(next_li)


def smr2(li):
    smt_li2 = li
    sol2 = smt_li2[0]
    del smt_li2[0]
    next_li2 = copy.deepcopy(smt_li2)
    del_i2 = 0
    for index, value in enumerate(smt_li2):
        last = 0
        sol_last = sol2.pop()
        v_last = value.pop()
        if set(sol2) & set(value):
            if v_last > sol_last:
                last = v_last
            else:
                last = sol_last
            sol2 = list(set(sol2) | set(value))
            del next_li2[del_i2]
            del_i2 = del_i2
        else:
            del_i2 = del_i2 + 1
            last = sol_last
        sol2.append(last)
    save_nmb2.append(sol2)
    if next_li2:
        smr2(next_li2)


if __name__ == '__main__':
    ## 修改 initial_config_name为poscar文件路径，结果输出在0NA_result.txt文件中
    ## 初始文件和参数
    start_time = time.time()
    initial_config_name = 'POSCAR-C'
    mesh_length = 0.2
    cores = 40

    jingge_vec, atom_num, atom_coor = get_initial_config(initial_config_name)
    param = [mesh_length, cores, jingge_vec, atom_num, atom_coor]
    content = m_process(param)

    ## 计算面积
    pore_center_list = []
    surface = 0
    for i in content:
        f_content = i.split(',')
        diamer = float(f_content[-1].split(']')[0])
        if diamer < 1.1:
            surface = surface + 1
    #print(surface)
    face = surface * 0.2 * 0.2
    print("total_surface：", face)
    surface_file = open('surface.txt', 'w')
    surface_file.write("total_surface：%f \n"%face)
    surface_file.close()

    pore_info = open('pore_center_info', 'r')
    content = pore_info.readlines()
    ## 计算孔隙
    six_list = get_pore_number(content)
    a = six_list
    l = len(a) // 39
    b = [a[i:i + l] for i in range(0, len(a), l)]
    #print(len(b))
    st_time = time.time()
    p = Pool(40)
    for i in range(40):
        p.apply_async(smr, (b[i],))
    p.close()
    p.join()
    #print(len(save_nmb))
    smr2(save_nmb)
    en_time = time.time()
    #print("循环时间", en_time - st_time)
    #print(len(save_nmb2))
    a = copy.deepcopy(save_nmb2)
    test = open('0NA.txt', 'w')
    for i in save_nmb2:
        test.write(str(i) + '\n')
    result = open('volume_diameter.txt', 'w')
    for i in save_nmb2:
        if len(i) > 15:
            v = round(len(i) * 0.2 * 0.2 * 0.2, 5)
            r = i.pop()
            #print('体积：%s，半径：%s' % (v, r))
            result.write('体积 %s 半径 %s' % (v, r) + '\n')
    result.close()
    end_time = time.time()
    print("total time cost: %f"%(end_time-start_time))