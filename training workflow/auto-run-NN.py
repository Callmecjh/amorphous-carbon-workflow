#! /usr/bin/env  /home10/python/bin/python

import os
import sys

#sys.path.append('/home10/kpl/Basic-tmp/')
import glob
import shutil
from multiprocessing import Pool,TimeoutError
import multiprocessing
import subprocess
import traceback
import time
import math
from LASP_PythonLib.allstr_new import BadStr
from LASP_PythonLib.allstr_new import allstr as allstr_new
from LASP_PythonLib.hostfile import Hostfile,runprog_cluster_manual
import numpy as np


class runssw(object):
    def __init__(self,SSWdir,cpuperjob,prog,masternode):
        self.dir =SSWdir
        self.cpuperjob =int(cpuperjob)
        self.prog= prog
        self.nbadneed=50
        self.masternode= masternode
        #self.prog='/home5/ssw-benchmark/vasp/sswoop/sswoop-4/main'

    def sethostfile(self):
        Host = Hostfile(self.dir,self.cpuperjob,self.masternode)
        #self.hostInfo, self.poolsize,totalproc= Host.setHostfile()
        hostdict= Host.setHostfile()
        return hostdict

    def run(self,njob,ncycle,nbadneed,maxtime,allstr,checkcycle):   
        #print(njob)
        #print(self.dir)
        workdirs,natomlist = self.buildSSWfolder(self.dir,njob,ncycle,allstr)  
        #print(workdirs,natomlist)
        #os.system('rm -rf killsignal')   
        exit =False
        self.nbadneed = nbadneed  
        task_id_list = []
        for i in range(int(njob)):
            #Ncore=32
            os.chdir(SSWdir)
            task_id_list.append(runprog_cluster_manual(workdirs[i]))  
        print('task id',task_id_list)
        alltime = 0
        while not exit:
            #print(checkcycle)
            time.sleep(checkcycle)
            alltime = alltime + checkcycle
            #print(workdirs,ncycle,allstr)
            time.sleep(10)
            time_task_id=[]
            #if ncycle == 1:
            '''for _tmp in range(1):
                try: 
                    nBad = int(os.popen('grep Energy allstr.arc-%d -c'%ncycle).readline().strip())  
                    #print(nBad)
                    #print(nbadneed)
                    #if (allstr==0 and nBad > nbadneed) or (allstr==1 and nBad > nbadneed*5) : break
                    if (allstr==0 and nBad > nbadneed) or (allstr==1 and nBad > nbadneed):    
                        break
                except:
                    time.sleep(10)
            if (allstr==0 and nBad > (nbadneed*2)) or (allstr==1 and nBad > (nbadneed*2)):  
                print('terminate: enough nBad')
                self.sendstopsignal(workdirs,ncycle)  
                time.sleep(60)
                exit= True
                for i in task_id_list:
                    os.system('qdel %s'%i)
                print('all work done in SSW')'''
            task_info = os.popen('squeue').readlines()    
            #print(task_info)
            for i in range(1,len(task_info)):  
                job_id = task_info[i].split()[0]
                job_user = task_info[i].split()[3]
                if job_user == 'roger':  
                    time_task_id.append(job_id)
                else:
                    continue
            job_nmber=0
            for i in time_task_id:
                if i in task_id_list:
                    job_nmber += 1
            if job_nmber == 0:  
                print('all VASP task work calculate finished')
                exit =True
            if alltime >= maxtime:   
                print('teminate: too long time')
                self.sendstopsignal(workdirs,ncycle)  
                time.sleep(60)
                exit = True
                for i in task_id_list:
                    os.system('scancel %s'%i)
                print('all work done in SSW')
            '''else:
                for _tmp in range(1):
                    try: 
                        nBad = int(os.popen('grep Energy allstr.arc-%d -c'%ncycle).readline().strip())  
                        #print(nBad)
                        #print(nbadneed)
                        #if (allstr==0 and nBad > nbadneed) or (allstr==1 and nBad > nbadneed*5) : break
                        if (allstr==0 and nBad > nbadneed) or (allstr==1 and nBad > nbadneed):    
                            break
                    except:
                        time.sleep(10)
                if alltime >= maxtime:   
                    print('teminate: too long time')
                    self.sendstopsignal(workdirs,ncycle)  
                    time.sleep(60)
                    exit = True
                    for i in task_id_list:
                        os.system('scancel %s'%i)'''
        self.collectdata(workdirs,ncycle,allstr)
        nBad = int(os.popen('grep Energy allstr.arc-%d -c'%ncycle).readline().strip())
        return nBad
        '''for i in range(int(njob)):
            #Ncore=int(math.ceil(natomlist[i]/(math.ceil(float(natomlist[i])/self.cpuperjob))))  
            #Ncore=math.ceil(float(natomlist[i])/self.cpuperjob)*self.cpuperjob
            #print(workdirs[i],self.prog,self.hostInfo,Ncore,self.dir,os.environ,poolcount)
            Ncore=32
            runprog_cluster_manual(i,workdirs[i],self.prog,self.hostInfo,Ncore,self.dir,os.environ,poolcount)
            #result.append(pool.apply_async(runprog_cluster_manual,args= (workdirs[i],self.prog,self.hostInfo,Ncore,self.dir,os.environ,poolcount))) 
            #if self.poolsize > 15:
            #   time.sleep(0.5)
            #try:
            #    print result.get(timeout=100)
            #except TimeourError:
            #    print('time out: job %s'%workdirs[i])
        while not exit:    
            print('yes')
            print(checkcycle)
            time.sleep(180)
            alltime = alltime + 10
            self.collectdata(workdirs,ncycle,allstr)
            time.sleep(10)
            for _tmp in range(5):
            #    if glob.glob('allstr.arc-%d'%ncycle):
                 try: 
                    nBad = int(os.popen('grep Energy allstr.arc-%d -c'%ncycle).readline().strip())
                    #if (allstr==0 and nBad > nbadneed) or (allstr==1 and nBad > nbadneed*5) : break
                    if (allstr==0 and nBad > nbadneed) or (allstr==1 and nBad > nbadneed) : break
                 except: time.sleep(10)
#           nBad = int(os.popen('grep Energy allstr.arc-%d -c'%ncycle).readline().strip())
            #if (allstr==0 and nBad > nbadneed) or (allstr==1 and nBad > nbadneed*5) :
            if (allstr==0 and nBad > nbadneed) or (allstr==1 and nBad > nbadneed) :
                print('terminate: enough nBad')
                self.sendstopsignal(workdirs,ncycle)
                time.sleep(60)
                exit= True
                pool.terminate()
            if alltime >= maxtime:
                print('teminate: too long time')
                self.sendstopsignal(workdirs,ncycle)
                time.sleep(60)
                exit =True
                pool.terminate()
            if glob.glob('killsignal'):
                sendkillsignal(workdirs)
                print('External signal: will be terminated in few sceonds')
                time.sleep(60)
                exit=True
                pool.terminate()
            process_count=len(pool._cache)
            if process_count ==0:
                print('all work done')
                exit=True
                #pool.terminate()
                time.sleep(60) 
                pool.terminate()
            #if glob.glob('terminatesignal'):
            #    print 'forced termination of pool'
            #    exit=True
            #    pool.terminate()
            #    time.sleep(60)
        process_count=len(pool._cache)
        if (exit) and (process_count!=0):
            time.sleep(60)
            process_count=len(pool._cache)
            if process_count!=0:
                sendkillsignal(workdirs)
                time.sleep(60)
                print('forced termination of pool')
                pool.terminate()

        pool.close()
        pool.join()
        if alltime >= maxtime:
            print('suggest change setting')
        time.sleep(30)
        self.collectdata(workdirs,ncycle, allstr)
        time.sleep(10)
        for _tmp in range(5):
            try:
               nBad = int(os.popen('grep Energy allstr.arc-%d -c'%ncycle).readline().strip())
               #if (allstr==0 and nBad > nbadneed) or (allstr==1 and nBad > nbadneed*5) : break
               if (allstr==0 and nBad > nbadneed) or (allstr==1 and nBad > nbadneed) : break
            except: time.sleep(10)
#       nBad = int(os.popen('grep Energy allstr.arc-%d -c'%ncycle).readline().strip())

#       for _tmp in range(500):
#           if glob.glob('allstr.arc-%d'%ncycle):
#               break
#           time.sleep(10)
#       nBad = int(os.popen('grep Energy allstr.arc-%d -c'%ncycle).readline().strip())
        return nBad'''   
 
    def sendstopsignal(self,workdirs,ncycle):  
        os.chdir(self.dir)
        for i in range(len(workdirs)):
            os.system('echo stop > %s/softstop'%(workdirs[i]))
        return 


    def buildSSWfolder(self,SSWdir,njob,ncycle,allstr):  
        os.chdir(SSWdir)   
        if os.path.exists('../NN/%s.pot'%(jobname)):  
            shutil.copy('../NN/%s.pot'%(jobname),'./sourcedir/')
            NN_exists=True
        else:
            NN_exists=False
        workdir = []
        Natom = []
        #if ncycle%2 == 0:
            #AllStr0= allstr_new()  
        #AllStr1= allstr_new()
            #AllStr0.arcinit([0,0],'./sourcedir/Badstr.arc-%d'%(ncycle-1))
            #AllStr0.RandomArange(200)
        #else:
        AllStr0= allstr_new()
        AllStr0.arcinit([0,0],'./sourcedir/allstr-ini.arc')
        AllStr0.RandomArange(200)
        for i in range(int(njob)):  #njob就是几个初始构型
            AllStr0.Gen_arc([i],'outstr.arc')   
            os.system('mv outstr.arc ./sourcedir/input.arc_%s'%(i))
        '''if ncycle == 1 or ncycle == 2:  
            AllStr0.arcinit([0,0],'./sourcedir/allstr-ini.arc')   
            AllStr0.RandomArange(200) 
        else:
            badstr_number = int(len(os.popen('grep Energy Badstr.arc-%d'%(ncycle-1)).readlines()))
            if badstr_number >= njob:   
                AllStr0.arcinit([0,0],'./Badstr.arc-%d'%(ncycle-1))
                AllStr0.RandomArange(200)
            elif badstr_number == 0:
                AllStr0.arcinit([0,0],'./allstr.arc-%d'%(ncycle-1))
                AllStr0.RandomArange(200)
            else:
                AllStr0.arcinit([0,0],'./Badstr.arc-%d'%(ncycle-1))
                AllStr1.arcinit([0,0],'./allstr.arc-%d'%(ncycle-1))  
                AllStr0.RandomArange(200)
                AllStr1.RandomArange(200)
                allstr_number = int(njob)-badstr_number'''
        #print(AllStr0)  
        #print(njob)
        #os.system('rm -r ./sourcedir/input.arc_*')  
        '''if ncycle == 1 or ncycle == 2:
            for i in range(int(njob)):  
                AllStr0.Gen_arc([i],'outstr.arc')   
                os.system('mv outstr.arc ./sourcedir/input.arc_%s'%(i))   
        else:
            if badstr_number >= njob:
                for i in range(int(njob)):  
                    AllStr0.Gen_arc([i],'outstr.arc')   
                    os.system('mv outstr.arc ./sourcedir/input.arc_%s'%(i))   
            elif badstr_number == 0:
                for i in range(int(njob)):  
                    AllStr0.Gen_arc([i],'outstr.arc')   
                    os.system('mv outstr.arc ./sourcedir/input.arc_%s'%(i))  
            else:
                for i in range(int(badstr_number)):
                    AllStr0.Gen_arc([i],'outstr.arc')   
                    os.system('mv outstr.arc ./sourcedir/input.arc_%s'%(i))
                for i in range(int(allstr_number)):
                    AllStr1.Gen_arc([i],'outstr.arc')
                    os.system('mv outstr.arc ./sourcedir/input.arc_%s'%(i+badstr_number))'''

        inputfile= glob.glob('./sourcedir/input.arc*')  
        #print(inputfile)  
        inputlist = []
        for item in inputfile:
            inputlist.append(item.split('_')[-1])   
        #print(inputlist)
        ntype= len(inputlist)  
        print(ntype)
