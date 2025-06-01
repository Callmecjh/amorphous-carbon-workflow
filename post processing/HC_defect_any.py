# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import math
import time
from random import *
import os
import glob
import ase
import random
import itertools

initial_config_name = 'hard-carbon-100atom.vasp'  #初始结构文件名，笛卡尔坐标形式的poscar
r_length = 3                                      #neighbor_list考虑的截断半径范围
pos_dir = 'neighbor_pos_dir'                      #存储每个原子周围环境的poscar的目录名
coor_length = 1.9                                 #走圆环时1.9埃内的配位考虑，参考vesta
plane_dis = 1.5                                   #平面性判断的距离

def get_initial_config(filename):  #默认只有一种碳元素,碳元素在首位
    pos_info = open(filename, 'r')
    for i in range(2):  #poscar前面两行不要
        line = pos_info.readline()
    vec_x = []; vec_y = []; vec_z = []
    line = pos_info.readline().split()   #晶格矢量的三行
    vec_x.append(float(line[0])); vec_x.append(float(line[1])); vec_x.append(float(line[2]))
    line = pos_info.readline().split()
    vec_y.append(float(line[0])); vec_y.append(float(line[1])); vec_y.append(float(line[2]))
    line = pos_info.readline().split()
    vec_z.append(float(line[0])); vec_z.append(float(line[1])); vec_z.append(float(line[2]))
    jingge_vec = [vec_x, vec_y, vec_z]
    line = pos_info.readline()
    line = pos_info.readline()
    atom_num = int(line.split()[0])
    line = pos_info.readline()
    atom_coor_x = []; atom_coor_y = []; atom_coor_z = [];
    for i in range(atom_num):
        line = pos_info.readline()
        atom_coor_x.append(float(line.split()[0]))
        atom_coor_y.append(float(line.split()[1]))
        atom_coor_z.append(float(line.split()[2]))
    atom_coor = [atom_coor_x, atom_coor_y, atom_coor_z]
    pos_info.close()
    return jingge_vec, atom_num, atom_coor

def out_i_pos(atom_index, jingge_vec, atom_num, atom_coor, neighbor_list_sta):
    i_atom_info=open(os.path.join(pos_dir, '%d_atom_neigh_en.vasp'%atom_index), 'w')
    i_atom_info.write('pos \n')
    i_atom_info.write('1 \n')
    i_atom_info.write('   ' + str(jingge_vec[0][0]) + '   ' + str(jingge_vec[0][1]) + '   ' + str(jingge_vec[0][2]) + ' \n')
    i_atom_info.write('   ' + str(jingge_vec[1][0]) + '   ' + str(jingge_vec[1][1]) + '   ' + str(jingge_vec[1][2]) + ' \n')
    i_atom_info.write('   ' + str(jingge_vec[2][0]) + '   ' + str(jingge_vec[2][1]) + '   ' + str(jingge_vec[2][2]) + ' \n')
    i_atom_info.write('C \n')
    i_atom_info.write('%d \n' % (len(neighbor_list_sta[atom_index]) + 1))
    i_atom_info.write('Car \n')
    i_atom_info.write('   ' + str(atom_coor[0][atom_index]) + '   ' + str(atom_coor[1][atom_index]) + '   ' + str(atom_coor[2][atom_index]) + ' \n')
    for i in range(len(neighbor_list_sta[atom_index])):
        i_atom_info.write('   ' + str(atom_coor[0][neighbor_list_sta[atom_index][i][1]]) + '   ' + str(atom_coor[1][neighbor_list_sta[atom_index][i][1]]) + '   ' + str(atom_coor[2][neighbor_list_sta[atom_index][i][1]]) + ' \n')
    i_atom_info.close()

