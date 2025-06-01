
from allstr_new import allstr
from structure_new import Str
import numpy as np
import hashlib
import zlib
import ctypes
from ctypes import pointer
from multiprocessing import Pool
#from babelfunc import *


def wrapGenECFPname(datain):
    str,savefp = datain
    #print str.sminame
    ECFPname,FP = str.GenECFPname()
    if savefp:
        return ECFPname,FP
    else:
        return ECFPname

def one_of_k_encoding(x, allowable_set):
    if x not in allowable_set:
        raise Exception("input {0} not in allowable set{1}:".format(x, allowable_set))
    return map(lambda s: x == s, allowable_set)

def one_of_k_encoding_unk(x, allowable_set):
    """Maps inputs not in the allowable set to the last element."""
    if x not in allowable_set:
        x = allowable_set[-1]
    return map(lambda s: x == s, allowable_set)


class SurfaceStr(Str):
    def GenFeature(self):
        self.AddAtomID()
        self.GetAtomInfo()
        for iatom,atom in enumerate(self.atom):
            atom.surface = self.surfaceatom[iatom]
            atom.surfacemetal = self.atom[-1].elesymbol
            atom.feature = self.Atom_Features(atom)

        self.NeighbourList()

    def Atom_Features(self,atom):
        return np.array(one_of_k_encoding_unk(atom.elesymbol,['C', 'O', 'H','N', 'Cu','Pt', 'Unknown']) +
        #return np.array(one_of_k_encoding_unk(atom.elesymbol,['C', 'O', 'H', 'Cu', 'Unknown']) +
                    one_of_k_encoding_unk(atom.expbond, [0, 1, 2, 3, 4, 5,6,7,8,9,10,11,12,'Unknown']) +
                    one_of_k_encoding_unk(atom.imph, [0, 1, 2, 3, 4, 5,'Unknown'])+
                    one_of_k_encoding_unk(atom.surfacemetal, ['Cu','Pt','Unknown'])+
                    #one_of_k_encoding_unk(atom.value, [-2, -1, 0, 1, 2, 3])+
                    #one_of_k_encoding_unk(atom.surface, ['single', 'bridge','hcp', 'fcc','4','unkonwn'])+
                    [0])


    def Bond_Features(self,bondorder):
        return np.array(one_of_k_encoding(bondorder,[1,2,3,4,5]))

#    def GetNeighbour(self,iatom):
#        for i in range(self.natom):
#            if self.bmx2D[iatom][i]>0:
#                self.atom[iatom].neighbour.append()
#


    def NeighbourList(self):
        for i in range(self.natom):
            self.atom[i].nbatom=[]
            self.atom[i].bond=[]
            self.atom[i].nb=[]

        for i in range(self.natom):
            for j in xrange(i+1,self.natom):
                if self.bmx2D[i][j]>0:
                    # do i need skip H?
                    self.atom[j].nbatom.append(self.atom[i])
                    self.atom[i].nbatom.append(self.atom[j])
                    #self.atom[j].bond.append(self.Bond_Features(self.bmx2D[i][j]))
                    #self.atom[i].bond.append(self.Bond_Features(self.bmx2D[i][j]))
                    self.atom[j].nb.append([self.bmx2D[i][j],i])
                    self.atom[i].nb.append([self.bmx2D[i][j],j])

    def SortbyDegree(self,):
        self.atom.sort(key = lambda x:len(x.neighbour))

    def AllAtomFeature(self):
        atomfeature = []
        for atom in self.atom:
            atomfeature.append(atom.feature)
            atomfeature.append(atom.bond)
      
    def AllBondFeature(self):
        atomfeature = []
        for atom in self.atom:
            for bond in atom.bond:
                bondfeature.append(bond)
                bondfeature.append(bond)

    def GenECFPname(self,depth=3,dim=10000000,savefp = False):
        FP = ECFP(self,depth,dim)
        FP.GenECFP()
        string = ''
        for index in FP.allindex:
            #print index
            string = string + str(len(FP.IndextoFp[index]))
            string = string+ str(index)
        self.ECFPname= string
        if savefp:
            self.FP = FP
        
        #print self.ECFPname
        return string,FP

    def CheckMin(self,flag = 1):
        sqnatm = self.natom**2

        self.calCtypes()
        program='/home7/kpl/pymodule/Lib/Lib_fillbond_new/checkminbond.so'
        #program='/home7/kpl/pymodule/Lib/Lib_fillbond/checkminbond.so'
        Lminstr = pointer(ctypes.c_bool(0))
        bmatrix = pointer((ctypes.c_int*sqnatm)(*[0 for i in range(sqnatm)]))
        bondneed = pointer((ctypes.c_int*(self.natom))(*[0 for i in range(self.natom)]))
        surface = pointer((ctypes.c_int*(self.natom))(*[0 for i in range(self.natom)]))

        checkmin = ctypes.cdll.LoadLibrary(program)
        if flag == 0:
            checkmin.judgebond_(self.c_natm,self.c_iza,self.c_xa,self.c_rv,Lminstr,bmatrix,bondneed)
        elif flag ==1 :
            #print 'into surface'
            checkmin.judgebondsurface_(self.c_natm,self.c_iza,self.c_xa,self.c_rv,Lminstr,bmatrix,bondneed,surface)
            #print 'finish fffffffffffffff'

        bmx = list(bmatrix.contents)
        #self.bmx2D = np.array(bmx).reshape(self.natom, self.natom)
        #self.bmx1D = bmx

        self.bondneed = list(bondneed.contents)
        self.Lminstr = bool(Lminstr.contents)
        return self.Lminstr,bmx,list(bondneed.contents),list(surface.contents)


