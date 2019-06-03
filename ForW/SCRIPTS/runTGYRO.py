# add the tungsten to the ions
input_tgyro=root['INPUTS']['TGYRO']
FracImp=root['SETTINGS']['PHYSICS']['FracImp']
MImp=root['SETTINGS']['PHYSICS']['MImp']
ZImp=root['SETTINGS']['PHYSICS']['ZImp']
#RankImp=root['SETTINGS']['PHYSICS']['RankImp'] # rank of the impurities in the ion species
inputs=[(input_tgyro['input.profiles'],'input.profiles'),
        (input_tgyro['input.profiles.geo'],'input.profiles.geo'),
        (input_tgyro['input.tgyro'],'input.tgyro'),
        (input_tgyro['jobtgyro.pbs'],'jobtgyro.pbs'),
        (input_tgyro['monitePBStgyro.sh'],'monitePBStgyro.sh')
	]
# add the impurities to the input.profiles
Loc_n_ion=input_tgyro['input.tgyro']['LOC_N_ION']+1
input_tgyro['input.tgyro']['LOC_N_ION']=Loc_n_ion
input_tgyro['input.tgyro']['LOC_MA'+str(Loc_n_ion)]=MImp
input_tgyro['input.tgyro']['LOC_Z'+str(Loc_n_ion)]=ZImp
input_tgyro['input.profiles']['ni_'+str(Loc_n_ion)]=FracImp*root['INPUTS']['TGYRO']['input.profiles']['ne']
# note NEO result is quite sensitive to whether it's quasi-netral. So here we need to enforce quasi-neutral , 
# the density of the 1st ions is used to enforce quasi-neutrality
temp=input_tgyro['input.profiles']['ne']
for k in range(2,input_tgyro['input.tgyro']['LOC_N_ION']+1):
    temp=temp-input_tgyro['input.profiles']['ni_'+str(k)]*input_tgyro['input.tgyro']['LOC_Z'+str(k)]
input_tgyro['input.profiles']['ni_1']=temp
# run TGYRO with 0 iteration to give input for TGLF
input_tgyro['input.tgyro']['TGYRO_RELAX_ITERATIONS']=0
##----------------------
### output
##----------------------
#p_tgyro=root['SETTINGS']['PHYSICS']['ptgyro']
ptgyro=len(input_tgyro['input.tgyro']['DIR'].keys())
outputs=['out.tgyro.gyrobohm','out.tgyro.nu_rho']
for k in range(1,ptgyro+1):
    input_tgyro['input.tgyro']['DIR']['TGLF'+str(k)]=1
    outputs.append('TGLF'+str(k)+'/out.tglf.localdump')
    outputs.append('TGLF'+str(k)+'/out.neo.localdump')
#print(outputs)    
##executable = str(root['SETTINGS']['SETUP']['executable'])
#executable ='chmod 777 monitePBStgyro.sh; ./monitePBStgyro.sh'
executable ='chmod 777 monitePBStgyro.sh ; ./monitePBStgyro.sh'
executable=executable+'; pbsMonitor '\
            + ' -jq '+ root['SETTINGS']['SETUP']['pbs_queue']\
            + ' -jn '+ str(root['SETTINGS']['SETUP']['num_nodes'])\
            + ' -cn '+ str(root['SETTINGS']['SETUP']['num_cores'])\
            + ' -wallTime ' + root['SETTINGS']['SETUP']['wall_time']\
            + ' -exe tgyro -e . -n '+str(sum([input_tgyro['input.tgyro']['DIR']['TGLF'+str(k)]for k in range(1,ptgyro+1)]))

ret_code=OMFITx.executable(root, inputs=inputs, outputs=outputs, executable=executable)
#ret_code=OMFITx.executable(root, inputs=inputs, outputs=outputs, executable=executable,clean='true')

#-----------------------
# load the results
#-----------------------
root['OUTPUTS']['TGYRO']['out.tgyro.gyrobohm']=OMFITasciitable('out.tgyro.gyrobohm')
root['OUTPUTS']['TGYRO']['out.tgyro.nu_rho']=OMFITasciitable('out.tgyro.nu_rho')
for k in range(1,ptgyro+1):
#    print(k)
    root['OUTPUTS']['TGYRO'][k]=OMFITtree()
    root['OUTPUTS']['TGYRO'][k]['input.tglf']=OMFITgaCode(outputs[2*k])
    root['OUTPUTS']['TGYRO'][k]['input.neo']=OMFITgaCode(outputs[2*k+1])
# add the theta resolution in
    root['OUTPUTS']['TGYRO'][k]['input.neo']['N_THETA']=root['SETTINGS']['PHYSICS']['n_theta']

# the species information of backgrond plasma should be recovered so that the project can be ran again
#input_tgyro['input.tgyro']['LOC_N_ION']=Loc_n_ion-1
#del input_tgyro['input.tgyro']['LOC_MA'+str(Loc_n_ion)]
#del input_tgyro['input.tgyro']['LOC_Z'+str(Loc_n_ion)]
#input_tgyro['input.profiles']['ni_'+str(Loc_n_ion)]=0.*root['INPUTS']['TGYRO']['input.profiles']['ne']
