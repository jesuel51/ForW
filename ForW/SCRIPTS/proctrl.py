# this script is used to control the whole execulation process
iMergeDT=root['SETTINGS']['PHYSICS']['iMergeDT']
consflag=root['SETTINGS']['SETUP']['consflag']
if iMergeDT==1 and root['INPUTS']['TGYRO']['input.tgyro']['LOC_MA1']!=2.5:
    root['SCRIPTS']['MergeDT.py'].run()
root['SCRIPTS']['runTGYRO.py'].run()
root['SCRIPTS']['scan.py'].run()
if 'neo' in consflag and 'tglf' not in consflag:
    root['PLOTS']['reconstructProfile_neo.py'].run()
elif 'neo' not in consflag and 'tglf' in consflag:
    root['PLOTS']['reconstructProfile_tur.py'].run()
# note before setting consflag constains both neo and tglf, root['SETTINGS']['SETUP']['irunneo'] should be set to 1
elif 'neo' in consflag and 'tglf' in consflag:
    root['PLOTS']['reconstructProfile.py'].run()