#       if ncycle>1:
#           os.system('rm -f  best.arc*')
#           for i in range(njob):
#               itype = i%ntype
#               dir ="SSW-%d-%d" %(ncycle-1,i)
#               os.system('rm -f %s/all*.arc '%(dir))
#               os.system('cat %s/best.arc >> best.arc-%s'%(dir,inputlist[itype]))
#           for i in range(ntype):
#               AllStr= screen.CoordSet()
#               AllStr.arcinit([0,0],'best.arc-%s'%(inputlist[i]))
#               if (len(AllStr)== 0): continue
#               AllStr=AllStr.sortbyE()
#               AllStr.Gen_arc([0],'outstr.arc')
#               os.system('mv outstr.arc ./sourcedir/input.arc_%s'%(inputlist[i]))
#       if ncycle==1:
#           os.system('rm -f  *.arc*')
#           for i in range(njob):
#               itype = i%ntype
#               dir ="SSW-%d-%d" %(ncycle,i)
#               if not glob.glob(dir): break
#               os.system('rm -f %s/kill* %s/soft* '%(dir,dir))
#             # os.system('cat %s/best.arc >> best.arc-%s'%(dir,inputlist[itype]))
#               os.system('cat %s/all.arc >> all.arc-%s'%(dir,inputlist[itype]))
#           if ncycle==2:
#               for i in range(njob):
#                   itype = i%ntype
#                   AllStr= screen.CoordSet()
#                   AllStr.arcinit([0,0],'best.arc-%s'%(inputlist[itype]))
#                   if (len(AllStr)== 0): continue
#                   AllStr=AllStr.sortbyE()
#                   AllStr.Gen_arc([0],'outstr.arc')
#                   os.system('mv outstr.arc ./sourcedir/input.arc_%s'%(inputlist[itype]))
#           if ncycle==1:
#               for i in range(njob):
#                   itype = i%ntype
#                   if not glob.glob('all.arc-%s'%(inputlist[itype])): break
#                   AllStr= allstr_new()
#                   AllStr.arcinit([0,0],'all.arc-%s'%(inputlist[itype]))
#                   if (len(AllStr)== 0): continue
#                   try:  AllStr=allstr_new(AllStr[len(AllStr)-10:len(AllStr)])
#                   except: AllStr=allstr_new(AllStr[:len(AllStr)])
#                   AllStr=AllStr.sortbyE()
#                   AllStr.Gen_arc([0],'outstr.arc')
#                   os.system('mv outstr.arc ./sourcedir/input.arc_%s'%(inputlist[itype]))

        for i in range(int(njob)):  
            #os.chdir(SSWdir)
            itype = i%ntype   
            dir ="SSW-%d-%d" %(ncycle,i)
            workdir.append(dir)
            #print(dir)
            #print(os.getcwd())
            if not glob.glob(dir): 
                os.mkdir(dir)  
            shutil.copy('../lasp.slurm','%s/lasp.slurm'%dir)   
            shutil.copy('./sourcedir/input.arc_%s'%(inputlist[itype]),'%s/input.arc'%dir)  

            os.system('sed -i "/^SSW.printevery/d" ./sourcedir/input.%s '%(inputlist[itype]))   
            os.system('sed -i "/^SSW.printselect/d" ./sourcedir/input.%s '%(inputlist[itype]))
            os.system('sed -i "/^SSW.printdelay/d" ./sourcedir/input.%s '%(inputlist[itype]))
            os.system('sed -i "/^SSW.Safe_hardcurv/d" ./sourcedir/input.%s '%(inputlist[itype]))
            os.system('sed -i "/^supercell/d" ./sourcedir/input.%s '%(inputlist[itype]))

            if allstr==0:
                os.system('sed -i "1i\SSW.printevery F" ./sourcedir/input.%s'%(inputlist[itype]))
            if allstr==1:
                os.system('sed -i "1i\SSW.printevery T" ./sourcedir/input.%s'%(inputlist[itype]))   
                os.system('sed -i "1i\SSW.printselect 6" ./sourcedir/input.%s'%(inputlist[itype]))
                os.system('sed -i "1i\SSW.printdelay  2" ./sourcedir/input.%s'%(inputlist[itype]))
                os.system('sed -i "1i\SSW.Safe_hardcurv  150" ./sourcedir/input.%s'%(inputlist[itype]))

            #shutil.copy('./sourcedir/input.%s'%(inputlist[itype]),'%s/input'%dir)
            if NN_exists:
                shutil.copy('./sourcedir/%s.pot'%(jobname),dir)
                #self.alter(os.path.join(os.path.join(SSWdir,'sourcedir'),'input.%s'%(inputlist[itype])),'potential NN','potential NN')
                os.system("sed -i 's/potential.*/potential  NN/g' ./sourcedir/input.%s"%(inputlist[itype])) 
                os.system("sed -i 's/SSW.SSWsteps.*/SSW.SSWsteps 500/g' ./sourcedir/input.%s"%(inputlist[itype]))  #ssw步数的修改
            else:
                shutil.copy('./sourcedir/INCAR',dir)   
                shutil.copy('./sourcedir/KPOINTS',dir)
                shutil.copy('./sourcedir/POTCAR',dir)
                #self.alter(os.path.join(os.path.join(SSWdir,'sourcedir'),'input.%s'%(inputlist[itype])),'potential NN','potential VASP')
                os.system("sed -i 's/potential.*/potential  VASP/g' ./sourcedir/input.%s"%(inputlist[itype]))
            Natom.append(int(os.popen('cat ./%s/input.arc | wc -l'%dir).readline().strip())-7)   
            #if Natom[i]==1: 
                #os.system('sed -i "1i\supercell 5 5 1" ./sourcedir/input.%s'%(inputlist[itype]))  
            #elif Natom[i]==2: 
                #os.system('sed -i "1i\supercell 2 2 2" ./sourcedir/input.%s'%(inputlist[itype]))  
            #elif Natom[i]==4: 
                #os.system('sed -i "1i\supercell 3 3 1" ./sourcedir/input.%s'%(inputlist[itype])) 
            #elif Natom[i]==6: 
                #os.system('sed -i "1i\supercell 2 2 1" ./sourcedir/input.%s'%(inputlist[itype])) 
            #elif Natom[i]==8: 
                #os.system('sed -i "1i\supercell 2 2 1" ./sourcedir/input.%s'%(inputlist[itype])) 
            #elif Natom[i]==32:
                #os.system('sed -i "1i\supercell 1 1 1" ./sourcedir/input.%s'%(inputlist[itype]))  
            shutil.copy('./sourcedir/input.%s'%(inputlist[itype]),'%s/lasp.in'%dir)
            
        return workdir,Natom

    def alter(self,file,old_str,new_str):   
        file_data = ""
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                if old_str in line:
                    line = line.replace(old_str,new_str)
                file_data += line
        with open(file,"w",encoding="utf-8") as f:
            f.write(file_data)


    def compare(self,ncycle):   
        nn= allstr_new()
        nn.readfile('allstr.arc-%d'%ncycle)
        vasp =allstr_new()
        vasp.readfile('1.arc')
        if (len(nn)!= len(vasp)):
            print('some str failed to dft cal')
        else :
            eall =0
            for i in range(len(nn)):
                eall=eall+np.square(nn[i].energy-vasp[i].energy)
            rmse= np.sqrt(eall/len(nn))
            print('rmsE %14.8f eV'%rmse)

    def collectdata(self,workdirs,ncycle,allstr):   
        os.chdir(self.dir)
        #print(self.dir)
        #os.system('rm -f *.arc*')
