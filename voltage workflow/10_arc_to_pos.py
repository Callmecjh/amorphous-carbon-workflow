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



if __name__ == "__main__":
#从all_str文件内提取出poscar文件，根据提供的序号标签
    AllStr = allstr_new()
    AllStr.arcinit([0,0],'input1.arc')
    AllStr[0].outPOSCAR('POSCAR_1')
    
    AllStr = allstr_new()
    AllStr.arcinit([0,0],'input2.arc')
    AllStr[0].outPOSCAR('POSCAR_2')
    
    AllStr = allstr_new()
    AllStr.arcinit([0,0],'input3.arc')
    AllStr[0].outPOSCAR('POSCAR_3')
        
    
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
    '''AllStr = allstr_new()
    AllStr.BuildCoordSet_fromPOSCAR(filename='hard-carbon-200Li-5200atom.vasp')
    #numberid = int(i.split('-')[1])
    outstr_name='input.arc'
    AllStr.Gen_arc(range(len(AllStr)),outstr_name,2)'''

    
'''path=os.getcwd()
    for i in range(150):
        os.chdir(path)
        os.mkdir('vasp-%d'%i)
        os.mkdir('NN-%d'%i)
        os.system('cp  KPOINTS  vasp-%d/'%(i))
        os.system('cp  POTCAR  vasp-%d/'%(i))
        os.system('cp  INCAR  vasp-%d/'%(i))
        os.system('cp  lasp.slurm  vasp-%d/'%(i))
        os.system('cp  input  vasp-%d/'%(i))
        os.system('cp  POSCAR-%d  vasp-%d/POSCAR'%(i,i))
        os.system('cp  outstr-%d.arc  vasp-%d/input.arc'%(i,i))
        #os.chdir(os.path.join(path,'vasp-%d'%i))
        #os.system('qsub lasp.slurm')
        os.system('cp  outstr-%d.arc  NN-%d/input.arc'%(i,i))
        os.system('cp  lasp.slurm  NN-%d/'%(i))
        os.system('cp  lasp.in  NN-%d/'%(i))
        os.system('cp  LiC.pot  NN-%d/'%(i))
        os.chdir(os.path.join(path,'vasp-%d'%i))
        os.system('qsub lasp.slurm')
        os.chdir(os.path.join(path,'NN-%d'%i))
        os.system('qsub lasp.slurm')'''
    
    
    
    

