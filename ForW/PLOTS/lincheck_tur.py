import numpy as np
from scipy import linalg
# this fuction is used to read the out.tglf.run when TGLF ran in a nonlinear mode
# the particle flux of electrons and impurities is captured
#RankImp=root['SETTINGS']['PHYSICS']['RankImp']
Loc_n_ion=root['INPUTS']['TGYRO']['input.tgyro']['LOC_N_ION']
def readfile(fn):
    f=open(fn,'-Ur')
    gamma=zeros(2)
    for line in f:
        if line.find('elec')!=-1:
            ind=line.find('elec')
            gamma[0]=float(line[ind+7:ind+18])
        elif line.find('ion'+str(Loc_n_ion))!=-1:
            ind=line.find('ion'+str(Loc_n_ion))
            gamma[1]=float(line[ind+7:ind+18])
    return gamma
    f.close()
# this script is used to check whether the flux of impurities is proprotional to the gradient
indradius=root['SETTINGS']['PLOTS']['indradius'] # the index of radius
alnrange=root['SETTINGS']['PHYSICS']['alnrange']
nscan=root['SETTINGS']['PHYSICS']['nscan']
aln=linspace(alnrange[0],alnrange[1],nscan)
#ns=root['INPUTS']['TGLF']['input.tglf']['NS']
ns=root['INPUTS']['TGYRO']['input.tgyro']['LOC_N_ION']+1
gamma=zeros([nscan,ns])
count=0
n_null=[]
mthdreaddata=root['SETTINGS']['SETUP']['mthdreaddata']
if mthdreaddata==1:
    for item in aln:
    #    if root['OUTPUTS']['TGLFScan'][indradius][item]['out.tglf.run']['header']!='':
        try:
            gamma[count]=root['OUTPUTS']['TGLFScan'][indradius][item]['out.tglf.run']['data']['Gam/Gam_GB']
    #    else:
        except:
            n_null=n_null+[count]
        finally:
            count=count+1
    print(n_null)
    #gamma_elec=list(gamma_elec)
    gamma_elec=gamma[:,0]
    gamma_imp=gamma[:,ns-1]
else:
    gamma_elec=zeros(nscan)
    gamma_imp=zeros(nscan)
    for item in aln:
        try:
            fn=root['OUTPUTS']['TGLFScan'][indradius][item]['out.tglf.run'].filename
            gammatemp=readfile(fn)
            gamma_elec[count]=gammatemp[0]
            gamma_imp[count]=gammatemp[1]
        except:
            n_null=n_null+[count]
        finally:
            if gamma_elec[count]==0 and count not in n_null:
                n_null=n_null+[count]
            count=count+1
    print(n_null)
##########################
def delarr(X,num):
    X=list(X)
#    del X[array(n) for n in num]
    for m in range(0,len(num)):
        del X[num[m]-m]
    X=array(X)
    return X

gamma_elec=delarr(gamma_elec,n_null)
gamma_imp=delarr(gamma_imp,n_null)
aln=delarr(aln,n_null)
# then we perform a linear regression on the impurities flux versus impurities density gradient
aln_T=zeros([len(aln),1])
aln_T[:,0]=aln
def linear_regression(X,Y):
    beta=np.linalg.solve(X.T.dot(X),X.T.dot(Y))
    return beta
aln_T=np.hstack((aln_T, np.ones((aln_T.shape[0], 1), dtype=aln_T.dtype)))
beta=linear_regression(aln_T,gamma_imp)
gamma_fit=beta[0]*aln+beta[1]
# record the result
radius_loc=root['OUTPUTS']['TGYRO'][indradius]['input.tglf']['RMIN_LOC']
if not  root['OUTPUTS']['DV'].has_key(indradius):
    root['OUTPUTS']['DV'][indradius]=OMFITtree()
root['OUTPUTS']['DV'][indradius]['radius']=radius_loc
root['OUTPUTS']['DV'][indradius]['aln_tur']=aln
root['OUTPUTS']['DV'][indradius]['gamma_tur']=gamma_imp
root['OUTPUTS']['DV'][indradius]['gamma_e_tur']=gamma_elec
root['OUTPUTS']['DV'][indradius]['D_tur']=beta[0]
root['OUTPUTS']['DV'][indradius]['V_tur']=beta[1]
# plot
lw=2
fs1=20
fs2=16
if root['SETTINGS']['PLOTS']['iplotlincheck']==1:
#    plt.close()
    figure('lincheck-tglf',figsize=[16,6])
    subplot(1,2,1)
    plot(aln,gamma_elec,'-bo',linewidth=lw)
    xlabel('a/Ln_imp',fontsize=fs1)
#    ylabel('gamma_ele(GB)',fontsize=fs1)
    ylabel('$\Gamma_{elec}(GB)$',fontsize=fs1)
    gamma_mid=(gamma_elec[0]+gamma_elec[-1])/2.
    ylim(0.9*gamma_mid,1.1*gamma_mid)  # try to make the gamma_elec look roughly constant versus the a/Ln_imp
    xticks(fontsize=fs2)
    yticks(fontsize=fs2)
    subplot(1,2,2)
    plot(aln, gamma_imp,'-ro',label='raw data')
    plot(aln, gamma_fit,'-bo',label='fit')
    xlabel('a/Ln_imp',fontsize=fs1)
#    ylabel('gamma_imp(GB)',fontsize=fs1)
    ylabel('$\Gamma_{imp}(GB)$',fontsize=fs1)
    xticks(fontsize=fs2)
    yticks(fontsize=fs2)
    legend(loc=0,fontsize=fs2).draggable(True)

