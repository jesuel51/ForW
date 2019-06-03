import numpy as np
from scipy import linalg
# this script is used to check whether the flux of impurities is proprotional to the gradient
indradius=root['SETTINGS']['PLOTS']['indradius'] # the index of radius
alnrange=root['SETTINGS']['PHYSICS']['alnrange']
nscan=root['SETTINGS']['PHYSICS']['nscan']
aln=linspace(alnrange[0],alnrange[1],nscan)
#ns=root['INPUTS']['NEO']['input.neo']['N_SPECIES']
#ns=root['SETTINGS']['PHYSICS']['RankImp']
ns=root['INPUTS']['TGYRO']['input.tgyro']['LOC_N_ION']
#ptgyro=root['SETTINGS']['PHYSICS']['ptgyro']
ptgyro=len(root['INPUTS']['TGYRO']['input.tgyro']['DIR'].keys())
def getgamma(fn,ns,fileflag):
    # this function is used to get the electron and impurities particle flux from fn, ns is the number of species, in view of the 
    # fileflag can be 1: out.neo.transport or 2:out.neo.transport_gv
    gamma=zeros(2)
    f=open(fn,'Ur')
    for line in f:
        data=[float(item) for item in line.split()]
    if fileflag==1:  # result from direct DKE equation
        gamma[0]=data[5+8*1]  # electron particle flux 
        gamma[1]=data[5+8*ns]  # impurities particle flux
    else:            # result from gyro-viscous effect
        gamma[0]=data[1+3*1]     # electron particle flux
        gamma[1]=data[1+3*ns] # impurity effect
    return gamma
gamma=zeros([nscan,2])
count=0
n_null=[]
for item in aln:
    try:
        fn1=root['OUTPUTS']['NEOScan'][indradius][item]['out.neo.transport'].filename
        fn2=root['OUTPUTS']['NEOScan'][indradius][item]['out.neo.transport_gv'].filename
        gamma[count]=getgamma(fn1,ns,1)+getgamma(fn2,ns,2)
#    else:
    except:
        n_null=n_null+[count]
    finally:
        count=count+1
print(n_null)
def delarr(X,num):
    X=list(X)
#    del X[array(n) for n in num]
    for m in range(0,len(num)):
        del X[num[m]-m]
    X=array(X)
    return X

# there should be a unit conversion between NEO normalization to GB normalization here
rho_sa=root['OUTPUTS']['TGYRO']['out.tgyro.nu_rho']['data']['rho_s/a']
rho_sa=[float(item) for item in rho_sa[-ptgyro-1:]] # 13 element here
Gamma_neo_GB=root['OUTPUTS']['TGYRO'][indradius]['input.tglf']['TAUS_2']**0.5*root['OUTPUTS']['TGYRO'][indradius]['input.tglf']['AS_2']*rho_sa[indradius]**(-2)
#print(rho_sa[indradius])
gamma=gamma*Gamma_neo_GB;
# distribute the values
gamma_elec=gamma.T[0]
gamma_imp=gamma.T[1]
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
radius_loc=root['OUTPUTS']['TGYRO'][indradius]['input.neo']['RMIN_OVER_A']
if not root['OUTPUTS']['DV'].has_key(indradius):
    root['OUTPUTS']['DV'][indradius]=OMFITtree()
root['OUTPUTS']['DV'][indradius]['radius']=radius_loc
root['OUTPUTS']['DV'][indradius]['aln_neo']=aln
root['OUTPUTS']['DV'][indradius]['gamma_neo']=gamma_imp
root['OUTPUTS']['DV'][indradius]['gamma_e_neo']=gamma_elec
root['OUTPUTS']['DV'][indradius]['D_neo']=beta[0]
root['OUTPUTS']['DV'][indradius]['V_neo']=beta[1]
# plot
lw=2
fs1=20
fs2=16
if root['SETTINGS']['PLOTS']['iplotlincheck']==1:
#    plt.close()
    figure('lincheck-neo',figsize=[16,6])
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

