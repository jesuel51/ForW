# I plan to modify this script into a function which is more easy to be used
# you just need to specify 
# (1) the inputfile and path;
# (2) the tree to store the output and the format to name it;
# (3) soemother settings, eg. the execulation name, the core used and so on.

exec_name=root['SETTINGS']['SETUP']['executable'].split()[0]  # could be tglf or neo
print "============== scan_"+exec_name+" ==========="
# specify the caseroot and casetag, note usually caseroot needs to have the key caseName
caseRoot=root['Cases'] # the root of the tag, defines where to store the scanning data
caseName=root['SETTINGS']['PHYSICS']['case_tag'] # the name of the tag, which indicates the name of the scanning
if not caseRoot.has_key(caseName):
    caseRoot[caseName]=OMFITtree()
else:
    for item in caseRoot[caseName].keys():     #cover the previous calculation
        del caseRoot[caseName][item]
wkdir=root['SETTINGS']['SETUP']['workDir'] # the local directory(not the remote one)
dir_list=[]
inputs_node_names={'input.'+exec_name:OMFITnamelist} # input node names (not file name), in a format of dictionary
#inputs_node=root['INPUTS']['TGLF']             # the father node of input_nodes_names
inputs_series_nodes=root['OUTPUTS']['TGYRO']  # the input.tglf or input.neo for all the radial grids are stored here
inputs=[]

if exec_name=='tglf':
#    base_loadOutputs={'out.tglf.run':OMFITpath,'run_log':OMFITpath}
    base_loadOutputs={'out.tglf.run':OMFITasciitable,'run_log':OMFITpath}
elif exec_name=='neo':
#    base_loadOutputs={'out.neo.run':OMFITpath,'out.neo.transport':OMFITpath,'out.neo.theory':OMFITpath,'out.neo.theory_nclass':OMFITpath,'run_log':OMFITpath}
    base_loadOutputs={'out.neo.run':OMFITasciitable,'out.neo.transport':OMFITpath,'out.neo.transport_gv':OMFITpath}#'out.neo.theory':OMFITpath,'out.neo.theory_nclass':OMFITpath,'run_log':OMFITpath}
else:
    print('Error!! You need to choose a correct execulatation name!')
# the inputfiles will not be load as output anymore 
#for item in inputs_node_names.keys():
#    base_loadOutputs[os.path.basename(root['INPUTS'][item].filename)]=inputs_node_names[item] #the input is recorded to output, os.path,basename is the name of the file but picked out the path
#kyarr=root['SETTINGS']['SETUP']['kyarr']
aln_arr=linspace(root['SETTINGS']['PHYSICS']['alnrange'][0],root['SETTINGS']['PHYSICS']['alnrange'][1],root['SETTINGS']['PHYSICS']['nscan'])
loadOutputs={} 
#for ra_ind in inputs_series_nodes.keys():
p_tgyro=len(root['INPUTS']['TGYRO']['input.tgyro']['DIR'])
for ra_ind in range(1,p_tgyro+1):
    printi('running the calculation on ra_ind='+str(ra_ind))
    # set list
    inputs_node=inputs_series_nodes[ra_ind]['input.'+exec_name]
    if exec_name=='tglf':
        inputs_node['USE_TRANSPORT_MODEL']=True
    for aln in aln_arr:
#        print('ky=',ky)
        new_dir='ra-ind~'+str(ra_ind)+'~aln~'+str(aln)[0:4]  # here we only retains 4 effective number for defining the ky
        dir_list.append(new_dir)
        # transfer the value to the inputs and prepare for running
#        inputs_node['input.tglf']['KY']=ky
        if exec_name=='tglf':
            inputs_node['RLNS_'+str(inputs_node['NS'])]=aln
        else:
            inputs_node['DLNNDR_'+str(inputs_node['N_SPECIES'])]=aln
        ## ----------------- ##
        caseRoot[caseName][new_dir]=OMFITtree()
        if os.path.isfile(new_dir+r'.zip'):
            os.remove(new_dir+r'.zip')
        tmp_zip=zipfile.ZipFile(new_dir+r'.zip', mode='w') # construct a new zip file, and waiting for files to be written in 
#        for item  in inputs_node_names.keys():
#            if inputs_node.has_key(item):
#                inputs_node[item].save()
#                caseRoot[caseName][new_dir][item]=copy.deepcopy(inputs_node[item])
        item='input.'+exec_name
        inputs_node.save()
        caseRoot[caseName][new_dir][item]=copy.deepcopy(inputs_node)
        tmp_zip.write(caseRoot[caseName][new_dir][item].filename, caseRoot[caseName][new_dir][item].filename.split(os.sep)[-1]) # os.sep is / for linux and \ for windows
        tmp_zip.close()
        caseRoot[caseName][new_dir]['zip']=OMFITpath(tmp_zip.filename) # the inputs are compressed as an zip file and loaded in the output directory
        inputs.append(caseRoot[caseName][new_dir]['zip'])              # then the zipfile are import as input
        # set OUTPUTS( a lot of dir ) for loadOutputs, all the parameters ranges are covered
        for item in base_loadOutputs:
            loadOutputs[new_dir+os.sep+item]=base_loadOutputs[item]
        # so till now, a lot of zip files ,covering all the paraters set , are constructed. In addition, all the output file forms, are also constructed.
        # next issues is to run with the inputfiles prepared in zip file format
