##===================================
### input
##==================================
inputs=[(root['INPUTS']['TGLF']['input.tglf'],'input.tglf'),
        (root['INPUTS']['TGLF']['jobtglf.pbs'],'jobtglf.pbs'),
        (root['INPUTS']['TGLF']['monitePBStglf.sh'],'monitePBStglf.sh')
	]
##----------------------
### output
##----------------------
outputs=['out.tglf.run']
executable ='chmod 777 monitePBStglf.sh ; ./monitePBStglf.sh'
ret_code=OMFITx.executable(root, inputs=inputs, outputs=outputs, executable=executable)
#-----------------------
# load the results
#-----------------------
for item in outputs:
    root['OUTPUTS']['TGLF'][item]=OMFITasciitable(item)