class AllStr(allstr):
    def readfile(self,inputfile, forcefile=False, allformat = 0):
        f= open(inputfile,'r')
        currentStr = -1
        for line in f:
            if ('Energy' in line\
                or 'React' in line\
                or 'TS' in line\
                or 'SSW-Crystl' in line\
                or 'Str' in line):
                self.append(SurfaceStr())
                currentStr +=  1
                self[currentStr].Lfor = False
                try:
                    self[currentStr].energy = float(line.split()[-1])
                    try :
                        self[currentStr].maxFF = float(item.split()[-2])
                    except :
                        self[currentStr].maxFF = 0

                    if self[currentStr].energy.is_integer():
                        self[currentStr].energy = float(line.split()[-2])
                except:
                    self[currentStr].energy = float(line.split()[-2])
                    self[currentStr].maxFF = 0
            elif 'CORE' in line:
                self[currentStr].addatom(line,1 )
            elif ('PBC' in line )and ('ON' not in line):
                self[currentStr].abc= [float(x) for x in line.split()[1:]]
        f.close()
        for str in self:
            str.sortatombyele()
            str.calAtomnum()
            str.abc2lat()

        if forcefile:
            f = open(forcefile,'r')
            currentStr= -1
            for line in f:
                if "For" in line:
                    self[currentStr].Lfor = True
                    currentStr += 1
                    iatom = 0
                    for atom in self[currentStr].atom: atom.force = [0.0, 0.0, 0.0]
                elif len(line.split()) == 6:
                    self[currentStr].addStress(line)
                elif len(line.split()) == 3:
                    if "****" not in line: self[currentStr].addForce(line, iatom)
                    else:                  self[currentStr].addForce('0.0 0.0 0.0', iatom)
                    iatom += 1

        if allformat:
            for str in self:
                str.TransferToXYZcoordStr()

 
    def GetAllECFPname(self, numproc=24,savefp = False):
        _tmp = []
        for Str in self:
            _tmp.append((Str,savefp))

        pool = Pool(processes=numproc)
        result = pool.map_async(wrapGenECFPname, _tmp)
        pool.close(); pool.join()

        for Str,r in zip(self,result.get()):
            if savefp:
                Str.ECFPname = r[0]
                Str.FP = r[1]
            else:
                Str.ECFPname = r

    def GetTmpFakebmx(self,numproc=24,flag =2,colorflag =  1):
        if flag == 1:
            self.calAllBondMatrix(numproc=numproc)
        if flag == 2:
            self.calAllFakeBondMaxtrix(numproc=numproc)
        self.calAllSegmolecular (numproc=numproc)

    def GetAllsminame_fromreactstr(self,numproc=24,flag =2,colorflag =  1):
        for Str in self:
            Str.RemoveMetalBond()
        self.calAllSegmolecular (numproc=numproc)

        allgroup = []
        for str in self:
            substr = [[] for i in np.unique(str.group)]
            for id,atom in enumerate(str.atom):
                atom.id = id
                substr[str.group[id]-1].append(atom)
            substr = sorted(substr, key=lambda x:calmass(x), reverse=True)
            if flag == 1: allgroup.append((substr, str.bmx2D, str.lat,[],1,[]))
            if flag == 2: allgroup.append((substr, str.bmx2D, str.lat,str.bondneed,2,str.surfaceatom))
            #print str.bondneed

        pool = Pool(processes=numproc)
        result = pool.map_async(calAllName, allgroup)
        pool.close(); pool.join()

        for istr,(str,re) in enumerate(zip(self,result.get())):
            str.allmol = re
            str.id     = istr

        for str in self:
            if colorflag:
                str.sminame, strflag = glueSegStr(str.allmol)
            else:
                str.sminame, strflag = glueSegStr_pure(str.allmol)

        for Str in self:
            Str.bmx2D = Str.bmxsave