def neigh_list_cal(jingge_vec, atom_num, atom_coor): #每个原子周围6埃局域环境的原子序号和最近邻三个原子序号
    jingge_matrix = np.array(jingge_vec)
    Volume = np.linalg.det(jingge_matrix)
    neighbor_list_sta = []  #存储所有信息
    for i in range(atom_num):
        i_neigh_list = []
        for j in range(atom_num):
            if i != j:
                i_j_dis = []
                for m in [-1, 0, 1]:   #考虑周期性
                    for n in [-1, 0, 1]:
                        for l in [-1, 0, 1]:
                            shift_x = m * jingge_vec[0][0] + n * jingge_vec[1][0] + l * jingge_vec[2][0]
                            shift_y = m * jingge_vec[0][1] + n * jingge_vec[1][1] + l * jingge_vec[2][1]
                            shift_z = m * jingge_vec[0][2] + n * jingge_vec[1][2] + l * jingge_vec[2][2]
                            ij_distance = math.sqrt((atom_coor[0][i] - atom_coor[0][j] - shift_x) ** 2 + (atom_coor[1][i] - atom_coor[1][j] - shift_y) ** 2 + (atom_coor[2][i] - atom_coor[2][j] - shift_z) ** 2)
                            i_j_dis.append(ij_distance)
                if min(i_j_dis) < r_length:
                    i_neigh_list.append([min(i_j_dis),j])
                else:
                    pass
            else:
                continue
        i_neigh_list.sort()
        #print(i_neigh_list)
        neighbor_list_sta.append(i_neigh_list)
    #print(neighbor_list_sta)
    neigh_info = open('neighbor_list_info','w')
    for i in range(atom_num):
        neigh_info.write(str(i)+' ')
        for j in range(len(neighbor_list_sta[i])):
            neigh_info.write(str(neighbor_list_sta[i][j][0]) + ' ') #键长值
        for j in range(len(neighbor_list_sta[i])):
            neigh_info.write(str(neighbor_list_sta[i][j][1]) + ' ') #原子index值
        neigh_info.write('\n')
    neigh_info.close()
    for i in range(atom_num):
        atom_index = i
        out_i_pos(atom_index, jingge_vec, atom_num, atom_coor, neighbor_list_sta)

def delete_file(path):
    ls = os.listdir(path)  # os.listdir：返回指定的文件夹包含的文件或文件夹的名字的列表
    for i in ls:
        c_path = os.path.join(path, i)  # join：将路径和文件结合成一个路径
        if os.path.isdir(c_path):  # isdir：是否为一个目录
            delete_file(c_path)
        else:
            os.remove(c_path)

