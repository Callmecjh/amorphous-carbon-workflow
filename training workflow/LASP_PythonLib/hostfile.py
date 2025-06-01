
import os
import time
import multiprocessing
from multiprocessing import Pool
import glob
import traceback
import subprocess


class Hostfile(object):
    def __init__(self,workdir,cpuperjob,setmasternode= 0):
        self.workdir = workdir
        self.cpuperjob = cpuperjob   
        self.setmasternode = setmasternode

    def setHostfile(self):
        hostDict = self.getProc()  #hostDict格式字典 {node1:64,node2:64} 机器名：节点数
        #print(hostDict)
        #divHost,totalproc = self.alloProc(hostDict,self.cpuperjob)   #cpuperjob是每个任务的核心数，这里设置是20，就是传入的size
        #print(divHost)
        # get the pool size 
        #poolsize= len(divHost)  #换算回来就是等于多少个任务了 
        #print(poolsize)
        # dump the hostfiles 主机信息存入文件内
        #self.hostInfo =self.dumpHost(divHost)
        #print('self.hostInfo',self.hostInfo)  #所有的主机信息
        #print('poolsize',poolsize)
        #print('totalproc',totalproc)
        print(hostDict)
        return hostDict   

    def getProc(self):   #得到目前集群内空闲的所有机器信息
        hostdict = {}
        #print(self.setmasternode)
        if self.setmasternode != 0:
            first = True
            #print('set masternode')
        else:
            first = False
        # get environment variable of host file list in group cluster 得到集群内可用的机器的信息
        #print(os.environ)
        #hostfile = os.environ.get() #['scontrol show node'] 
        hostfile_info = os.popen('sinfo').readlines()
        fp_info = open('hostfile',"w")
        for i in hostfile_info:
            fp_info.write(str(i))
        fp_info.close()
        fp = open(r'hostfile',"r")
        contents = fp.readlines()
        #print(contents)
        for x in contents:
            list1=x.strip().split()
            #print(list1[0],list1[4])
            if list1[0] == 'lasp':    #队列要相应修改
                if list1[4] == 'idle':                    
                    jiqi_nodes = x.split()[5]
                    all_number_1 = jiqi_nodes.split('[')[1]
                    all_number_2 = [all_number_1.split(']')[0]]                   
                    all_number_3 = all_number_2[0].split(',')
                    #print(all_number_3)
                    for i in all_number_3:
                        #print(i)
                        if len(i.split('-')) == 2:
                            #print(i.split('-'))
                            for j in range(int(i.split('-')[0]),int(i.split('-')[1])+1):
                                hostdict['node'+str(j)]=64
                        elif len(i.split('-')) == 1:
                            hostdict['node'+str(i)]=64   #每台机器64个核
                else:
                    continue
            else:
                continue                       
        os.system('rm -r hostfile')
        fp.close()
        '''#the following part are designed for fudannhpcc system
        hostfile = os.environ["PBS_NODEFILE"]
        print(hostfile)
        fp = open(hostfile,"r")
        for x in fp:
            if first:
                masternode = x.split()[0]
                first= False
                continue
            line = x.split()
            hostdict[line[0]] = 12 #int(line[1]) zpliu
        fp.close()
        if self.setmasternode: 
            hostdict.pop(masternode)'''
        return hostdict

    # chuck the list  列表分块
    def chunks(self,arr, n):   #这里的n就是每个任务的核心数
        all = len(arr)-len(arr)%n  #等于0
        return [tuple(arr[i:i+n]) for i in range(0, all, n)]  #根据核心数来得到多少个任务



    def alloProc(self,hostdict,size=1):   #总的可用的节点数
        # construct a list of possible hosts
        totProc = 0
        hostList = []
        for key,val in hostdict.items():
            totProc += val  #所有节点数,单个数
            hostList.extend([key]*val)  #host的列表 [node3, node3, node3,....]

        print("Availiable proc number: ",totProc)
        print("Availiable nodes number: ",int(totProc/64))
        if size ==0:
            size = totProc
        return self.chunks(hostList,size),totProc


    # dump hosts info into files
    # return a list of file names and corresponding host number

    def dumpHost(self,divHost):
        os.chdir(self.workdir)
        hostInfo = []
        ft = open(".hostfile", "w")  #这里创建的是隐藏文件
        for i,record in enumerate(divHost):
            fn = ".hostfile_%03d" %i
            fp = open(fn,"w")
            for line in record:
                fp.write(line+"\n")
                ft.write(line+"\n")
            fp.close()
            # why plus one ? in fact, I don't know either
            hostInfo.append((fn, len(set(record))))
        ft.close()
        return hostInfo



def runprog_local(workdir, prog, ncpus):
    try:
        os.chdir(workdir)
        mpiprog = "mpirun -np %d "%(ncpus) + prog
        fout = open('output','w')
        subprocess.call(mpiprog,stdout = fout, stderr=fout,shell=True,executable='/bin/bash')
        fout.close()
        return
    except Exception as e:
        traceback.print_exc()
        raise e
    except:
        print('error')
        return 


