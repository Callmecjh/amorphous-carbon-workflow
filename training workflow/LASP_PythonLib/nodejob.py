import screen
import sys

def collectallstr(workdirs,nbadneed):
    AllStr= screen.CoordSet()
    AllStr.arcinit([0,0],'%s/allstr.arc'%(workdirs)) #, '%s/allfor.arc'%(workdirs[i]))
    if (len(AllStr)== 0): return
    AllStr.RandomArange(200)
    AllStr = screen.CoordSet(AllStr[:nbadneed])
    AllStr.Gen_arc(range(len(AllStr)),'%s/outstr.arc'%workdirs,2)
    return

if __name__ == "__main__":
    workdir, nbadneed = sys.argv[1:]
    nbadneed = int(nbadneed)
    collectallstr (workdir, nbadneed)