class singlefp(object):
    def __init__(self):
        self.index = 0
        self.neighbour= []
        self.allatom = []
        self.trace = []
        self.save = 1
        self.coreele = 0
        self.coreid = 0

    def Inherit(self,parent):
        self.index = parent.index
        self.allatom = parent.allatom[:]
        self.trace = parent.trace[:]
        self.coreele = parent.coreele
        self.coreid = parent.coreid

    def genidentifier(self,dim=10000000):
        self.neighbour.sort(key= lambda x:x[0])
        
        #if self.coreele == 29:
        #    print len(self.neighbour)

        for nb in self.neighbour:
            self.trace.append(nb[1])

        self.allatom.sort()
        self.allatomset = np.unique(self.allatom)

        tmpall= [(1,self.index)]
        for nb in self.neighbour:
            tmpall.append(nb[0])
            #print nb[0]
            #tmpall.append(nb[0][0])
            #tmpall.append(nb[0][1])
        self.index = hashlist(tmpall,dim)

        #string = '1:%s'(%self.index)
        #for item in self.neighbour:
        #    string = string+ str(item)
        


class ECFP(object):
    def __init__(self,structure, nlayer, dim=10000000):
        self.str = structure
        self.nlayer = nlayer
        self.allfp = []
        self.dim = dim

#    def PreparebyLayer(self):
#        for atom in self.str.atom:
#            atom.layeratom = {}
#            atom.layeratom[0] = [atom]
#
#        neighbourdict = {}
#        for ilayer in range(nlayer):
#            atom.layeratom[ilayer+1] = []
#            for iatom,atom in enumerate(self.str.atom):
#                #neighbourdict[(iatom,ilayer)] = []
#                for subatom in atom.layeratom[ilayer]:
#                    #neighbourdict[(iatom,ilayer)].append(subatom.id)
#                    for inb,newatom in enumerate(subatom.neighbour):
#                        atom.layeratom[ilayer+1].append(newatom)
#                        self.cyclenb[(iatom,ilayer+1)].append([subatom.bond[inb],newatom.id])

    def GenECFP(self):
        self.InitIdentifier()
        for ilayer in xrange(1,self.nlayer):
            self.UpdateLayer(ilayer)
        allindex = []
        for fp in self.allfp:
            allindex.append(fp.index)
        allindex.sort()
        self.allindex  = np.unique(allindex)
        #self.allindex,self.allindexconut =list(np.unique(allindex,return_counts=True))
        self.GenDict()
        return

    def GenDict(self):
        AtomsettoIndex = {}
        IndextoAtomset = {}
        IndextoFp = {}
        for fp in self.allfp:
            #AtomsettoIndex[set(fp.allatomset)] = fp.index
            IndextoAtomset[fp.index] = fp.allatomset
            if fp.index not in IndextoFp.keys():
                IndextoFp[fp.index] = [fp]
            else:
                IndextoFp[fp.index].append(fp)

        self.IndextoAtomset = IndextoAtomset
        self.IndextoFp = IndextoFp


    def InitIdentifier(self):
        self.str.GenFeature()
        self.genbylayer=[[0 for x in range(self.str.natom)]]
        for iatom,atom in enumerate(self.str.atom):
            newfp= singlefp()
            newfp.allatom.append(atom.id)
            newfp.trace.append(atom.id)
            newfp.coreele = atom.ele
            newfp.coreid = iatom
            #print atom.feature
            newfp.index =hashlist(atom.feature,self.dim)
            #print newfp.index
            #print newfp.index
            newfp.allatom.sort()
            newfp.allatomset = np.unique(newfp.allatom)
            #newfplist.append(newfp)
            self.genbylayer[0][iatom] = newfp
            #if newfp.coreele < 18: continue
            #if newfp.coreele == 1: continue
            self.allfp.append(newfp)

    def UpdateLayer(self,layer):
        newfplist =[]
        for iatom,atom in enumerate(self.str.atom):
            newfp = singlefp()
            #newfp.append((1,self.genbylayer[layer-1][atom.id]))
            newfp.Inherit(self.genbylayer[layer-1][atom.id])
            for subatomid in self.genbylayer[layer-1][atom.id].allatom:
                #if self.str.atom[subatomid].ele > 18: continue
                for nb in self.str.atom[subatomid].nb:
                    if nb[1] not in newfp.allatom :# and self.str.atom[nb[1]].ele != 1:
                        newfp.neighbour.append([(nb[0], self.genbylayer[layer-1][nb[1]].index),nb[1]])
                        newfp.allatom.append(nb[1])
            
            #newfp.allatomset = set(newfp.allatom)
            newfp.genidentifier(self.dim)
            newfplist.append(newfp)
        #for fp in  newfplist:
            #print fp.save, fp.index
        newfplist =self.CheckDuplicate(newfplist)
        #print 'CheckDuplicate'
        #for fp in  newfplist:
        #    print fp.save, fp.index

        self.genbylayer.append([0 for x in range(self.str.natom)])
        for ifp,fp in enumerate(newfplist):
            if fp.save ==1:
                self.genbylayer[layer][ifp]= fp
                #if fp.coreele < 18: continue
                #if fp.coreele == 1: continue
                self.allfp.append(fp)
            else:
                self.genbylayer[layer][ifp] = self.genbylayer[layer-1][ifp]
        return

    def CheckDuplicate(self,newfplist):
        for newfp in newfplist:
            for fp in self.allfp:
                if set(newfp.allatomset) == set(fp.allatomset):
                    # for unity
                    #newfp.index = fp.index
                    # old mode
                    newfp.save = 0
                    break

        for newfp1 in newfplist:
            for newfp2 in newfplist:
                if set(newfp1.allatomset) == set(newfp2.allatomset):
                    if newfp1.index > newfp2.index:
                        #newfp1.index = newfp2.index
                        newfp1.save = 0
                    elif newfp1.index < newfp2.index:
                        #newfp2.index = newfp1.index
                        newfp2.save = 0
        return newfplist


