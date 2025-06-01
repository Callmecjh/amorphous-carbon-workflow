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
        

#no_na_jidi_single=-17330.56445
#no_na_jidi_ssw=-17420.75977

group123_x=[]
group123_y=[]
group123_z=[]
#print('abc')
indata=open(os.path.join(os.path.join(os.path.join(homepath,'6_voltage'),'4_cluster_all'),'energy.dat'))
content=indata.readlines()
for i in range(len(content)):
    i_content=content[i].strip().split()
    group123_x.append(float(i_content[0]))
    group123_y.append(float(i_content[1]))
    group123_z.append(float(i_content[2]))
indata.close()
group123_y_single=[]
group123_y_ssw=[]
for i in range(len(group123_y)):
    i_tranform = -(group123_y[i]-no_na_jidi_single-(i+1)*na_energy)/(i+1)
    group123_y_single.append(i_tranform)
for i in range(len(group123_z)):
    i_tranform = -(group123_z[i]-no_na_jidi_ssw-(i+1)*na_energy)/(i+1)
    group123_y_ssw.append(i_tranform)

    
group132_x=[]
group132_y=[]
group132_z=[]
#print('abc')
indata=open(os.path.join(os.path.join(os.path.join(homepath,'7_voltage_path'),'132'),'energy.dat'))
content=indata.readlines()
for i in range(len(content)):
    i_content=content[i].strip().split()
    group132_x.append(float(i_content[0]))
    group132_y.append(float(i_content[1]))
    group132_z.append(float(i_content[2]))
indata.close()
group132_y_single=[]
group132_y_ssw=[]
for i in range(len(group132_y)):
    i_tranform = -(group132_y[i]-no_na_jidi_single-(i+1)*na_energy)/(i+1)
    group132_y_single.append(i_tranform)
for i in range(len(group132_z)):
    i_tranform = -(group132_z[i]-no_na_jidi_ssw-(i+1)*na_energy)/(i+1)
    group132_y_ssw.append(i_tranform)


group213_x=[]
group213_y=[]
group213_z=[]
#print('abc')
indata=open(os.path.join(os.path.join(os.path.join(homepath,'7_voltage_path'),'213'),'energy.dat'))
content=indata.readlines()
for i in range(len(content)):
    i_content=content[i].strip().split()
    group213_x.append(float(i_content[0]))
    group213_y.append(float(i_content[1]))
    group213_z.append(float(i_content[2]))
indata.close()
group213_y_single=[]
group213_y_ssw=[]
for i in range(len(group213_y)):
    i_tranform = -(group213_y[i]-no_na_jidi_single-(i+1)*na_energy)/(i+1)
    group213_y_single.append(i_tranform)
for i in range(len(group213_z)):
    i_tranform = -(group213_z[i]-no_na_jidi_ssw-(i+1)*na_energy)/(i+1)
    group213_y_ssw.append(i_tranform)

group231_x=[]
group231_y=[]
group231_z=[]
#print('abc')
indata=open(os.path.join(os.path.join(os.path.join(homepath,'7_voltage_path'),'231'),'energy.dat'))
content=indata.readlines()
for i in range(len(content)):
    i_content=content[i].strip().split()
    group231_x.append(float(i_content[0]))
    group231_y.append(float(i_content[1]))
    group231_z.append(float(i_content[2]))
indata.close()
group231_y_single=[]
group231_y_ssw=[]
for i in range(len(group231_y)):
    i_tranform = -(group231_y[i]-no_na_jidi_single-(i+1)*na_energy)/(i+1)
    group231_y_single.append(i_tranform)
for i in range(len(group231_z)):
    i_tranform = -(group231_z[i]-no_na_jidi_ssw-(i+1)*na_energy)/(i+1)
    group231_y_ssw.append(i_tranform)


group312_x=[]
group312_y=[]
group312_z=[]
#print('abc')
indata=open(os.path.join(os.path.join(os.path.join(homepath,'7_voltage_path'),'312'),'energy.dat'))
content=indata.readlines()
for i in range(len(content)):
    i_content=content[i].strip().split()
    group312_x.append(float(i_content[0]))
    group312_y.append(float(i_content[1]))
    group312_z.append(float(i_content[2]))
