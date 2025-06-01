import numpy as np
import math
import time
import os
import glob
import LASP_PythonLib
from LASP_PythonLib.structure_new import Str
from LASP_PythonLib.allstr_new import allstr as allstr_new
import shutil
import matplotlib.pyplot as plt

homepath = os.getcwd()
na_energy=-1.31
with open(os.path.join(os.path.join(os.path.join(os.path.join(homepath, '6_voltage'), '0_na'), '0-single'),'lasp.out'),'r') as n:
    content = n.readlines()
    total_line = len(content)
    no_na_jidi_single = 'false'
    for j in range(total_line):
        text = content[j].split()
        if len(text) != 0 and str(text[0]) == 'Energy,force':
            no_na_jidi_single = float(text[1])
        else:
            pass
with open(os.path.join(os.path.join(os.path.join(os.path.join(homepath, '6_voltage'), '0_na'), '0-ssw'),'lasp.out'),'r') as n:
    content = n.readlines()
    total_line = len(content)
    nn_energy_ssw = 'false'
    for j in range(total_line):
        text = content[j].split()
        if len(text) != 0 and str(text[0]) == 'minimum':
            no_na_jidi_ssw = float(text[5])
        else:
            pass

group12_x=[]
group12_y=[]
indata=open(os.path.join(os.path.join(os.path.join(homepath,'8_voltage_dis_group'),'12'),'energy.dat'))
content=indata.readlines()
for i in range(len(content)):
    i_content=content[i].strip().split()
    group12_x.append(float(i_content[0]))
    group12_y.append(float(i_content[1]))
indata.close()
group12_y_single=[]
for i in range(len(group12_y)):
    i_tranform = -(group12_y[i]-no_na_jidi_single-(i+1)*na_energy)/(i+1)
    group12_y_single.append(i_tranform)


group12_x_C=[]
group12_y_C=[]
indata=open(os.path.join(os.path.join(os.path.join(homepath,'8_voltage_dis_group'),'12_C'),'energy.dat'))
content=indata.readlines()
for i in range(len(content)):
    i_content=content[i].strip().split()
    group12_x_C.append(float(i_content[0]))
    group12_y_C.append(float(i_content[1]))
indata.close()
group12_y_single_C=[]
for i in range(len(group12_y_C)):
    i_tranform = -(group12_y_C[i]-no_na_jidi_single-(i+1)*na_energy)/(i+1)
    group12_y_single_C.append(i_tranform)
    
group21_x=[]
group21_y=[]
indata=open(os.path.join(os.path.join(os.path.join(homepath,'8_voltage_dis_group'),'21'),'energy.dat'))
content=indata.readlines()
for i in range(len(content)):
    i_content=content[i].strip().split()
    group21_x.append(float(i_content[0]))
    group21_y.append(float(i_content[1]))
indata.close()
group21_y_single=[]
for i in range(len(group21_y)):
    i_tranform = -(group21_y[i]-no_na_jidi_single-(i+1)*na_energy)/(i+1)
    group21_y_single.append(i_tranform)


group21_x_C=[]
group21_y_C=[]
indata=open(os.path.join(os.path.join(os.path.join(homepath,'8_voltage_dis_group'),'21_C'),'energy.dat'))
content=indata.readlines()
for i in range(len(content)):
    i_content=content[i].strip().split()
    group21_x_C.append(float(i_content[0]))
    group21_y_C.append(float(i_content[1]))
indata.close()
group21_y_single_C=[]
for i in range(len(group21_y_C)):
    i_tranform = -(group21_y_C[i]-no_na_jidi_single-(i+1)*na_energy)/(i+1)
    group21_y_single_C.append(i_tranform)

voltage_data_single=open(os.path.join(os.path.join(homepath,'8_voltage_dis_group'),'voltage_data_single.dat'),'w')

for i in range(len(group12_y)):
    voltage_data_single.write('%s  %s  %s  %s  %s   \n'% (group12_x[i],group12_y_single[i],group21_y_single[i],group12_y_single_C[i],group21_y_single_C[i]))      
voltage_data_single.close()
    
