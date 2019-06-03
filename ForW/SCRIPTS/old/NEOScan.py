# this script is used to scan the TGLF with different impurities density gradient
ptgyro=root['SETTINGS']['PHYSICS']['ptgyro']
RankImp=root['SETTINGS']['PHYSICS']['RankImp']
nscan=root['SETTINGS']['PHYSICS']['nscan']
alnrange=root['SETTINGS']['PHYSICS']['alnrange']
aln=linspace(alnrange[0],alnrange[1],nscan)
# start to scan
for k in range(1, ptgyro+1):
    root['INPUTS']['NEO']['input.neo']=root['OUTPUTS']['TGYRO'][k]['input.neo']
    root['OUTPUTS']['NEOScan'][k]=OMFITtree()
    for item in aln:
        root['OUTPUTS']['NEO']=OMFITtree()
        root['INPUTS']['NEO']['input.neo']['DLNNDR_'+str(RankImp+1)]=item
        root['SCRIPTS']['runNEO.py'].run()
        root['OUTPUTS']['NEOScan'][k][item]=OMFITtree()
        for item2 in root['OUTPUTS']['NEO']:
            root['OUTPUTS']['NEOScan'][k][item][item2]=root['OUTPUTS']['NEO'][item2]