indata.close()
group312_y_single=[]
group312_y_ssw=[]
for i in range(len(group312_y)):
    i_tranform = -(group312_y[i]-no_na_jidi_single-(i+1)*na_energy)/(i+1)
    group312_y_single.append(i_tranform)
for i in range(len(group312_z)):
    i_tranform = -(group312_z[i]-no_na_jidi_ssw-(i+1)*na_energy)/(i+1)
    group312_y_ssw.append(i_tranform)


group321_x=[]
group321_y=[]
group321_z=[]
#print('abc')
indata=open(os.path.join(os.path.join(os.path.join(homepath,'7_voltage_path'),'321'),'energy.dat'))
content=indata.readlines()
for i in range(len(content)):
    i_content=content[i].strip().split()
    group321_x.append(float(i_content[0]))
    group321_y.append(float(i_content[1]))
    group321_z.append(float(i_content[2]))
indata.close()
group321_y_single=[]
group321_y_ssw=[]
for i in range(len(group321_y)):
    i_tranform = -(group321_y[i]-no_na_jidi_single-(i+1)*na_energy)/(i+1)
    group321_y_single.append(i_tranform)
for i in range(len(group321_z)):
    i_tranform = -(group321_z[i]-no_na_jidi_ssw-(i+1)*na_energy)/(i+1)
    group321_y_ssw.append(i_tranform)

voltage_data_single=open(os.path.join(os.path.join(homepath,'7_voltage_path'),'voltage_data_single.dat'),'w')
voltage_data_ssw=open(os.path.join(os.path.join(homepath,'7_voltage_path'),'voltage_data_ssw.dat'),'w')
for i in range(len(group123_x)):
    voltage_data_single.write('%s  %s  %s  %s  %s  %s  %s   \n'% (group123_x[i],group123_y_single[i],group132_y_single[i],group213_y_single[i],group231_y_single[i],group312_y_single[i],group321_y_single[i]))
    voltage_data_ssw.write('%s  %s  %s  %s  %s  %s  %s   \n'% (group123_x[i],group123_y_ssw[i],group132_y_ssw[i],group213_y_ssw[i],group231_y_ssw[i],group312_y_ssw[i],group321_y_ssw[i]))    
voltage_data_single.close()
voltage_data_ssw.close()
    
'''plt.plot(group123_x,group123_y_single,label='group 123',color='r')
plt.plot(group132_x,group132_y_single,label='group 132',color='g')
plt.plot(group213_x,group213_y_single,label='group 213',color='b')
plt.plot(group231_x,group231_y_single,label='group 231',color='y')
plt.plot(group312_x,group312_y_single,label='group 312',color='o')
plt.plot(group321_x,group321_y_single,label='group 321',color='p')
plt.xlabel('Na number')
plt.ylabel('Voltage(V)')
plt.legend()
ax = plt.gca()
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(True)


#plt.savefig('a.png')
plt.show()'''



'''fig,ax=plt.subplot(nrows=1,ncols=2)
ax[0].plot(group123_x,group123_y,label='group 123',color='r')
ax[0].plot(group132_x,group132_y,label='group 132',color='g')
ax[0].plot(group213_x,group213_y,label='group 213',color='b')
ax[0].plot(group231_x,group231_y,label='group 231',color='y')
ax[0].plot(group312_x,group312_y,label='group 312',color='o')
ax[0].plot(group321_x,group321_y,label='group 321',color='p')

ax[1].plot(group123_x,group123_z,label='group 123',color='r')
ax[1].plot(group132_x,group132_z,label='group 132',color='g')
ax[1].plot(group213_x,group213_z,label='group 213',color='b')
ax[1].plot(group231_x,group231_z,label='group 231',color='y')
ax[1].plot(group312_x,group312_z,label='group 312',color='o')
ax[1].plot(group321_x,group321_z,label='group 321',color='p')

plt.xlabel('Na number')
plt.ylabel('Voltage(V)')
plt.legend()'''








