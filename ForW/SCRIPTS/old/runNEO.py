##===================================
### input
##==================================
inputs=[(root['INPUTS']['NEO']['input.neo'],'input.neo'),
        (root['INPUTS']['NEO']['jobneo.pbs'],'jobneo.pbs'),
        (root['INPUTS']['NEO']['monitePBSneo.sh'],'monitePBSneo.sh')
	]
root['INPUTS']['NEO']['input.neo']['SIM_MODEL']=1
##----------------------
### output
##----------------------
outputs=['out.neo.transport','out.neo.theory','out.neo.theory_nclass']
executable ='chmod 777 monitePBSneo.sh ; ./monitePBSneo.sh'
ret_code=OMFITx.executable(root, inputs=inputs, outputs=outputs, executable=executable)
#-----------------------
# load the results
#-----------------------
for item in outputs:
    root['OUTPUTS']['NEO'][item]=OMFITasciitable(item)