def runprog_cluster(workdir,prog,ncpus,hostInfo,rootdir,env,poolcount = 0):

    try:
        os.chdir(rootdir)
        cwd = os.getcwd()
        exit = False
        #print multiprocessing.current_process().name
        nodeInfo = hostInfo[int(multiprocessing.current_process().name.split("-")[-1])-1-poolcount]
        os.chdir(workdir)
        mf = os.path.join(cwd,nodeInfo[0])
        #mpiprog = "/home/software/mpi/intel/impi/4.0.1.007/bin64/mpirun --rsh=ssh -machinefile %s -np %d "%(mf, ncpus) + prog
        mpiprog = "mpirun -r ssh -machinefile %s -np %d "%(mf, ncpus) + prog
        fout1 = open("proginfo","w")
        fout1.write("Current process: "+ multiprocessing.current_process().name +"\n")
        fout1.write("Host file: " + mf + "\n")
        fout = open('output','w')
        #totalrun = 'source ~/.bashrc; '+ mpiprog
        totalrun = mpiprog
        #nodename = os.popen('head -1 %s'%mf).readline().strip()
        #totalrun = 'source ~/.bashrc; ssh '+nodename +"; "+mpiprog
        fout1.write(totalrun+"\n")
        fout1.close()
        #child= subprocess.Popen(mpiprog,stdout = fout, stderr=fout,shell=True,executable='/bin/bash',preexec_fn = os.setpgrp)
        subprocess.call(mpiprog,stdout = fout, stderr=fout,shell=True,executable='/bin/bash')
        fout.close()
        return
    except Exception as e:
        traceback.print_exc()
        raise e
    except:
        print('error')
        return


def runprog_cluster_manual(workdir):
    '''os.chdir(workdir)
    fout1 = open("proginfo","w")
    fout1.write("Current process: " +"\n")
    fout1.write("Host file: "  + "\n")
    print(rootdir)   #/home/roger/SSW-NN-autotrain/SSW
    print(hostInfo)
    cwd = os.getcwd()  #/home/roger/SSW-NN-autotrain/SSW/SSW-1-0
    print(cwd)'''
    #print(hostInfo)
    #os.chdir(rootdir)
    #print(rootdir)
    #cwd = os.getcwd()
    #print(cwd)
    #exit = False
    os.chdir(workdir)
    #print(workdir)
    task = os.popen('sbatch lasp.slurm').readlines()
    #print(task)
    task_id = str(task[0].split()[-1])
    #print(task_id)
    return task_id
    #os.system('sbatch lasp.slurm')
    '''try:
        print(hostInfo)
        os.chdir(rootdir)
        print(rootdir)
        cwd = os.getcwd()
        print(cwd)
        exit = False
        os.chdir(workdir)
        os.system('sbatch lasp.slurm')
        print(multiprocessing.current_process().name)
        #nodeInfo = hostInfo[int(multiprocessing.current_process().name.split("-")[-1])-1-poolcount]
        nodeInfo = hostInfo[jobnumber][0]
        print(nodeInfo)
        os.chdir(workdir)
        mf = os.path.join(cwd,nodeInfo)
        print(mf)
        #mpiprog = "/opt/intel/impi/5.0.2.044/intel64/bin/mpirun -machinefile %s -np %d "%(mf, ncpus) + prog
        #mpiprog = "mpirun -machinefile %s -env I_MPI_DEVICE rdma:OpenIB-cma -np %d "%(mf, ncpus) + prog
#        mpiprog = "source /home2/shang/.bashrc; mpirun -machinefile %s -np %d "%(mf, ncpus) + prog
        #mpiprog = " mpirun  -rsh=ssh -machinefile %s -np %d "%(mf, ncpus) + prog
        #mpiprog = " srun -n %d "%(ncpus) + prog
        mpiprog = "mpirun -genv I_MPI_FABRICS=shm:ofi -machinefile hostfile -np %d "%(ncpus) + prog
#       mpiprog = "mpirun -machinefile %s -np %d "%(mf, ncpus) + prog
        fout1 = open("proginfo","w")
        #fout1.write("Current process: "+ multiprocessing.current_process().name +"\n")  # Current process: PoolWorker-1
        fout1.write("Current process: Current process: PoolWorker-"+ str(jobnumber) +"\n")
        fout1.write("Host file: " + mf + "\n")
        fout = open('output','w')
        #totalrun = 'source ~/.bashrc; '+ mpiprog
        totalrun = mpiprog
        #nodename = os.popen('head -1 %s'%mf).readline().strip()
        #totalrun = 'source ~/.bashrc; ssh '+nodename +"; "+mpiprog
        fout1.write(totalrun+"\n")
        child= subprocess.Popen(mpiprog,stdout = fout, stderr=fout,shell=True,executable='/bin/bash',preexec_fn = os.setpgrp)
        print(child)
        print ('start run job in %s'%workdir)
        fout1.write('pid   %d\n'%child.pid)
        fout1.close()
        pid =child.pid
        if maxtime:
            alltime = 0
        while not exit:
            time.sleep(30)
            returnCode= child.poll()
            if glob.glob('killsignal'):
                os.kill(-pid,9)
                time.sleep(3)
                fout.write('kill %s\n'%pid)
                a=os.waitpid(pid,0)
                print(a)
                time.sleep(3)
                exit =True
            if isinstance(returnCode,int):
                if returnCode == 0:
                    fout.write('successfully done\n')
                else:
                    fout.write('something wrong: returnCode  %d\n'%returnCode)
                exit =True
            if maxtime:
                alltime = alltime+30
                if alltime >maxtime:
                    os.kill(-pid,9)
                    os.system('pkill -9 %s'%prog)
                    time.sleep(3)
                    fout.write('time out :kill %s\n'%pid)
                    a=os.waitpid(pid,0)
                    print(a)
                    time.sleep(3)
                    exit =True

        #fout1.write(str(child.poll())+'\n')
        fout.write('exit\n')
        fout.close()
        return
    except Exception as e:
        traceback.print_exc()
        raise e'''



if __name__ == "__main__":
    #pass
    Host = Hostfile(rootdir,ncpu,0)
    hostInfo,poolsize,totalproc= Host.setHostfile()