def carbon_ring(jingge_vec, atom_num, atom_coor): #开始圆环的判断
    neigh_info = open('neighbor_list_info','r')
    carbon_ring_info = open('carbon_ring_data','w')
    content = neigh_info.readlines()
    neigh_info_list = []
    for i in range(len(content)):  #收集每个原子最近邻index的所有信息,只取前三最近邻
        i_atom_info = []
        i_content = content[i].split()
        i_content_length = len(i_content)
        ##设置截断半径内1.9
        bond_index_end = int((i_content_length - 1)/2 + 1)   #这里由于我的文件格式是先写键长再写index
        half_length = int((i_content_length - 1)/2)
        i_atom_info.append(int(i_content[0]))
        for i in range(1,bond_index_end):
            if float(i_content[i]) < coor_length:
                i_atom_info.append(int(i_content[i+half_length]))
        neigh_info_list.append(i_atom_info)
    ###各原子数有几配位进行一个统计
    zero_num = 0; one_num = 0; two_num = 0; three_num = 0; four_num = 0; five_num = 0
    zero_coor_list = []; one_coor_list = []; two_coor_list = []; three_coor_list = []; four_coor_list = []; five_coor_list = []
    for i in neigh_info_list:
        i_coor_num = len(i) - 1
        if i_coor_num == 0:
            zero_num += 1
            zero_coor_list.append(i[0])
        elif i_coor_num == 1:
            one_num += 1
            one_coor_list.append(i[0])
        elif i_coor_num == 2:
            two_num += 1
            two_coor_list.append(i[0])
        elif i_coor_num == 3:
            three_num += 1
            three_coor_list.append(i[0])
        elif i_coor_num == 4:
            four_num += 1
            four_coor_list.append(i[0])
        elif i_coor_num == 5:
            five_num += 1
            five_coor_list.append(i[0])
    print('zero coor: %d, one coor: %d, two coor: %d, three coor: %d, four coor: %d, five coor: %d ' % (zero_num, one_num, two_num, three_num, four_num, five_num))  #截断半径内各个配位的原子数有多少
    carbon_ring_info.write('zero coor: %d, one coor: %d, two coor: %d, three coor: %d, four coor: %d, five coor: %d  \n' % (zero_num, one_num, two_num, three_num, four_num, five_num))
    carbon_ring_info.write('0配位原子： ' + str(zero_coor_list) +'\n')
    carbon_ring_info.write('1配位原子： ' + str(one_coor_list) + '\n')
    carbon_ring_info.write('2配位原子： ' + str(two_coor_list) + '\n')
    carbon_ring_info.write('3配位原子： ' + str(three_coor_list) + '\n')
    carbon_ring_info.write('4配位原子： ' + str(four_coor_list) + '\n')
    carbon_ring_info.write('5配位原子： ' + str(five_coor_list) + '\n')
    ring_list_total = []
    ###开始进行圆环的判断
    three_ring = []; four_ring = []; five_ring = []; six_ring = []; seven_ring = []; eight_ring = []; nine_ring = []; ten_ring = []; eleven_ring = []; twelve_ring = []  #存储所有圆环的信息
    for i in range(len(neigh_info_list)):  #最大判断到9个圆环为止
        atom_i_ring = []
        count = 0
        #while True:
        for j in neigh_info_list[i][1:]:
            count += 1
            for k in neigh_info_list[j][1:]:
                if k != i:  #防止邻近的第一个原子在回到中心原子处
                    count += 1
                    for l in neigh_info_list[k][1:]:
                        if l != j:
                            count += 1
                            if l == i:
                                three_ring.append([i,j,k])
                                atom_i_ring.append([i,j,k])  #三元环
                            for m in neigh_info_list[l][1:]:
                                if m != k and m != l and m != j:
                                    count += 1
                                    if m == i:
                                        four_ring.append([i, j, k, l])
                                        atom_i_ring.append([i, j, k, l])  #四元环
                                    for n in neigh_info_list[m][1:]:
                                        if n != l and n != m and n != j and n != k:
                                            count += 1
                                            if n == i:
                                                five_ring.append([i, j, k, l, m])
                                                atom_i_ring.append([i, j, k, l, m]) #五元环
                                            for q in neigh_info_list[n][1:]:
                                                if q != m and q != j and q != k and q != l and q != n:
                                                    count += 1
                                                    if q == i:
                                                        six_ring.append([i, j, k, l, m, n])
                                                        atom_i_ring.append([i, j, k, l, m, n])  #六元环
                                                    for o in neigh_info_list[q][1:]:
                                                        if o != n and o != j and o != k and o != l and o != m and o != q:
                                                            count += 1
                                                            if o == i:
                                                                seven_ring.append([i, j, k, l, m, n, q])
                                                                atom_i_ring.append([i, j, k, l, m, n, q])  #七元环
                                                            for p in neigh_info_list[o][1:]:
                                                                if p != q and p != j and p != k and p != l and p != m and p != n and p != o:
                                                                    count += 1
                                                                    if p == i:
                                                                        eight_ring.append([i, j, k, l, m, n, q, o])
                                                                        atom_i_ring.append([i, j, k, l, m, n, q, o])  #八元环
                                                                    for a in neigh_info_list[p][1:]:
                                                                        if a != o and a != q and a != j and a != k and a != l and a != m and a != n and a != p:
                                                                            count += 1
                                                                            if a == i:
                                                                                nine_ring.append([i, j, k, l, m, n, q, o, p])
                                                                                atom_i_ring.append([i, j, k, l, m, n, q, o, p])  #九元环
        ring_list_total.append(atom_i_ring)
    # 多次循环去除重复的,去除圆环三个最近邻的问题
    print('去除大圆环包含小圆环问题：')
    carbon_ring_info.write('\n去除大圆环包含小圆环问题： \n')
    for i in range(10):  # 列表remove的原因，先这样写
        three_ring = remove_similar(three_ring, neigh_info_list)
    print(len(three_ring),three_ring)
    for i in range(10):
        four_ring = remove_similar(four_ring, neigh_info_list)
    print(len(four_ring),four_ring)
    for i in range(10):
        five_ring = remove_similar(five_ring, neigh_info_list)
    print(len(five_ring),five_ring)
    for i in range(10):
        six_ring = remove_similar(six_ring, neigh_info_list)
    print(len(six_ring),six_ring)
    for i in range(10):
        seven_ring = remove_similar(seven_ring, neigh_info_list)
    print(len(seven_ring),seven_ring)
    for i in range(10):
        eight_ring = remove_similar(eight_ring, neigh_info_list)
    print(len(eight_ring),eight_ring)
    for i in range(10):
        nine_ring = remove_similar(nine_ring, neigh_info_list)
    print(len(nine_ring),nine_ring)
    ####输出信息到文件内
    ring_big_small = [three_ring, four_ring, five_ring, six_ring, seven_ring, eight_ring, nine_ring]
    for i in range(len(ring_big_small)):
        if len(ring_big_small[i]) == 0:
            carbon_ring_info.write('无%d圆环 \n' % (i+3))
        else:
            ring_length = len(ring_big_small[i][0])
            a = len(ring_big_small[i]) // 10; b = len(ring_big_small[i]) % 10
            carbon_ring_info.write('%d圆环: %d \n'%(ring_length, len(ring_big_small[i])))
            for j in range(a):
                for k in range(10):  #每一行10个输出
                    carbon_ring_info.write(str(ring_big_small[i][k+j*10])+'  ')
                carbon_ring_info.write('\n')
            for j in range(b):
                carbon_ring_info.write(str(ring_big_small[i][j + a * 10]) + '  ')
            carbon_ring_info.write('\n')

    # 去除跨周期性问题
    print('去除周期性的问题：')
    carbon_ring_info.write('\n去除周期性的问题： \n')
    #four_coor_ring = []#存在四配位的圆环的情况收集列表
    ###三元环
    three_ring_filter = filter_ring(three_ring, neigh_info_list)
    print(len(three_ring_filter), three_ring_filter)
    ###四元环
    four_ring_filter = filter_ring(four_ring, neigh_info_list)
    print(len(four_ring_filter), four_ring_filter)
    #print(period_judge([1, 2, 73, 96, 97],neigh_info_list))
    ###五元环
    five_ring_filter = filter_ring(five_ring, neigh_info_list)
    print(len(five_ring_filter), five_ring_filter)
    ###六元环
    #a = catch_exception_ring([47, 52, 67, 68, 74, 80], neigh_info_list)
    #print('a', a)
    six_ring_filter = filter_ring(six_ring, neigh_info_list)
    print(len(six_ring_filter), six_ring_filter)
    #print(four_coor_ring)
    ###七元环
    seven_ring_filter = filter_ring(seven_ring, neigh_info_list)
    print(len(seven_ring_filter), seven_ring_filter)
    ###八元环
    eight_ring_filter = filter_ring(eight_ring, neigh_info_list)
    print(len(eight_ring_filter), eight_ring_filter)
    ###九元环
    nine_ring_filter = filter_ring(nine_ring, neigh_info_list)
    print(len(nine_ring_filter), nine_ring_filter)
    ####输出信息到文件内
    ring_period = [three_ring_filter, four_ring_filter, five_ring_filter, six_ring_filter, seven_ring_filter, eight_ring_filter, nine_ring_filter]
    for i in range(len(ring_period)):
        if len(ring_period[i]) == 0:
            carbon_ring_info.write('无%d圆环 \n' % (i + 3))
        else:
            ring_length = len(ring_period[i][0])
            a = len(ring_period[i]) // 10;
            b = len(ring_period[i]) % 10
            carbon_ring_info.write('%d圆环: %d \n' % (ring_length, len(ring_period[i])))
            for j in range(a):
                for k in range(10):  # 每一行10个输出
                    carbon_ring_info.write(str(ring_period[i][k + j * 10]) + '  ')
                carbon_ring_info.write('\n')
            for j in range(b):
                carbon_ring_info.write(str(ring_period[i][j + a * 10]) + '  ')
            carbon_ring_info.write('\n')

    ###这里计算每个圆环的直径，取最大的两个原子间距
    carbon_ring_info.write('\n各圆环直径计算：\n')
    ring_period_diamter = []
    for i in ring_period:
        i_diamter = []
        for j in i:
            j_diamter = ring_diamter_cal(j, jingge_vec, atom_num, atom_coor)
            i_diamter.append(j_diamter)
        ring_period_diamter.append(i_diamter)

    for i in range(len(ring_period_diamter)):
        if len(ring_period_diamter[i]) == 0:
            carbon_ring_info.write('无%d圆环直径 \n' % (i + 3))
        else:
            #ring_length = len(ring_period_diamter[i][0])
            a = len(ring_period_diamter[i]) // 10;
            b = len(ring_period_diamter[i]) % 10
            carbon_ring_info.write('%d圆环直径: %d \n' % (i + 3, len(ring_period_diamter[i])))
            for j in range(a):
                for k in range(10):  # 每一行10个输出
                    carbon_ring_info.write(str(ring_period_diamter[i][k + j * 10]) + '  ')
                carbon_ring_info.write('\n')
            for j in range(b):
                carbon_ring_info.write(str(ring_period_diamter[i][j + a * 10]) + '  ')
            carbon_ring_info.write('\n')


    #平面性判断, 至少从四圆环开始
    print('圆环平面性评估问题：')
    carbon_ring_info.write('\n圆环平面性评估问题： \n')
    four_ring_plane = plane_judge(four_ring_filter, neigh_info_list)
    print(len(four_ring_plane), four_ring_plane)
    five_ring_plane = plane_judge(five_ring_filter, neigh_info_list)
    print(len(five_ring_plane), five_ring_plane)
    six_ring_plane = plane_judge(six_ring_filter, neigh_info_list)
    print(len(six_ring_plane), six_ring_plane)
    seven_ring_plane = plane_judge(seven_ring_filter, neigh_info_list)
    print(len(seven_ring_plane), seven_ring_plane)
    eight_ring_plane = plane_judge(eight_ring_filter, neigh_info_list)
    print(len(eight_ring_plane), eight_ring_plane)
    nine_ring_plane = plane_judge(nine_ring_filter, neigh_info_list)
    print(len(nine_ring_plane), nine_ring_plane)
    #a=plane_judge([[0, 2, 6, 7, 73, 78]], neigh_info_list)
    ring_plane = [four_ring_plane, five_ring_plane, six_ring_plane, seven_ring_plane,eight_ring_plane, nine_ring_plane]
    for i in range(len(ring_plane)):
        if len(ring_plane[i]) == 0:
            carbon_ring_info.write('无%d圆环 \n' % (i + 4))
        else:
            ring_length = len(ring_plane[i][0])
            a = len(ring_plane[i]) // 10;
            b = len(ring_plane[i]) % 10
            carbon_ring_info.write('%d圆环: %d \n' % (ring_length, len(ring_plane[i])))
            for j in range(a):
                for k in range(10):  # 每一行10个输出
                    carbon_ring_info.write(str(ring_plane[i][k + j * 10]) + '  ')
                carbon_ring_info.write('\n')
            for j in range(b):
                carbon_ring_info.write(str(ring_plane[i][j + a * 10]) + '  ')
            carbon_ring_info.write('\n')
    carbon_ring_info.write('\n边缘性缺陷判断： \n')
    edge_site_zigzag, edge_site_armchair = edge_site(neigh_info_list)
    carbon_ring_info.write('zigzag ： %d \n' % len(edge_site_zigzag))
    if len(edge_site_zigzag) == 0:
        carbon_ring_info.write('无 zigzag 类型 \n')
    else:
        a = len(edge_site_zigzag) // 10;
        b = len(edge_site_zigzag) % 10
        for j in range(a):
            for k in range(10):  # 每一行10个输出
                carbon_ring_info.write(str(edge_site_zigzag[k + j * 10]) + '  ')
            carbon_ring_info.write('\n')
        for j in range(b):
            carbon_ring_info.write(str(edge_site_zigzag[j + a * 10]) + '  ')
        carbon_ring_info.write('\n')
    carbon_ring_info.write('armchair ： %d \n' % len(edge_site_armchair))
    if len(edge_site_armchair) == 0:
        carbon_ring_info.write('无 armchair 类型 \n')
    else:
        a = len(edge_site_armchair) // 10;
        b = len(edge_site_armchair) % 10
        for j in range(a):
            for k in range(10):  # 每一行10个输出
                carbon_ring_info.write(str(edge_site_armchair[k + j * 10]) + '  ')
            carbon_ring_info.write('\n')
        for j in range(b):
            carbon_ring_info.write(str(edge_site_armchair[j + a * 10]) + '  ')
        carbon_ring_info.write('\n')
    carbon_ring_info.close()