#        for i in range(len(workdirs)):
#            if allstr==0: 
#                os.system('cat %s/Badstr.arc >> allstr.arc-%d'%(workdirs[i],ncycle))
#            if allstr==1:
##                os.system('cat %s/allstr.arc >> allstr.arc-%d'%(workdirs[i],ncycle))
#                 self.collectallstr(workdirs,i,ncycle)
##                try: os.system('cat %s/outstr.arc >> allstr.arc-%d'%(workdirs[i],ncycle))
##                except: continue
        #allproc = np.unique([line.split()[0] for line in open('.hostfile')])   
        #print(allproc)
        #if not os.path.exists('nodejob.py'): os.system ('ln -s ../nodejob.py .') 

        #global poolcount
        #poolcount = poolcount + len(allproc)
        #pool = Pool(processes=len(allproc))
        count = 0
        for wdir in workdirs: 
            if allstr == 0: 
                os.system('cat %s/Badstr.arc >> allstr.arc-%d'%(wdir,ncycle))   
            else:
                #procid = count%len(allproc)
                #print(procid)
                #pool.apply_async(collectallstr, (allproc[procid], wdir, self.nbadneed))
                #print(allproc[procid], wdir, self.nbadneed)
                #print(type(self.nbadneed))
                collectallstr(wdir, self.nbadneed)   
        #pool.close(); pool.join()

        time.sleep(10)
        for i in range(len(workdirs)):
            os.system('cat %s/Badstr.arc >> Badstr.arc-%d'%(workdirs[i],ncycle))  
            if glob.glob('%s/outstr.arc'%(workdirs[i])): os.system('cat %s/outstr.arc >> allstr.arc-%d'%(workdirs[i],ncycle))  
       
        #os.system('rm -f ../VASP/*.arc-%d; ln -s ../SSW/allstr.arc-%d ../VASP/'%(ncycle,ncycle))   
        os.system('ln -s ../SSW/allstr.arc-%d ../VASP/'%(ncycle))
        os.system('ln -s ../SSW/Badstr.arc-%d ../VASP/'%(ncycle))
        os.system('cp ../SSW/Badstr.arc-%d ../SSW/sourcedir'%(ncycle))
        return

