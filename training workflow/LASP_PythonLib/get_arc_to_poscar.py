#! /home7/zpliu/anaconda2/bin/python

__author__ = 'zpliu learn from hsd Arcread.py'

import time
import cmath as m
import os
import numpy as np
import random
import sys
#import template as Tp
import string
sys.path.append('/home11/Liugroup/tools/')
#from XYZCoord import *   #  XYZCoord, BadStr, FooError, ParaWrap_JudgeShape, ParaWrap_Shortestbond
from multiprocessing import Pool
#import PeriodicTable as PT 
#from XYZCoordSet import CoordSet
import LASP_PythonLib 
from LASP_PythonLib.structure_new import Str
from LASP_PythonLib.allstr_new import allstr as allstr_new
import glob



if __name__ == "__main__":
    '''#从all_str文件内提取出poscar文件，根据提供的序号标签
    AllStr = allstr_new()
    AllStr.arcinit([0,0],'md-percular-opti.arc')
    total_str_num=len(AllStr)
    print(len(AllStr))
    #for i in range(0,total_str_num,10):
    AllStr[100].outPOSCAR('POSCAR_%d-percular'%(100))
    #AllStr[50].outPOSCAR('POSCAR_%d'%(50))
    #AllStr[800].outPOSCAR('POSCAR_%d'%(800))'''
    
    '''if len( sys.argv ) < 2 :
        print( "Please use following syntax :" )
        print( " pos2arc format " )
        print( " format : required argument, being arc2pos / pos2arc " )
        import sys
        sys.exit( )

    AllStr= allstr_new()'''
    
    '''poscar_list=[]
    path=os.getcwd()
    dir_file=os.listdir(path)
    for i in dir_file:
        if i.split('-')[0] == 'POSCAR':
            poscar_list.append(i)
    print(poscar_list)
    
    for i in poscar_list:'''

    #将单个poscar文件转为arc文件 
    for i in range(1,8):
        AllStr = allstr_new()
        AllStr.BuildCoordSet_fromPOSCAR(filename='%d.vasp'%i)
        #numberid = int(i.split('-')[1])
        outstr_name='input%d.arc'%i
        AllStr.Gen_arc(range(len(AllStr)),outstr_name,2)

    
    path=os.getcwd()
    for i in range(1,8):
        os.chdir(path)
        #os.mkdir('vasp-%d'%i)
        os.mkdir('NN-%d'%i)
        #os.system('cp  KPOINTS  vasp-%d/'%(i))
        #os.system('cp  POTCAR  vasp-%d/'%(i))
        #os.system('cp  INCAR  vasp-%d/'%(i))
        #os.system('cp  lasp.slurm  vasp-%d/'%(i))
        #os.system('cp  input  vasp-%d/'%(i))
        #os.system('cp  POSCAR%d  vasp-%d/POSCAR'%(i,i))
        #os.system('cp  input%d.arc  vasp-%d/input.arc'%(i,i))
        #os.chdir(os.path.join(path,'vasp-%d'%i))
        #os.system('qsub lasp.slurm')
        os.system('cp  input%d.arc  NN-%d/input.arc'%(i,i))
        os.system('cp  lasp.slurm  NN-%d/'%(i))
        os.system('cp  lasp.in  NN-%d/'%(i))
        os.system('cp  LiC.pot  NN-%d/LiC.pot'%(i))
        #os.chdir(os.path.join(path,'vasp-%d'%i))
        #os.system('qsub lasp.slurm')
        #os.chdir(os.path.join(path,'NN-%d-2'%i))
        #os.system('qsub lasp.slurm')
    
    '''homepath=os.getcwd()
    print(homepath)
    shuju=open('energy_vasp_NN-2','w')
    shuju.write('atom_num    vasp_energy    nn_energy'+'\n')
    for i in range(1,8):
        if not glob.glob('vasp-%d/OSZICAR'%i): 
            print('vasp-%d do not have OSZICAR'%i)
        elif not glob.glob('NN-%d/lasp.out'%i):
            print('NN-%d-2 do not have lasp.out'%i)
        else:
            with open(os.path.join(os.path.join(homepath,'vasp-%d'%i),'POSCAR'),'r') as p:
                content=p.readlines()
                total_line=len(content)
                atom_num=total_line-8
            with open(os.path.join(os.path.join(homepath,'vasp-%d'%i),'OSZICAR'),'r') as f:
                content=f.readlines()
                total_line=len(content)
                vasp_energy=str(content[total_line-1].split()[2])
            with open(os.path.join(os.path.join(homepath,'NN-%d-2'%i),'lasp.out'),'r') as n:
                content=n.readlines()
                total_line=len(content)
                #nn_energy=str(content[total_line-3].split()[1])
                print(str(content[total_line-3].split()[0]))
                nn_energy='false'
                for j in range(total_line):
                    text=content[j].split()
                    if len(text) != 0 and str(text[0]) == 'Energy,force':
                        nn_energy=float(text[1])
                    else:
                        pass
            shuju.write(str(i)+'    '+str(atom_num)+'    '+str(vasp_energy)+'    '+str(nn_energy)+'\n')
    shuju.close()'''
    
    '''path=os.getcwd()
    os.chdir(path) 
    for i in range(1,8):
        if glob.glob('vasp-%d/OSZICAR'%(i)):   
            icontrol= int(os.popen('cat vasp-%d/OSZICAR | wc -l'%(i)).readline().strip())  
            step=len(os.popen("grep 'F=' vasp-%d/OSZICAR"%(i)).readlines())  
            print(icontrol,step)
            if (icontrol < 100) and step == 1:   
                os.system('cat vasp-%d/allstr.arc >> 1.arc'%(i))    
                os.system('cat vasp-%d/allfor.arc >> 2.arc'%(i))
        
    tmpall= allstr_new() 
    tmpall.readfile('1.arc', '2.arc')   
    tmpall.shuffle(200)   
        
    #for str in tmpall: str.addCharge()  
        
    tmpall.genDataStr(range(len(tmpall)),    'TrainStr.txt')
    tmpall.genDataFor(range(len(tmpall)),    'TrainFor.txt')
    os.system('cat TrainStr.txt >> ../TrainStr.txt')
    os.system('cat TrainFor.txt >> ../TrainFor.txt')'''