def ring_diamter_cal(ring, jingge_vec, atom_num, atom_coor):   #计算圆环直径,从文件内读取
    zuhe_combination = list(itertools.combinations(ring,2))
    dis_jihe = []
    for i in zuhe_combination:
        i_j_dis = []
        i_index = i[0]; j_index = i[1]
        for m in [-1, 0, 1]:   #考虑周期性
            for n in [-1, 0, 1]:
                for l in [-1, 0, 1]:
                    shift_x = m * jingge_vec[0][0] + n * jingge_vec[1][0] + l * jingge_vec[2][0]
                    shift_y = m * jingge_vec[0][1] + n * jingge_vec[1][1] + l * jingge_vec[2][1]
                    shift_z = m * jingge_vec[0][2] + n * jingge_vec[1][2] + l * jingge_vec[2][2]
                    ij_distance = math.sqrt((atom_coor[0][i_index] - atom_coor[0][j_index] - shift_x) ** 2 + (atom_coor[1][i_index] - atom_coor[1][j_index] - shift_y) ** 2 + (atom_coor[2][i_index] - atom_coor[2][j_index] - shift_z) ** 2)
                    i_j_dis.append(ij_distance)
        dis_jihe.append(min(i_j_dis))
    ring_diamter = max(dis_jihe)
    return ring_diamter