#    def collectallstr(self,workdirs,i,ncycle):
#
#        AllStr= screen.CoordSet()
#        AllStr.arcinit([0,0],'%s/allstr.arc'%(workdirs[i])) #, '%s/allfor.arc'%(workdirs[i]))
#        if (len(AllStr)== 0): return
#        AllStr.RandomArange(200)
#        AllStr = screen.CoordSet(AllStr[:self.nbadneed])
#        AllStr.Gen_arc(range(len(AllStr)),'outstr.arc',2)
##       if AllStr[0].Lfor: AllStr.Gen_Forarc(range(len(AllStr)),'outfor.arc',2)
#        return


class runvasp(object):
    def __init__(self,vaspdir,cpuperjob,prog, masternode):
        self.dir =vaspdir
        self.cpuperjob =int(cpuperjob)
        self.prog = prog
#       self.base =base
        self.masternode = masternode
        #self.prog='/home7/bin/lsasp-20171227'

    def sethostfile(self):
        Host = Hostfile(self.dir,self.cpuperjob,self.masternode)
        #self.hostInfo, self.poolsize ,total= Host.setHostfile()
        hostdict= Host.setHostfile()

    def run(self,ncycle,nbadneed,maxF,maxtime,maxtimeperjob=False, Lallstr=0):  
        self.pooluse =0
        self.nmax = nbadneed
        self.maxF = maxF

        os.chdir(self.dir)
        print(self.dir)
        if not glob.glob('cycle-%d'%ncycle): 
            os.mkdir('cycle-%d'%ncycle)
        os.system('cp Badstr.arc-%d ./cycle-%d/Badstr.arc-%d'%(ncycle,ncycle,ncycle))
        os.system('cp allstr.arc-%d ./cycle-%d/allstr.arc-%d'%(ncycle,ncycle,ncycle))
        '''self.screendata('allstr.arc-%d'%ncycle, nmax = nbadneed)  
        if not glob.glob('cycle-%d'%ncycle): 
            os.mkdir('cycle-%d'%ncycle)  
        if glob.glob('outstr.arc'): 
            os.system('mv outstr.arc ./cycle-%d/allstr.arc-%d'%(ncycle,ncycle))  

        if glob.glob('Badstr.arc-%d'%ncycle):    
            self.screendata('Badstr.arc-%d'%ncycle, nmax = nbadneed)
            if glob.glob('outstr.arc'): 
                os.system('cat outstr.arc >> ./cycle-%d/allstr.arc-%d'%(ncycle,ncycle))

        if glob.glob('AddVASPcal.arc'):  
            os.system('cat AddVASPcal.arc >> ./cycle-%d/allstr.arc-%d'%(ncycle,ncycle))
            os.system('mv AddVASPcal.arc AddVASPcal.arc-addedcycle%d'%(ncycle))
#       os.system('rm -f allstr.arc-%d'%ncycle)'''

        workdir =os.path.join(self.dir,'cycle-%d'%ncycle)
        #shutil.copy('allstr.arc-%d'%ncycle,workdir)
        os.chdir(workdir)
        #os.system('rm -rf killsignal')

        #AllStr1= allstr_new()
        #AllStr1.readfile('allstr.arc-%d'%ncycle)  #allstr.                 
        #AllStr1.RandomArange(200)
        AllStr1= allstr_new()
        AllStr1.readfile('Badstr.arc-%d'%ncycle)
        
        
        workdirs=[]
        exit = False
        alltime =0
        result = []
        task_id_list = []
        #pool = poolshell(self.poolsize)
        #print(pool)
        #print('Allstr number:',len(AllStr1)+100)
        print('Allstr number:',len(AllStr1))
        '''for i in range(len(AllStr[:100])):  
            os.chdir(workdir)
            AllStr.printlist([i],'input.arc_%d'%i)  
            if not glob.glob('para%d'%(i+1)) : os.system('mkdir para%d'%(i+1))  
            if glob.glob('para%d/allstr.arc'%(i+1)): 
                icontrol= int(os.popen('cat para%d/OSZICAR | wc -l'%(i+1)).readline().strip())
                icontrol0= int(os.popen('cat para%d/allstr.arc | wc -l'%(i+1)).readline().strip())
                if icontrol < 100 and icontrol0 > 5: continue   
#           os.system('rm -fr para%d; mkdir para%d'%(i+1,i+1))
           #changeinput = allstr_k()
           #changeinput.readfile('input.arc_%d'%i)
            AllStr[i].outPOSCAR('POSCAR_%d'%i)  #POSCAR
            AllStr[i].genPOTCAR('../sourcedir/','POTCAR_%d'%i) 

            os.system('cp  ../sourcedir/KPOINTS  para%d'%(i+1))  
            self.prog=para['prog']['VASP'] 
            #print(self.prog)
            #if AllStr[i].abc[0]== AllStr[i].abc[1] and \    #
               #AllStr[i].abc[1]==AllStr[i].abc[2] and \
               #AllStr[i].abc[1] > 9.99 :
                #os.system('\cp  ../sourcedir/KPOINTS_gamma  para%d/KPOINTS'%(i+1))
                #self.prog=para['prog']['VASPgamma']

#           if AllStr[i].abc[0]>9.90 and \
#               AllStr[i].abc[1]>9.90 and \
#               AllStr[i].abc[2] > 9.90 :
#               os.system('\cp  ../sourcedir/KPOINTS_gamma  para%d/KPOINTS'%(i+1))
#               self.prog=para['prog']['VASPgamma']

            os.system('rm -f para%d/input; cp  ../sourcedir/input  para%d'%(i+1,i+1))  
            os.system('cp  ../sourcedir/INCAR  para%d'%(i+1))  
            #os.system('sed -i "/^LDAU /d" para%d/INCAR'%(i+1))
            os.system('mv input.arc_%d para%d/input.arc'%(i,i+1))  
            os.system('mv POSCAR_%d para%d/POSCAR'%(i,i+1))
            os.system('mv POTCAR_%d para%d/POTCAR'%(i,i+1))
            os.system('cp  ../../lasp.slurm  para%d'%(i+1))
#           Nc=0; No=0; Nh=0; Nn=0
#           for i0,x in enumerate(AllStr[i].elenameList):
#              if x=='O': No = AllStr[i].natompe[i0]
#              if x=='C': Nc = AllStr[i].natompe[i0]
#              if x=='F': Nn  = AllStr[i].natompe[i0]
#              if x=='H': Nh = AllStr[i].natompe[i0]
#           a='';b='';c='';d=''
#           for i0,x in enumerate(AllStr[i].elenameList):
#              if x=='O':  Nx=1 
#              if x=='H':  Nx=0
#              if x=='C':  Nx=0
#              if x=='F':  Nx=1
#              if float(2*Nco/(2*No-Nh))>  0.9: Nx=1; LDAUL=2; LDAUU=3.5; LDAUJ=0.0
#              if float(2*Nco/(2*No-Nh))<= 0.73: Nx=3; LDAUL=2; LDAUU=3.5; LDAUJ=0.0
#              if x=='H': Nx=0; LDAUL=-1; LDAUU=0.0; LDAUJ=0.0
#              a += '%d*%d '%(AllStr[i].natompe[i0],Nx)
#              b += '%d '%(LDAUL)
#              c += '%.1f '%(LDAUU)
#              d += '%.1f '%(LDAUJ)
#           if((Nh+7*Nn+4*Nc+6*No)%2 ==1):
#              os.system('sed -i "1a \ISPIN = 2" para%d/INCAR'%(i+1))
#              os.system('sed -i "1a \MAGMOM = %s" para%d/INCAR'%(a,i+1))
#           os.system('sed -i "1a \LDAUL = %s" para%d/INCAR'%(b,i+1))
#           os.system('sed -i "1a \LDAUU = %s" para%d/INCAR'%(c,i+1))
#           os.system('sed -i "1a \LDAUJ = %s" para%d/INCAR'%(d,i+1))

#LDAUL = -1 2 -1
#LDAUU = 0.0 3.3 0.0
#LDAUJ = 0.0 0.0 0.0

            workdirs.append('para%d'%(i+1))
            #print 'runjob',i+1
            #result = pool.apply_async(singlevaspRun, args=('para%d'%(i+1),self.prog, vaspcpu))
            #os.chdir('../')
            #print(workdir)
            #task_id_list.append(runprog_cluster_manual('cycle-%d/para%d'%(ncycle,i+1)))
            #result.append( pool.apply_async(runprog_cluster_manual,args=('cycle-%d/para%d'%(ncycle,i+1),self.prog, self.hostInfo,self.cpuperjob,self.dir,os.environ,poolcount,maxtimeperjob)))  
            #if self.poolsize > 15:            
                #time.sleep(1)'''  

        for i in range(len(AllStr1)):
            os.chdir(workdir)
            AllStr1.printlist([i],'input.arc_%d'%(i))  
            if not glob.glob('para%d'%(i)) : os.system('mkdir para%d'%(i))  
            if glob.glob('para%d/allstr.arc'%(i)): 
                icontrol= int(os.popen('cat para%d/OSZICAR | wc -l'%(i)).readline().strip())
                icontrol0= int(os.popen('cat para%d/allstr.arc | wc -l'%(i)).readline().strip())
                if icontrol < 100 and icontrol0 > 5: continue   
            AllStr1[i].outPOSCAR('POSCAR_%d'%(i))  #POSCAR
            AllStr1[i].genPOTCAR('../sourcedir/','POTCAR_%d'%(i)) 
            os.system('cp  ../sourcedir/KPOINTS  para%d'%(i))  
            self.prog=para['prog']['VASP']
            os.system('rm -f para%d/input; cp  ../sourcedir/input  para%d'%(i,i))  
            os.system('cp  ../sourcedir/INCAR  para%d'%(i))  
            os.system('mv input.arc_%d para%d/input.arc'%(i,i))  
            os.system('mv POSCAR_%d para%d/POSCAR'%(i,i))
            os.system('mv POTCAR_%d para%d/POTCAR'%(i,i))
            os.system('cp  ../../lasp.slurm  para%d'%(i))
            workdirs.append('para%d'%(i))
            #os.chdir('../')
            #task_id_list.append(runprog_cluster_manual('cycle-%d/para%d'%(ncycle,i+1+100)))
        
        for i in range(len(AllStr1)):
            os.chdir(workdir)
            total_line= int(os.popen('cat para%d/POSCAR | wc -l'%(i)).readline().strip())
            C_number=total_line-8
            poscar=open(os.path.join(os.path.join(workdir,'para%d'%(i)),'POSCAR'),'r')
            indata=poscar.readlines()
            new_poscar=open(os.path.join(os.path.join(workdir,'para%d'%(i)),'POSCAR'),'w')
            for j in range(len(indata)):
                if i == 6:
                    new_poscar.write('   %d'%C_number+'\n')
                else:
                    new_poscar.write(indata[j])
            poscar.close()
            new_poscar.close()
            task_id_list.append(runprog_cluster_manual('para%d'%(i)))
            
        
        while not exit:    
            time.sleep(60)
            alltime= alltime + 120
            os.chdir(workdir)
            time_task_id = []
            task_info = os.popen('squeue').readlines()    
            #print(task_info)
            for i in range(1,len(task_info)):  
                job_id = task_info[i].split()[0]
                job_user = task_info[i].split()[3]
                if job_user == 'roger':  
                    time_task_id.append(job_id)
                else:
                    continue
            job_nmber=0
            for i in time_task_id:
                if i in task_id_list:
                    job_nmber += 1
            if job_nmber == 0:  
                print('all VASP task work calculate finished')
                exit =True
            if alltime >= maxtime:   
                print('teminate: too long time')
                #sendkillsignal(workdirs)  
                time.sleep(60)
                exit =True
                #pool.terminate()
                for i in time_task_id:
                    if i in task_id_list:
                        os.system('scancel %s'%i)            
            #if glob.glob('killsignal'): 
                #sendkillsignal(workdirs)
                #print('External signal: will be terminated in few sceonds')
                #time.sleep(60)
                #exit=True
                #pool.terminate()
            #process_count=len(pool._cache)
            #if process_count ==0:
                #print('all work done')
                #exit=True
                #pool.terminate()
            #if glob.glob('terminatesignal'):
            #    print 'forced termination of pool'
            #    exit=True
            #    pool.terminate()
            #    time.sleep(60)
        #os.system('echo poolclose > msg')
        #process_count=len(pool._cache)
        #if (exit) and (process_count!=0):
            #time.sleep(60)
            #process_count=len(pool._cache)
            #print(process_count)
            #if process_count!=0:
                #sendkillsignal(workdirs)
                #time.sleep(60)
                #print('forced termination of pool')
                #pool.terminate()


        #pool.close()
        #pool.join()

        #self.pooluse = self.pooluse + self.poolsize

        print('Start collect data')
        #os.system('cp  ../sourcedir/OSZICAR  para1')
        self.collectdata(ncycle,len(AllStr1))   #得到1.arc结构文件和2.arc受力文件
        #if(Lallstr==0): self.compare(ncycle)
        self.compare(ncycle)
        self.screendata('1.arc',forcefile ='2.arc')  
        naddstr = self.arc2traindata()  
        os.system('cat TrainStr.txt >> ../../NN/TrainStr.txt  ')  
        os.system('cat TrainFor.txt >> ../../NN/TrainFor.txt  ')  
        #os.system('cp ../../lasp.slurm ../../NN/lasp.slurm')
        time.sleep(120)
        return naddstr  

    def getallpath(self,dir):
        pathlist = []
        for i in os.listdir(dir):
            if( i.split('a')[0] == 'p'):
                pathlist.append(i)
        return pathlist


    def compare(self,ncycle):    
        nn= allstr_new()
        nn.readfile('allstr.arc-%d'%ncycle)
        vasp =allstr_new()
        vasp.readfile('1.arc')
        if (len(nn)!= len(vasp)):
            print('some str failed to dft cal')  
        else :
            eall =0
            for i in range(len(nn)):
                eall=eall+np.square(nn[i].energy-vasp[i].energy)  
            rmse= np.sqrt(eall/len(nn))
            print('rmsE %14.8f eV'%rmse)   


    def collectdata(self,ncycle,nstr):   
        os.chdir(self.dir)
        os.chdir('cycle-%d'%ncycle)
        #os.system('rm -rf 1.arc')
        #os.system('rm -rf 2.arc')
        for i in range(nstr):
            if glob.glob('para%d/OSZICAR'%(i)):   
                icontrol= int(os.popen('cat para%d/OSZICAR | wc -l'%(i)).readline().strip())  
                step=len(os.popen("grep 'F=' para%d/OSZICAR"%(i)).readlines())  
                print(icontrol,step)
                if (icontrol < 100) and step == 1:   
                    os.system('cat para%d/allstr.arc >> 1.arc'%(i))    
                    os.system('cat para%d/allfor.arc >> 2.arc'%(i))    

