# this script is used to merge DT when necceary
inputpro=root['INPUTS']['TGYRO']['input.profiles']
inputtgyro=root['INPUTS']['TGYRO']['input.tgyro']
Loc_n_ion=inputtgyro['LOC_N_ION']
inputpro['ni_1']=inputpro['ni_1']+inputpro['ni_2']
inputtgyro['LOC_MA1']=2.5
for k in range(2,Loc_n_ion):
    inputpro['ni_'+str(k)]=inputpro['ni_'+str(k+1)]
    inputtgyro['LOC_MA'+str(k)]=inputtgyro['LOC_MA'+str(k+1)]
    inputtgyro['LOC_Z'+str(k)]=inputtgyro['LOC_Z'+str(k+1)]
# if the DT is merged, than Loc_n_ion should minus 1
inputtgyro['LOC_N_ION']=Loc_n_ion-1
# also, some note here, you must be careful when setting the RankImp,
# to get a sensible result, RankImp should be set to inputtgyro['LOC_N_ION']+1, since you need plus a new species, through it's of trace level