def edge_site(neigh_info_list):  #边缘性缺陷的判断, 22332233,33223322,23232323,32323232 四种配位变化的形式,以八个原子为单位
    for i in neigh_info_list:
        coor_num = len(i)-1
        i.append(coor_num)
    zig_zag = [[2,3,2,3],[3,2,3,2]]; armchair = [[2,2,3,3,],[3,3,2,2]]   #边缘区域的标准形式
    edge_site_zigzag = []; edge_site_armchair = []
    for i in neigh_info_list:
        i_edge = []
        for j in neigh_info_list[i[0]][1:-1]:
            for k in neigh_info_list[j][1:-1]:
                for l in neigh_info_list[k][1:-1]:
                    if len(set([i[0], j, k, l])) == 4:
                        i_edge.append(neigh_info_list[i[0]][-1])
                        i_edge.append(neigh_info_list[j][-1])
                        i_edge.append(neigh_info_list[k][-1])
                        i_edge.append(neigh_info_list[l][-1])
                        if i_edge in zig_zag:
                            edge_site_zigzag.append([i[0],j,k,l])
                        elif i_edge in armchair:
                            edge_site_armchair.append([i[0],j,k,l])
                        else:
                            pass
    return edge_site_zigzag, edge_site_armchair

def plane_judge(rings, neigh_info_list):  #同样要考虑周期性问题
    jingge_vec, atom_num, atom_coor = get_initial_config(initial_config_name)
    for i in range(10):
        for j in rings:
            numstr, period_index = period_judge(j, neigh_info_list)
            period_index.sort()
            #print(period_index)
            for k in range(10):  #随机取三个点，取十次
                plane_point = random.sample(j,4)  #随机取三个点确定平面
                a=plane_point[0];b=plane_point[1];c=plane_point[2];d=plane_point[3]
                a_mnl = period_index[j.index(a)][1:];b_mnl = period_index[j.index(b)][1:];c_mnl = period_index[j.index(c)][1:];d_mnl = period_index[j.index(d)][1:]
                shift_x_a = a_mnl[0] * jingge_vec[0][0] + a_mnl[1] * jingge_vec[1][0] + a_mnl[2] * jingge_vec[2][0]; shift_y_a = a_mnl[0] * jingge_vec[0][1] + a_mnl[1] * jingge_vec[1][1] + a_mnl[2] * jingge_vec[2][1]; shift_z_a = a_mnl[0] * jingge_vec[0][2] + a_mnl[1] * jingge_vec[1][2] + a_mnl[2] * jingge_vec[2][2]
                shift_x_b = b_mnl[0] * jingge_vec[0][0] + b_mnl[1] * jingge_vec[1][0] + b_mnl[2] * jingge_vec[2][0];shift_y_b = b_mnl[0] * jingge_vec[0][1] + b_mnl[1] * jingge_vec[1][1] + b_mnl[2] * jingge_vec[2][1];shift_z_b = b_mnl[0] * jingge_vec[0][2] + b_mnl[1] * jingge_vec[1][2] + b_mnl[2] * jingge_vec[2][2]
                shift_x_c = c_mnl[0] * jingge_vec[0][0] + c_mnl[1] * jingge_vec[1][0] + c_mnl[2] * jingge_vec[2][0];shift_y_c = c_mnl[0] * jingge_vec[0][1] + c_mnl[1] * jingge_vec[1][1] + c_mnl[2] * jingge_vec[2][1];shift_z_c = c_mnl[0] * jingge_vec[0][2] + c_mnl[1] * jingge_vec[1][2] + c_mnl[2] * jingge_vec[2][2]
                shift_x_d = d_mnl[0] * jingge_vec[0][0] + d_mnl[1] * jingge_vec[1][0] + d_mnl[2] * jingge_vec[2][0];shift_y_d = d_mnl[0] * jingge_vec[0][1] + d_mnl[1] * jingge_vec[1][1] + d_mnl[2] * jingge_vec[2][1];shift_z_d = d_mnl[0] * jingge_vec[0][2] + d_mnl[1] * jingge_vec[1][2] + d_mnl[2] * jingge_vec[2][2]
                point1 = [atom_coor[0][plane_point[0]]+shift_x_a, atom_coor[1][plane_point[0]]+shift_y_a, atom_coor[2][plane_point[0]]+shift_z_a]
                point2 = [atom_coor[0][plane_point[1]]+shift_x_b, atom_coor[1][plane_point[1]]+shift_y_b, atom_coor[2][plane_point[1]]+shift_z_b]
                point3 = [atom_coor[0][plane_point[2]]+shift_x_c, atom_coor[1][plane_point[2]]+shift_y_c, atom_coor[2][plane_point[2]]+shift_z_c]
                point4 = [atom_coor[0][plane_point[3]]+shift_x_d, atom_coor[1][plane_point[3]]+shift_y_d, atom_coor[2][plane_point[3]]+shift_z_d]
                cal_d = point2area_distance(point1, point2, point3, point4)
                if cal_d > plane_dis:
                    #print(plane_point)
                    #print(point1, point2, point3, point4)
                    #print(cal_d)
                    rings.remove(j)
                    break
                else:
                    pass
    return rings

