# load the outputs from the scanning for both tglf and neo
def loaddata():
    case_tag=root['SETTINGS']['PHYSICS']['case_tag']
    if 'tglf' in case_tag:
        scanname='TGLFScan'
    else:
        scanname='NEOScan'
    for item in root['Cases'][case_tag].keys():
        item_temp=item.split('~')
        if not  root['OUTPUTS'][scanname].has_key(int(item_temp[1])):
            root['OUTPUTS'][scanname][int(item_temp[1])]=OMFITtree()
        if not  root['OUTPUTS'][scanname][int(item_temp[1])].has_key(float(item_temp[3])):
            root['OUTPUTS'][scanname][int(item_temp[1])][float(item_temp[3])]=OMFITtree()
    #    if not root['OUTPUTS']['TGLFScan'][int(item_temp[0])][float(item_temp[1])].has_key('nonlin'):
    #        root['OUTPUTS']['TGLFScan'][int(item_temp[0])][float(item_temp[1])]['nonlin']=OMFITtree()
        for files in root['Cases'][case_tag][item].keys():
    #        root['OUTPUTS']['TGLFScan'][int(item_temp[0])][float(item_temp[1])]['nonlin'][files]=root['Cases'][case_tag][item][files]
            root['OUTPUTS'][scanname][int(item_temp[1])][float(item_temp[3])][files]=root['Cases'][case_tag][item][files]
    return 1

# this script is used to do the scan of density gradient for both running tglf and neo
root['SETTINGS']['PHYSICS']['case_tag']='tglf'
root['SETTINGS']['SETUP']['executable']='tglf -e . -n 1'
root['SCRIPTS']['subscan.py'].run()
loaddata()
if root['SETTINGS']['SETUP']['irunneo']==1:  #determine whether to run neo
    root['SETTINGS']['PHYSICS']['case_tag']='neo'
    root['SETTINGS']['SETUP']['executable']='neo -e . -n 1'
    root['SCRIPTS']['subscan.py'].run()
    loaddata()