#       for i in range(nstr):
#           if glob.glob('para%d/OSZICAR'%(i+1)):
#               icontrol= int(os.popen('cat para%d/OS* | wc -l'%(i+1)).readline().strip())
#               if(icontrol <  80): 
#                   os.system('cat para%d/allstr.arc >> 1.arc'%(i+1))
#                   os.system('cat para%d/allfor.arc >> 2.arc'%(i+1))
        return

    def screendata(self,strfile,forcefile = False,nmax = 999999):        
        AllStr= allstr_new()
        if forcefile:  
            AllStr.arcinit([0,0],strfile,forcefile)  
        else :
            AllStr.arcinit([0,0],strfile)
        print(len(AllStr))
        # Here can set HighE,MaxAngle,MinAngle
        if len(AllStr)==0: return  
        b=BadStr()
        #   b.HighE=-3.0
        b.MaxFor = self.maxF  
        b.MaxLat = 40
        b.MinLat = 1.6
        #
        AllStr = AllStr.filter(b)   

        if(len(AllStr) > nmax):  
            AllStr.RandomArange(200)  
            AllStr = allstr_new(AllStr[:(nmax)])  

        print('All Str:',len(AllStr))
        #print 'present force',AllStr[0].Lfor
    
        if len(AllStr)==0: return
        # parallel version