outputs=loadOutputs.keys()
#
executable='mv * input.'+exec_name+';\n '+root['SETTINGS']['SETUP']['executable']

#set job scipts
pbs_file=root['SETTINGS']['SETUP']['workDir']+os.sep+'scan.pbs'
username=root['SETTINGS']['REMOTE_SETUP']['server'].split('@')[0]
ps_name=exec_name
#print ps_name # You may need to check command name

## the bash_head below is used for runing on SHNEMA
if root['SETTINGS']['SETUP']['server']=='SHENMA':
    bash_head = \
    r'#!/bin/sh '+'\n'+ \
    r'#PBS -N '+ps_name +'\n'+ \
    r'#PBS -l nodes='+str(root['SETTINGS']['SETUP']['num_nodes'])+':ppn='+str(root['SETTINGS']['SETUP']['num_cores']) +'\n'+ \
    r'#PBS -j oe' +'\n'+ \
    r'#PBS -l walltime='+str(root['SETTINGS']['SETUP']['wall_time']) +'\n'+ \
    r'#PBS -q '+root['SETTINGS']['SETUP']['pbs_queue'] +'\n'+ \
    r'cd ${PBS_O_WORKDIR}' +'\n'+ \
    r'pwd'  +'\n'+ \
    r'NP=`cat ${PBS_NODEFILE}|wc -l`' +'\n'+ \
    '\n'+ \
    r'JOBID_FILE="JOBID_${PBS_JOBID}"' +'\n'+ \
    r'touch ${JOBID_FILE}' +'\n'
else:
    # the bash_head below is suitable for kuafu
    num_nodes=root['SETTINGS']['SETUP']['num_nodes']
    num_cores=root['SETTINGS']['SETUP']['num_cores']
    bash_head= \
    r'#!/bin/sh '+'\n' + \
    r'#SBATCH -p '+root['SETTINGS']['SETUP']['pbs_queue'] +'\n' +\
    r'#SBATCH -J '+ps_name +'\n' +\
    r'#SBATCH -t '+str(root['SETTINGS']['SETUP']['wall_time']) +'\n' +\
    r'#SBATCH -o -o.out'+'\n' +\
    r'#SBATCH -e -e.out'+'\n' +\
    r'#SBATCH --workdir=./'+'\n' +\
    r'#SBATCH --ntasks '+str(num_nodes*num_cores) +'\n'
###########
bash_content= \
'dir_list=('+' '.join(dir_list)+')' +'\n'+ \
r'for i in ${dir_list[@]}; ' +'\n'+  \
'do '  +'\n'+  \
r'  while [[ $( ps -u '+username+r' |grep '+ps_name+r' | wc -l ) -gt '+str(root['SETTINGS']['SETUP']['num_cores']-1)+' ]]; do ' +'\n' + \
r'    sleep 2s' +'\n' +\
r'  done ' +'\n'+ \
r'  unzip ${i}.zip -d $i ' +'\n'+ \
r' cd $i'  +'\n'+ \
executable+r' > run_log & ' +'\n'+ \
r"  cd .." +'\n'+ \
r'done' +'\n'

bash_tail= \
r'while [[ $( ps -u '+username+r' |grep '+ps_name+r' | wc -l ) -gt 0 ]]; do ' +'\n' + \
r'  sleep 5s' +'\n'+ \
r'done ' +'\n'+ \
r'rm ${JOBID_FILE}' +'\n'



##############################################
if not os.path.exists(str(root['SETTINGS']['SETUP']['workDir'])):
    os.makedirs(str(root['SETTINGS']['SETUP']['workDir']))
##############################################
with open(pbs_file,'w') as f1:
    f1.write(bash_head+'\n'+bash_content+'\n'+bash_tail)
caseRoot[caseName][pbs_file.split(os.sep)[-1]]=OMFITascii(pbs_file)

inputs.append(caseRoot[caseName][pbs_file.split(os.sep)[-1]])

# sub jobs
#executable='chmod u+x pbsMonitor; ./pbsMonitor '+'scan.pbs'
executable='/project/CFETR/bin/pbsMonitor '+'scan.pbs'
#executable='chmod u+x '+pbs_file+'; '+pbs_file
ret_code=OMFITx.executable(root, inputs=inputs, outputs=[],  server=root['SETTINGS']['REMOTE_SETUP']['server'], tunnel=None, executable=executable,clean=True)

workDir='./'
workDir=str(root['SETTINGS']['REMOTE_SETUP']['workDir'])+os.sep
# load result
print 'listdir'
print os.listdir(workDir)
#print os.listdir(wkdir+os.sep)
#print outputs
for item in outputs:
    if os.path.exists(workDir+os.sep+item):
        print "Loading "+item
        if not caseRoot[caseName].has_key(item.split(os.sep)[0]):
            caseRoot[caseName][item.split(os.sep)[0]]=OMFITtree()
        caseRoot[caseName][item.split(os.sep)[0]][item.split(os.sep)[-1]]=loadOutputs[item](workDir+os.sep+item)
for item in caseRoot[caseName]:
    if isinstance(caseRoot[caseName][item],dict) and caseRoot[caseName][item].has_key('zip'):
        del caseRoot[caseName][item]['zip']
del caseRoot[caseName]['scan.pbs']