def define_area(point1, point2, point3):  #三点确定一个平面，得到平面的方程
    point1 = np.asarray(point1)
    point2 = np.asarray(point2)
    point3 = np.asarray(point3)
    AB = np.asmatrix(point2 - point1)
    AC = np.asmatrix(point3 - point1)
    N = np.cross(AB, AC)      #向量叉乘，求法向量
    # Ax+By+Cz
    Ax = N[0, 0]
    By = N[0, 1]
    Cz = N[0, 2]
    D = -(Ax * point1[0] + By * point1[1] + Cz * point1[2])
    return Ax, By, Cz, D #返回平面方程

def point2area_distance(point1, point2, point3, point4):  #1，2，3为平面的点
    Ax, By, Cz, D = define_area(point1, point2, point3)
    #print(Ax, By, Cz, D)
    mod_d = Ax * point4[0] + By * point4[1] + Cz * point4[2] + D
    mod_area = np.sqrt(np.sum(np.square([Ax, By, Cz])))
    d = abs(mod_d) / mod_area
    return d  #返回距离

def filter_ring(rings, neigh_info_list):
    #coor_ring = []
    for k in range(10):    # 列表remove的原因，先这样写
        for i in rings:
            return_str = catch_exception_ring(i, neigh_info_list)
            if return_str == 1:
                pass
            elif return_str == 2:
                rings.remove(i)
            elif return_str == 3:
                rings.remove(i)
                #coor_ring.append(i)
    return rings