#       Ncore= 8 
#       ## remove redundant structure
#       disa, strb = AllStr.ParaShortestBond(Ncore)
#       global poolcount
#       poolcount = poolcount + Ncore    
#       print disa
#       b=sorted(strb)
#       AllStr = AllStr.filter_byset(b)
#       #nmax = 500 
        if(len(AllStr) > nmax):
            AllStr.RandomArange(200)   
            AllStr = allstr_new(AllStr[:(nmax)])
    
        #  AllStr.sortbyE()
    
        print('Final Dump Str:',len(AllStr))  
        if len(AllStr) >0:
            #print('YES')
            AllStr.Gen_arc(range(len(AllStr)),'outstr.arc',2)   
            if AllStr[0].Lfor: AllStr.Gen_Forarc(range(len(AllStr)),'outfor.arc',2)   
    
    def arc2traindata(self):     
        dir = os.path.abspath('.')  #'/home7/zpliu/ZPLPython/carbon-vdw/job0'  
#       base = self.base


        tmpall= allstr_new() 
        tmpall.readfile('%s/outstr.arc'%dir, '%s/outfor.arc'%dir)   
        tmpall.shuffle(200)   
        
        #for str in tmpall: str.addCharge()  
        
        tmpall.genDataStr(range(len(tmpall)),    'TrainStr.txt')
        tmpall.genDataFor(range(len(tmpall)),    'TrainFor.txt')
        return len(tmpall)



class runNNtraining(object):
    def __init__(self,NNdir,cpuperjob,prog):
        self.dir =NNdir
        self.cpuperjob =int(cpuperjob)
        self.prog = prog
        self.maxtime = 3600
        #self.prog='/home7/hsd/program/traincnn-1.0/trainCNN-1.0'

    def sethostfile(self):
        Host=Hostfile(self.dir,self.cpuperjob)
        #self.hostInfo, self.poolsize, totalproc = Host.setHostfile()
        hostdict = Host.setHostfile()
        #if self.cpuperjob ==0:
            #self.cpuperjob = totalproc
        #if self.poolsize != 1:
            #print('unsuitable NN cpuset')

    def run(self,ncycle,nadd,NNstd = False, NNepoch = 2000):
        self.setfile(ncycle,nadd, NNepoch)   
        os.system('rm -rf killsignal')

        #pool = poolshell(self.poolsize)
        exit =False
        alltime =0 
        task_id_list = []
        for i in range(1):
            path=os.path.join(self.dir,'cycle-%d'%ncycle)
            task_id_list.append(runprog_cluster_manual(path))
            os.system('touch iteration1')
            #results.append(pool.apply_async(runprog_cluster_manual,args=('.',self.prog, self.hostInfo,self.cpuperjob,self.dir,os.environ,poolcount)))

        while not exit:
            time.sleep(60)
            alltime= alltime +60
            print('maxtime', self.maxtime)
            #os.chdir(workdir)
            time_task_id = []
            task_info = os.popen('squeue').readlines()    
            #print(task_info)
            for i in range(1,len(task_info)):  
                job_id = task_info[i].split()[0]
                job_user = task_info[i].split()[3]
                if job_user == 'roger':  
                    time_task_id.append(job_id)
                else:
                    continue
            job_nmber=0
            for i in time_task_id:
                if i in task_id_list:
                    job_nmber += 1
            if job_nmber == 0:  
                print('all NN task work calculate finished')
                exit =True
            os.system('cp %s.pot ../%s.pot'%(jobname,jobname)) 
        interation_num=1
        while True:
            time.sleep(60)
            task_id_list = []
            pot_info=open('%s.pot'%jobname,'r')
            pot_info_content=pot_info.readlines()
            for i in pot_info_content:
                if len(i.split()) != 0:
                    if i.split()[0] == 'RMS':
                        rmse_value = float(i.split()[1])
                    else:
                        continue
                else:
                    continue
            if rmse_value < 10.0:
                print('The fitting accuracy of this cycle is up to standard')
                break
            else:
                os.system('cp %s.pot %s.input'%(jobname,jobname))
                os.system("sed -i 's/float  newrun/float  %s.input/g' %s.input"%(jobname,jobname))
                os.system("sed -i 's/calfact.*/calfact 200  15  1  0/g' adjust_factor")
                os.system("sed -i 's/NNepochs.*/NNepochs 10000/g' lasp.in")
                path=os.path.join(self.dir,'cycle-%d'%ncycle)
                task_id_list.append(runprog_cluster_manual(path))
                interation_num += 1
                os.system('touch iteration%d'%interation_num)
                os.system('cp %s.pot %s.pot-iteration%d'%(jobname,jobname,interation_num-1))
                os.system('cp lasp.out lasp.out-iteration%d'%(interation_num-1))
                while True:
                    time.sleep(60)
                    time_task_id=[]
                    task_info = os.popen('squeue').readlines()
                    for i in range(1,len(task_info)):  
                        job_id = task_info[i].split()[0]
                        job_user = task_info[i].split()[3]
                        if job_user == 'roger':  
                            time_task_id.append(job_id)
                        else:
                            continue
                    job_nmber=0
                    for i in time_task_id:
                        if i in task_id_list:
                            job_nmber += 1
                    if job_nmber == 0:  
                        print('all NN task work calculate finished')
                        os.system('cp %s.pot ../%s.pot'%(jobname,jobname))
                        break
                    
