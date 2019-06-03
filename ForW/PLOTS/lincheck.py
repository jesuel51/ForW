import numpy as np
from scipy import linalg
# this script is used to check whether the flux of impurities is proprotional to the gradient
indradius=root['SETTINGS']['PLOTS']['indradius'] # the index of radius
# the turbulence and neoclassical part should be calculated before
root['PLOTS']['lincheck_tur.py'].run()
root['PLOTS']['lincheck_neo.py'].run()
#=========================================
gamma_neo=root['OUTPUTS']['DV'][indradius]['gamma_neo']      # neoclassical impurity particle flux
gamma_e_neo=root['OUTPUTS']['DV'][indradius]['gamma_e_neo']  # neoclasscial electron particle flux
aln_neo=root['OUTPUTS']['DV'][indradius]['aln_neo']
gamma_tur=root['OUTPUTS']['DV'][indradius]['gamma_tur']
gamma_e_tur=root['OUTPUTS']['DV'][indradius]['gamma_e_tur'] # 
aln_tur=root['OUTPUTS']['DV'][indradius]['aln_tur']

# get the scanned density that both NEO and TGLF have
aln=[]
gamma_elec=[]
gamma_imp=[]
count=0
aln_tur_str=[str(item) for item in aln_tur]
aln_neo_str=[str(item) for item in aln_neo]
for item in aln_tur_str:
#    if aln_neo_str.find(item)!=-1:
    if item in aln_neo_str:
        aln.append(float(item))
        gamma_elec.append(gamma_e_neo[count]+gamma_e_tur[count])
        gamma_imp.append(gamma_neo[count]+gamma_tur[count])
    count=count+1
# turn them into correct data format
aln=array(aln)
gamma_elec=array(gamma_elec)
gamma_imp=array(gamma_imp)
def linear_regression(X,Y):
    beta=np.linalg.solve(X.T.dot(X),X.T.dot(Y))
    return beta
# then we perform a linear regression on the impurities flux versus impurities density gradient
aln_T=zeros([len(aln),1])
aln_T[:,0]=aln
aln_T=np.hstack((aln_T, np.ones((aln_T.shape[0], 1), dtype=aln_T.dtype)))
beta=linear_regression(aln_T,gamma_imp)
gamma_fit=beta[0]*aln+beta[1]
# record the result
radius_loc=root['OUTPUTS']['TGYRO'][indradius]['input.tglf']['RMIN_LOC']
#radius_loc=root['OUTPUTS']['TGYRO'][indradius]['RMIN_LOC']
if not root['OUTPUTS']['DV'].has_key(indradius):
    root['OUTPUTS']['DV'][indradius]=OMFITtree()
root['OUTPUTS']['DV'][indradius]['aln']=aln
root['OUTPUTS']['DV'][indradius]['gamma']=gamma_imp
root['OUTPUTS']['DV'][indradius]['gamma_e']=gamma_elec
root['OUTPUTS']['DV'][indradius]['D']=beta[0]
root['OUTPUTS']['DV'][indradius]['V']=beta[1]

# plot
lw=2
fs1=20
fs2=16
if root['SETTINGS']['PLOTS']['iplotlincheck']==1:
#    plt.close()
    figure('lincheck-total',figsize=[16,6])
    subplot(1,2,1)
    plot(aln,gamma_elec,'-bo',linewidth=lw)
    xlabel('a/Ln_imp',fontsize=fs1)
    ylabel('$\Gamma_{elec}(GB)$',fontsize=fs1)
    gamma_mid=(gamma_elec[0]+gamma_elec[-1])/2.
    ylim(0.9*gamma_mid,1.1*gamma_mid)  # try to make the gamma_elec look roughly constant versus the a/Ln_imp
    xticks(fontsize=fs2)
    yticks(fontsize=fs2)
    subplot(1,2,2)
    plot(aln, gamma_imp,'-ro',label='raw data')
    plot(aln, gamma_fit,'-bo',label='fit')
    xlabel('a/Ln_imp',fontsize=fs1)
    ylabel('$\Gamma_{imp}(GB)$',fontsize=fs1)
    xticks(fontsize=fs2)
    yticks(fontsize=fs2)
    legend(loc=0,fontsize=fs2).draggable(True)

