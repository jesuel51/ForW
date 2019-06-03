# this script is used to scan the TGLF with different impurities density gradient
ptgyro=root['SETTINGS']['PHYSICS']['ptgyro']
RankImp=root['SETTINGS']['PHYSICS']['RankImp']
nscan=root['SETTINGS']['PHYSICS']['nscan']
alnrange=root['SETTINGS']['PHYSICS']['alnrange']
aln=linspace(alnrange[0],alnrange[1],nscan)
# start to scan
for k in range(1, ptgyro+1):
    root['INPUTS']['TGLF']['input.tglf']=root['OUTPUTS']['TGYRO'][k]['input.tglf']
    root['OUTPUTS']['TGLFScan'][k]=OMFITtree()
    for item in aln:
        root['OUTPUTS']['TGLF']=OMFITtree()
        root['INPUTS']['TGLF']['input.tglf']['RLNS_'+str(RankImp+1)]=item
        root['SCRIPTS']['runTGLF.py'].run()
        root['OUTPUTS']['TGLFScan'][k][item]=OMFITtree()
        for item2 in root['OUTPUTS']['TGLF']:
            root['OUTPUTS']['TGLFScan'][k][item][item2]=root['OUTPUTS']['TGLF'][item2]