#class NNFingerPrint(object):
#    def __init__(self):
#        return
#
#    def neighbouractive(self):
#        for degree in degrees:
#            atom_neighbour= self.atom[j].neighbour
#            bond_neighbour = self.bond[j].neighbour
#
#
#    def layerupdate(self):
#        return

def hashlist(list,dim =10000000):
    #print list
    string = ''
    for i in list:
        string = string +str(i)

    #print string
    md5 =hashlib.md5()

    #print md5.digest_size
    #print md5.block_size
    md5.update(string)
    #print md5.digest
    #print string

    #return md5.hexdigest()
    _tmp= md5.hexdigest()
    return int((int(_tmp,16))%dim)
    #return zlib.adler32(string)


if (__name__ == "__main__"):
    test =[1,2332421,1,14757242,2,124253533]
#    string = ''
#    for i in test:
#        string = string +str(i) 
#    sha1 =hashlib.sha1()
#    sha1.update(string)
#    print sha1.hexdigest()
#
#
#
#    md5 =hashlib.md5()
#    md5.update(string)
#    print md5.hexdigest()
#    
#
#
#    print zlib.adler32(string)
    print hashlist(test)


    test =AllStr()
    test.readfile('target.arc')
    test.calAllFakeBondMaxtrix()
    fp= ECFP(test[0],3)
    fp.GenECFP()
    #print len(fp.allfp)

    #for sfp in fp.allfp:
    #    print sfp.index

    print fp.allindex
    print fp.IndextoAtomset
    for ilayer in range(3):
        for iatom in range(test[0].natom):
            print ilayer,iatom,fp.genbylayer[ilayer][iatom].index, fp.genbylayer[ilayer][iatom].trace
#    all.GetAllpuresminame()
#    all.GenCanoicalSmiles(chiral= False)
#
#    ndim = 1000000
#    info= {}
#    info2 = {}
#    for i in range(len(test)):
#        str1 = test[i]
#        m1 = Chem.MolFromSmiles(str1.canname)
#        Chem.SanitizeMol(m1)
#        fptest= AllChem.GetHashedMorganFingerprint(m1,2,nBits=ndim, bitInfo = info,useChirality=False)
#        if i ==0:
#            fpall =fptest
#        fpall =fpall + fptest
#    print info