def catch_exception_ring(single_ring, neigh_info_list):   #捕获出现异常的元环，有的四配位的情况
    try:
        judge_num, period_index = period_judge(single_ring, neigh_info_list)
        if judge_num == 1:
            return 1
        elif judge_num == 2:
            return 2
        else:
            pass
    except TypeError as e:
        #print(e)
        return 3

def remove_similar(ring_set, neigh_info_list):
    ring_set_new = []
    for i in ring_set:  #去除重复的圆环
        i.sort()
        if i not in ring_set_new:
            ring_set_new.append(i)
    for i in ring_set_new:     #去除三个最近邻都在的圆环
        for j in i:
            j_count = 0
            for k in neigh_info_list[j]:
                if k in i:
                    j_count += 1
                else:
                    pass
            if j_count > 3:  #超过三就都属于大环含小环的情况
                ring_set_new.remove(i)
                break
            else:
                pass
            #a = neigh_info_list[j][0]
            #b = neigh_info_list[j][1]
            #c = neigh_info_list[j][2]
            #d = neigh_info_list[j][3]
            #if (a in i) and (b in i) and (c in i) and (d in i):
                #ring_set_new.remove(i)
                #break  #防止重复删除引起的报错
            #else:
                #pass
    return ring_set_new

def next_index_judge(index1, index2, ring_list, neigh_info_list):
    next_index_list = neigh_info_list[index2][1:]
    #print(next_index_list)
    for i in next_index_list:
        if i in ring_list:
            if i != index1:
                next_index = i
                return next_index