#           if glob.glob('killsignal'):
#               sendkillsignal(['.'])
#               print 'External signal: will be terminated in few sceonds'
#               time.sleep(60)
#               exit=True
#           process_count=len(pool._cache)
#           if process_count ==0:
#               print 'all work done'
#               exit=True
#           if NNstd:
#               try:
#                   MAXinfo=os.popen('grep MAX hTrainOutput | tail -1').readline().split()
#                   maxE = float(MAXinfo[3])
#                   maxF = float(MAXinfo[5])
#                   RMSinfo=os.popen('grep RMS hTrainOutput | tail -1').readline().split()
#                   rmsE = float(RMSinfo[3])
#                   rmsF = float(RMSinfo[5])
#
#                   if ((maxE < NNstd['maxE']) and (maxF < NNstd['maxF']) and \
#                       (rmsE < NNstd['rmsE']) and (rmsF < NNstd['rmsF'])):
#                       sendkillsignal(['.'])
#                       print 'terminate: has reached NN std'
#                       time.sleep(60)
#                       exit=True
#               except:
#                   continue
#           #if glob.glob('terminatesignal'):
#           #    print 'forced termination of pool'
#           #    exit=True
#           #    pool.terminate()
#           #    time.sleep(60)
#
#
#
#       process_count=len(pool._cache)
#       if (exit) and (process_count!=0):
#           time.sleep(60)
#           process_count=len(pool._cache)
#           if process_count!=0:
#               sendkillsignal(['.'])
#               time.sleep(60)
#               print 'forced termination of pool'
#               pool.terminate()
#
#
#
#       pool.close()
#       pool.join()


    def setfile(self,ncycle,nadd, NNepoch):   
        os.chdir(self.dir)
        os.mkdir('cycle-%d'%ncycle)
        if ncycle == 1:
            pass
        else:
            os.system('cp %s.pot %s.input'%(jobname,jobname))   
            #os.system('cp %s.pot cycle-%d'%(jobname,ncycle))
            os.system("sed -i 's/float  newrun/float  %s.input/g' %s.input"%(jobname,jobname))
            os.system('cp %s.input cycle-%d'%(jobname,ncycle))
            #sed -i 's/float  newrun/float  H2O.input/g' H2O.pot
        #os.system('cp ../lasp.slurm ./')
        #os.system("sed -i 's/#PBS -q.*/#PBS -q PE/g' lasp.pbs")    
        #os.system("sed -i 's/#PBS -l node.*/#PBS -l nodes=6:ppn=24/g' lasp.pbs")
        #os.system("sed -i 's/#SBATCH -N 1/#SBATCH -N 4/g' lasp.slurm")
        #os.system("sed -i 's/#SBATCH -n*/#SBATCH -n 256/g' lasp.slurm")
        os.system('cp lasp.slurm cycle-%d'%(ncycle))
        os.system("sed -i 's/calfact.*/calfact 10  2000  1  0/g' adjust_factor")
        os.system('cp adjust_factor cycle-%d'%(ncycle))
        os.system('cp TrainFor.txt cycle-%d'%(ncycle))
        os.system('cp TrainStr.txt cycle-%d'%(ncycle))
        #os.system('mv lasp.out cycle-%d'%(ncycle))
        #os.system('mv SavePot/ cycle-%d'%(ncycle))
        os.system("sed -i 's/NNepochs.*/NNepochs 10000/g' lasp.in")

        #self.nstr = self.nstr + nadd
        nBad = int(len(os.popen('grep Energy TrainStr.txt').readlines()))
        print(nBad)
        os.system("sed -i 's/Ntrain.*/Ntrain  %d/g' lasp.in"%nBad)
        os.system('cp lasp.in cycle-%d'%(ncycle))


class runNNvalidation(object):
    def __init__(self,NNdir,cpuperjob,prog):
        self.dir =NNdir
        self.cpuperjob =int(cpuperjob)
        self.prog = prog
        self.maxtime = 3600
    
    def sethostfile(self):
        Host=Hostfile(self.dir,self.cpuperjob)
        hostdict = Host.setHostfile()
        


def collectallstr(workdir, nbadstr):
    #print('ssh %s "python %s/nodejob.py %s/%s %d" '%(procname, os.getcwd(),os.getcwd(),workdir, nbadstr))
    #os.system ('ssh %s "python %s/nodejob.py %s/%s %d" '%(procname, os.getcwd(),os.getcwd(),workdir, nbadstr))
    #print('python %s/nodejob.py %s/%s %d '%(os.getcwd(),os.getcwd(),workdir, nbadstr))
    #os.system ('python %s/nodejob.py %s/%s %d '%(os.getcwd(),os.getcwd(),workdir, nbadstr))    
    AllStr= allstr_new()
    if glob.glob('%s/allstr.arc'%(workdir)):
        AllStr.arcinit([0,0],'%s/allstr.arc'%(workdir)) #, '%s/allfor.arc'%(workdirs[i]))  
        if (len(AllStr)== 0): 
            return
        b=BadStr()
        b.MaxFor = 600
        b.MaxLat = 50
        AllStr = AllStr.filter(b)   
        if (len(AllStr)== 0): 
            return
        AllStr.RandomArange(200)
        AllStr = allstr_new(AllStr[:nbadstr])  
        AllStr.Gen_arc(range(len(AllStr)),'%s/outstr.arc'%workdir,2)   
    
    AllStr= allstr_new()
    if glob.glob('%s/allslab.arc'%(workdir)):
        AllStr.arcinit([0,0],'%s/allslab.arc'%(workdir)) #, '%s/allfor.arc'%(workdirs[i]))
        if (len(AllStr)== 0): 
            return
        AllStr = AllStr.filter(b)
        AllStr=AllStr.sortbyE()
        AllStr = allstr_new(AllStr[:1])
        AllStr.Gen_arc(range(len(AllStr)),'%s/outstr-1.arc'%workdir,2)
        os.system('cat %s/outstr-1.arc >> %s/outstr.arc'%(workdir,workdir))

    AllStr= allstr_new()
    if glob.glob('%s/best.arc'%(workdir)):
        AllStr.arcinit([0,0],'%s/best.arc'%(workdir)) #, '%s/allfor.arc'%(workdirs[i]))
        if (len(AllStr)== 0): 
            return
        AllStr = AllStr.filter(b)
        AllStr=AllStr.sortbyE()
        AllStr = allstr_new(AllStr[:1])
        AllStr.Gen_arc(range(len(AllStr)),'%s/outstr-1.arc'%workdir,2)
        os.system('cat %s/outstr-1.arc >> %s/outstr.arc'%(workdir,workdir))

        

def getjobinfo():   
    #print(self.dir)
    #os.chdir(self.dir)
    #line = os.popen('grep Jobname NNinput').readline().split()
    #self.jobname = line[-1]
    f = open(r'console','r')
    lines=f.readlines()
    #while line:
    #if len(line.split()) == 0:
        #line=f.readline()
        #continue
    for i in lines:
        if len(i.strip().split()) == 0:
            continue
        elif i.strip().split()[0]=='Jobname':
            jobname = i.strip().split()[1]
        else:
            continue
        '''elif line.split()[0]=='Ntrain':
            self.nstr= int(line.split()[1])
        elif line.split()[0] =='%block':
            blockname = line.split()[-1]
            autobase={}
            blockline=f.readline().split()
            while blockline[0] != '%endblock':
                autobase[blockline[0]]= 0.0
                blockline=f.readline().split()
            #print(autobase)
        line=f.readline()'''
    f.close()
    return jobname


def poolshell(poolsize):
    pool = Pool(processes=poolsize)
    return pool

