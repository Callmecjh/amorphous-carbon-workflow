#统计一个碳材料体系，统计体系内所有碳原子的杂化类型，属于sp2还是sp3，最后给出该结构中的sp2成分

from ase import build
from ase.io import read,write
import numpy as np
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.core.structure import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.core.structure import Structure
import sys
import time

def define_area(point1, point2, point3):  #三点确定一个平面，得到平面的方程
    point1 = np.asarray(point1)
    point2 = np.asarray(point2)
    point3 = np.asarray(point3)
    AB = np.asmatrix(point2 - point1)
    AC = np.asmatrix(point3 - point1)
    N = np.cross(AB, AC) #向量叉乘，求法向量
    # Ax+By+Cz
    Ax = N[0, 0]
    By = N[0, 1]
    Cz = N[0, 2]
    D = -(Ax * point1[0] + By * point1[1] + Cz * point1[2])
    return Ax, By, Cz, D #返回平面方程

def point2area_distance(point1, point2, point3, point4):
    Ax, By, Cz, D = define_area(point1, point2, point3)
    #print(Ax, By, Cz, D)
    mod_d = Ax * point4[0] + By * point4[1] + Cz * point4[2] + D
    mod_area = np.sqrt(np.sum(np.square([Ax, By, Cz])))
    d = abs(mod_d) / mod_area
    return d  #返回距离

if __name__ == '__main__':           
    start_time=time.time()
    pos_name='1.34-density.vasp'
    primi_cell=read(pos_name)
    pymatgen_stru = AseAtomsAdaptor().get_structure(primi_cell)
    frac_coor = pymatgen_stru.frac_coords.tolist() #所有原子分数坐标
    atom_number=len(frac_coor)
    #print('Total number of atoms in the system:',atom_number)
    #cutoff_range=list(np.arange(0.5,3.2,0.1))
    cutoff_limit=1.9  #配位数键长极限
    #print('Truncation radius range value:',cutoff_limit)
    isolate_atom_index=[]
    one_coor_atom_index=[];one_coor_atom_match_index=[]
    two_coor_atom_index=[];two_coor_atom_match_index=[]
    three_coor_atom_index=[];three_coor_atom_match_index=[]
    four_coor_atom_index=[];four_coor_atom_match_index=[]
    five_coor_atom_index=[];five_coor_atom_match_index=[]
    for j in range(atom_number):
        j_atom_coor_num=0
        j_atom_coor_num_match_index=[]
        for k in range(atom_number):
            if k != j:
                jk_distance=pymatgen_stru.get_distance(j,k)
                if jk_distance < cutoff_limit:
                    j_atom_coor_num += 1
                    j_atom_coor_num_match_index.append(k)
            else:
                continue
        if j_atom_coor_num == 0:
            isolate_atom_index.append(j)
        elif j_atom_coor_num == 1:
            one_coor_atom_index.append(j)
            one_coor_atom_match_index.append(j_atom_coor_num_match_index)
        elif j_atom_coor_num == 2:
            two_coor_atom_index.append(j)
            two_coor_atom_match_index.append(j_atom_coor_num_match_index)
        elif j_atom_coor_num == 3:
            three_coor_atom_index.append(j)
            three_coor_atom_match_index.append(j_atom_coor_num_match_index)
        elif j_atom_coor_num == 4: 
            four_coor_atom_index.append(j)
            four_coor_atom_match_index.append(j_atom_coor_num_match_index)
        elif j_atom_coor_num ==5:
            five_coor_atom_index.append(j)
            five_coor_atom_match_index.append(j_atom_coor_num_match_index)
        else:
            pass
    #先对配位数为3的原子进行分析判断
    sp2_number=0
    sp2_atom_index=[]
    image_sp2_number=0
    image_sp2_atom_index=[]
    for i in range(len(three_coor_atom_index)):
        point4=frac_coor[three_coor_atom_index[i]]
        point1=frac_coor[three_coor_atom_match_index[i][0]]
        point2=frac_coor[three_coor_atom_match_index[i][1]]
        point3=frac_coor[three_coor_atom_match_index[i][2]]
        i_distance=point2area_distance(point1, point2, point3, point4)
        if i_distance < 0.5: #是否是一个平面的判断标准是小于0.5埃
            sp2_number += 1
            sp2_atom_index.append(three_coor_atom_index[i])
        else:
            continue
    #再对配位数为2的原子进行分析判断
    for i in range(len(two_coor_atom_index)):
        i_match_index1=two_coor_atom_match_index[i][0]
        i_match_index2=two_coor_atom_match_index[i][1]
        if i_match_index1 in sp2_atom_index and i_match_index2 in sp2_atom_index:
            image_sp2_number += 1
            image_sp2_atom_index.append(two_coor_atom_index[i])
    #输出信息
    #print('Number of isolated atoms:',len(isolate_atom_index))
    #print('Single coordination atom number:',len(one_coor_atom_index))
    #print('Double coordination atom numbe:',len(two_coor_atom_index))
    #print('Three coordination atom number:',len(three_coor_atom_index))
    #print('four coordination atom number:',len(four_coor_atom_index))
    #print('five coordination atom number:',len(five_coor_atom_index))
    #print('number of sp2 atom:',sp2_number)
    #print('number of image sp2 atom:',image_sp2_number)
    print('sp atom content:',(len(two_coor_atom_index)-image_sp2_number)/atom_number)
    print('sp2 atom content:',(sp2_number+image_sp2_number)/atom_number)
    print('sp3 atom content:',len(four_coor_atom_index)/atom_number)
    end_time=time.time()
    print('End of code run, total cost time:',end_time-start_time) 
    '''#输出截断半径和平均配位数信息
    output_file_name='output_'+pos_name.split('.')[0]
    #print(output_file_name)
    output_info=open(output_file_name,'w')
    output_info.write('      cutoff       aver_coordination_number'+'\n')
    for i in range(len(cutoff_range)):
        output_info.write('    '+str(cutoff_range[i])+'     '+str(atom_coor_number_aver[i])+'\n')
    output_info.close()
    end_time=time.time()
    print('End of code run, total cost time:',end_time-start_time)'''