def period_judge(ring_list, neigh_info_list):  #跨周期的判断, 大胞不太能遇到这个问题
    ring_num = len(ring_list)    #此为几圆环
    start_point = ring_list[0]   #先确定链条的顺序,首先任意确定连续的两个
    for i in neigh_info_list[start_point][1:]:
        if i in ring_list:
            second_point = i
            break
    shunxu_ring = [start_point,second_point]
    while True:
        index1, index2 = shunxu_ring[-2:]
        next_index = next_index_judge(index1, index2, ring_list, neigh_info_list)
        shunxu_ring.append(next_index)
        if len(shunxu_ring) == ring_num:
            break
        else:
            continue
    #print(shunxu_ring)
    #再确定每一个原子的周期
    jingge_vec, atom_num, atom_coor = get_initial_config(initial_config_name)
    period_index=[[shunxu_ring[0],0,0,0]]
    for i in range(len(shunxu_ring)):
        if i == len(shunxu_ring) - 1:
            i_i1_dis = []
            shift_x_ahead = period_index[-1][1] * jingge_vec[0][0] + period_index[-1][2] * jingge_vec[1][0] + period_index[-1][3] * jingge_vec[2][0]
            shift_y_ahead = period_index[-1][1] * jingge_vec[0][1] + period_index[-1][2] * jingge_vec[1][1] + period_index[-1][3] * jingge_vec[2][1]
            shift_z_ahead = period_index[-1][1] * jingge_vec[0][2] + period_index[-1][2] * jingge_vec[1][2] + period_index[-1][3] * jingge_vec[2][2]
            for m in [-1, 0, 1]:  # 考虑周期性
                for n in [-1, 0, 1]:
                    for l in [-1, 0, 1]:
                        shift_x = m * jingge_vec[0][0] + n * jingge_vec[1][0] + l * jingge_vec[2][0]  #近邻原子的周期性
                        shift_y = m * jingge_vec[0][1] + n * jingge_vec[1][1] + l * jingge_vec[2][1]
                        shift_z = m * jingge_vec[0][2] + n * jingge_vec[1][2] + l * jingge_vec[2][2]
                        ij_distance = math.sqrt((atom_coor[0][shunxu_ring[i]] + shift_x_ahead - atom_coor[0][shunxu_ring[0]] - shift_x) ** 2 + (atom_coor[1][shunxu_ring[i]] + shift_y_ahead - atom_coor[1][shunxu_ring[0]] - shift_y) ** 2 + (atom_coor[2][shunxu_ring[i]] + shift_z_ahead - (atom_coor[2][shunxu_ring[0]]) - shift_z) ** 2)
                        i_i1_dis.append([ij_distance, shunxu_ring[0], m, n, l])
            i_i1_dis.sort()
            i_i1_dis[0].pop(0)
        else:
            i_i1_dis = []
            shift_x_ahead = period_index[-1][1] * jingge_vec[0][0] + period_index[-1][2] * jingge_vec[1][0] + period_index[-1][3] * jingge_vec[2][0]  #中心原子自身具有周期性
            shift_y_ahead = period_index[-1][1] * jingge_vec[0][1] + period_index[-1][2] * jingge_vec[1][1] + period_index[-1][3] * jingge_vec[2][1]
            shift_z_ahead = period_index[-1][1] * jingge_vec[0][2] + period_index[-1][2] * jingge_vec[1][2] + period_index[-1][3] * jingge_vec[2][2]
            for m in [-1, 0, 1]:   #考虑周期性
                for n in [-1, 0, 1]:
                    for l in [-1, 0, 1]:
                        shift_x = m * jingge_vec[0][0] + n * jingge_vec[1][0] + l * jingge_vec[2][0] #近邻原子的周期性
                        shift_y = m * jingge_vec[0][1] + n * jingge_vec[1][1] + l * jingge_vec[2][1]
                        shift_z = m * jingge_vec[0][2] + n * jingge_vec[1][2] + l * jingge_vec[2][2]
                        ij_distance = math.sqrt((atom_coor[0][shunxu_ring[i]] + shift_x_ahead - atom_coor[0][shunxu_ring[i+1]] - shift_x) ** 2 + (atom_coor[1][shunxu_ring[i]] + shift_y_ahead - atom_coor[1][shunxu_ring[i+1]] - shift_y) ** 2 + (atom_coor[2][shunxu_ring[i]] + shift_z_ahead - atom_coor[2][shunxu_ring[i+1]] - shift_z) ** 2)
                        i_i1_dis.append([ij_distance,shunxu_ring[i+1],m,n,l])
            i_i1_dis.sort()
            i_i1_dis[0].pop(0)
        period_index.append(i_i1_dis[0])
    #print(period_index)
    period_fix_index = period_index[:-1]
    if period_index[0] == period_index[-1]:
        return 1, period_fix_index
    else:
        return 2, period_fix_index

if __name__ == '__main__':
    start_time = time.time()
    homepath = os.getcwd()
    if not glob.glob('%s/%s' % (homepath, pos_dir)):
        os.mkdir('%s/%s' % (homepath, pos_dir))
    delete_file(os.path.join(homepath, pos_dir))
    jingge_vec, atom_num, atom_coor = get_initial_config(initial_config_name)
    neigh_list_cal(jingge_vec, atom_num, atom_coor)
    carbon_ring(jingge_vec, atom_num, atom_coor)
    end_time = time.time()
    print('total time cost:', end_time - start_time)