def readpara():
    f= open(r'console','r')
    para ={'Nbad':200,'maxF':100,'maxSSWtime':99999,'maxVASPtime':99999,\
            'maxtimeperVASP':99999,'maxcycle':99999,'masternode':0}
    line=f.readline()
    while line:
        if len(line.split()) == 0:
            line=f.readline()
            continue
        elif line.split()[0]=='Nbad':
            para['Nbad'] = int(line.split()[1])
        elif line.split()[0]=='maxF':
            para['maxF'] = int(line.split()[1])
        elif line.split()[0]=='maxSSWtime':
            para['maxSSWtime']= int(line.split()[1])
        elif line.split()[0] =='cyclecontrol':
            para['maxcycle']= int(line.split()[1])
        elif line.split()[0] == 'maxVASPtime':
            para['maxVASPtime']=int(line.split()[1])
        elif line.split()[0] == 'maxtimeperVASP':
            para['maxtimeperVASP']=int(line.split()[1])
        elif line.split()[0] == 'SSWprog':
            para['SSWprog']= line.split()[1]
        elif line.split()[0] == 'VASPprog':
            para['VASPprog']= line.split()[1]
        elif line.split()[0] == 'NNprog':
            para['NNprog']= line.split()[1]
        elif line.split()[0] == 'SSWcpu':
            para['SSWcpu'] =int(line.split()[1])
        elif line.split()[0] == 'VASPcpu':
            para['VASPcpu'] =int(line.split()[1])
        elif line.split()[0] =='masternode':
            para['masternode'] = int(line.split()[1])
        elif line.split()[0] =='maxSSWpara':
            para['maxSSWpara'] = int(line.split()[1])
        elif line.split()[0] =='Allstr':
            para['Allstr'] = int(line.split()[1])
        elif line.split()[0] =='cpupernode':
            para['cpupernode'] = int(line.split()[1])
        elif line.split()[0] == 'NNepoch' :
            para['NNepoch'] = int(line.split()[1])
        elif line.split()[0] == 'StartfromVASP' :
            para['StartfromVASP'] = int(line.split()[1])
        elif line.split()[0] == 'SSWcheckcycle' :
            para['SSWcheckcycle'] = int(line.split()[1])
        

        elif line.split()[0] =='%block':  
            blockname = line.split()[-1]
            lines= []
            blockline=f.readline().split()
            while blockline[0] != '%endblock':
                lines.append(blockline)
                blockline=f.readline().split()
            para[blockname]=readblock(lines)
        line=f.readline()
    f.close()
    return para

def readblock(lines):  
    dict = {}
    for line in lines:
        try:
            dict[line[0]]= float(line[1])  
            if dict[line[0]].is_integer():
                dict[line[0]]=int(dict[line[0]])
        except:
            dict[line[0]]= line[1]
    return dict


def sendkillsignal(workdirs):
    for i in range(len(workdirs)):
        os.system('echo kill > %s/killsignal'%(workdirs[i]))
    return


if __name__ == "__main__":
    time_start = time.time()
    newstart = 1  
    global para  
    para = readpara()   
    print('para',para)   
    #print(para['masternode'])
    
    global jobname
    jobname = getjobinfo()   
    print('jobname',jobname)
    
    rootdir = os.getcwd()  
    #print(rootdir)
    if not glob.glob('SSW/sourcedir'):   
        print('not find SSW file')
        sys.exit()
    if not glob.glob('VASP/sourcedir'):
        print('not find vasp file')
        sys.exit()
    if not glob.glob('NN'):
        print('not find training file')
        sys.exit()    
    SSWdir=os.path.join(rootdir,'SSW')
    #print(SSWdir)
    VASPdir=os.path.join(rootdir,'VASP')
    #print(VASPdir)
    NNdir=os.path.join(rootdir,'NN')    
    #print(NNdir) 
    os.chdir(rootdir)
    #if(newstart == 1):
        #os.system('rm -rf SSW/SSW*')   
        #os.system('rm -rf VASP/cycle-*')
        #os.system('rm -rf NN/cycle-*')    
    SSW =runssw(SSWdir,para['cpuperjob']['SSW'],para['prog']['SSW'],para['masternode'])   
    totalnodes =SSW.sethostfile()   
    print('totalnodes_number',len(totalnodes))

    VASP =runvasp(VASPdir,para['cpuperjob']['VASP'],para['prog']['VASP'],para['masternode'])
    #VASP.sethostfile()   

    NN =runNNtraining(NNdir,para['cpuperjob']['NN'],para['prog']['NN'])
    #NN.sethostfile()  

    #print(totalnodes)     
    #totalnodes_number=len(totalnodes['PB'])+len(totalnodes['PC'])+len(totalnodes['PD'])+len(totalnodes['PE'])+len(totalnodes['PF'])
    #print('totalnodes_number',totalnodes_number)

    #global poolcount
    #poolcount =0    
    #print(para['cpuperjob']['SSW'])
    SSWpara = para['maxSSWpara']   
    print('SSWpara',para['maxSSWpara'])
    #PB_number=len(totalnodes['PB']);PC_number=len(totalnodes['PC']);PD_number=len(totalnodes['PD']);PE_number=len(totalnodes['PE']);PF_number=len(totalnodes['PF'])
    #print(para['maxSSWpara'])
    #print(totalproc/para['cpuperjob']['SSW'])
    #cycle_list = []
    #cycle_list=[i for i in range(100)]
    cycle_list=[20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
    if (para['StartfromVASP'] == 0):
        startcycle = 1   
        for i in cycle_list:
            icycle = startcycle + i
            #print(rootdir)
            os.chdir(rootdir)
            #if icycle%2 == 0:
                #AllStr0= allstr_new()  
                #AllStr0.arcinit([0,0],'./SSW/sourcedir/Badstr.arc-%d'%(icycle-1))
                #SSWpara=int(len(AllStr0))  
            #else:
            AllStr0= allstr_new()  
            AllStr0.arcinit([0,0],'./SSW/sourcedir/allstr-ini.arc')
            SSWpara=int(len(AllStr0)) 
            print(SSWpara)
            #para = readpara()
            #print(para['maxcycle'])   #para['maxcycle']
            if icycle> para['maxcycle'] : break   
            print(' ')
            print('-------------------------->   Start cycle %d   <--------------------------'%icycle)
            print(' ')
            #print(para)
            print(' ')
            print('==========================start SSW sampling=============================')
            #print(SSWpara)
            #print(icycle)
            #print(para['Nbad'])
            #print(para['maxSSWtime'])
            #print(para['Allstr'])
            #print(para['SSWcheckcycle'])
            nbadcol = SSW.run(SSWpara,icycle,para['Nbad'],para['maxSSWtime'], para['Allstr'],para['SSWcheckcycle'])  #SSWpara
            #nbadcol = 1
            print('sswnbadcol',nbadcol)
            #poolcount=poolcount+ SSW.poolsize  #SSW.poolsize
            #print('poolcount',poolcount)
            #print('SSW.poolsize',SSW.poolsize)
            print('icycle',icycle)
            print("para['Nbad']",para['Nbad'])
            print("para['Allstr']",para['Allstr'])
            print("para['NNstd']",para['NNstd'])
            print("para['NNepoch']",para['NNepoch'])
            if(nbadcol >0):
                print('==========================start VASP calculation=========================')
                nadd = VASP.run(icycle,para['Nbad'],para['maxF'],para['maxVASPtime'],para['maxtimeperVASP'], para['Allstr'])
                print('vaspnadd', nadd)
                #nadd=100
                print('===========================start NN training=============================')
                NN.run(icycle, nadd, para['NNstd'],para['NNepoch'])
            time.sleep(5)
    print('auto-train end')    
    time_end = time.time()
    print('total time', time_end-time_start)
