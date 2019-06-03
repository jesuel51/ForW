# this scripts is used to construct the impurities density profiles according to the D and V of each radius 
#ptgyro=root['SETTINGS']['PHYSICS']['ptgyro']
ptgyro=len(root['INPUTS']['TGYRO']['input.tgyro']['DIR'].keys())
n_pvt=root['SETTINGS']['PHYSICS']['n_pvt']
a=root['INPUTS']['TGYRO']['input.profiles']['rmin'][-1] # minor radius
frac=root['SETTINGS']['PHYSICS']['FracImp']
radius=zeros(ptgyro)
Darr=zeros(ptgyro)
Varr=zeros(ptgyro)
root['SETTINGS']['PLOTS']['iplotlincheck']=0
for k in range(1,ptgyro+1):
    root['SETTINGS']['PLOTS']['indradius']=k
    root['PLOTS']['lincheck_neo.py'].run()
    radius[k-1]=root['OUTPUTS']['DV'][k]['radius']
    Darr[k-1]=root['OUTPUTS']['DV'][k]['D_neo']
    Varr[k-1]=root['OUTPUTS']['DV'][k]['V_neo']
# let's construct the profiles
VdD=Varr/Darr
VdDmid=(VdD[0:ptgyro-1]+VdD[1:ptgyro])/2
Dr=zeros(ptgyro-1)
ExpFct=zeros(ptgyro+1)
n_imp=zeros(ptgyro)
for k in range(0,ptgyro-1):
    m=ptgyro-1-k
    Dr[m-1]=radius[m-1]-radius[m]
#    ExpFct[m-1]=VdDmid[m-1]*Dr[m-1]+ExpFct[m]
    ExpFct[m]=VdDmid[m-1]*Dr[m-1]+ExpFct[m+1]
ExpFct[0]=VdDmid[0]/2.*radius[0]+ExpFct[1]
#ExpFct=ExpFct/a
n_imp=exp(ExpFct)
# then experimental D and V value should be calculated\
if root['SETTINGS']['SETUP']['mthdreaddata']==1:
    gamma_gb=root['OUTPUTS']['TGYRO']['out.tgyro.gyrobohm']['data']['10^19/m^2/s']
else:
    gamma_gb=root['OUTPUTS']['TGYRO']['out.tgyro.gyrobohm']['data']['Gamma_GB']
    gamma_gb=[float(item) for item in gamma_gb[1:]]
#print(Darr)
D_exp=Darr*gamma_gb[1:ptgyro+1]*a/(frac*n_imp[1:])
#print(D_exp)
V_exp=Varr*gamma_gb[1:ptgyro+1]/(frac*n_imp[1:])
# visuilization

lw=2
fs1=20
fs2=16
#plt.close()
figure('profile of impurities,resonctructed based on neoclassical transport')
subplot(2,2,1)
plot(radius,D_exp,'-bo',linewidth=lw)
xlabel('r/a',fontsize=fs1)
ylabel('D($m^2s^{-1}$)',fontsize=fs1)
xticks(fontsize=fs2)
yticks(fontsize=fs2)
subplot(2,2,3)
plot(radius,V_exp,'-bo',linewidth=lw)
xlabel('r/a',fontsize=fs1)
ylabel('V($ms^{-1}$)',fontsize=fs1)
xticks(fontsize=fs2)
yticks(fontsize=fs2)
subplot(2,2,2)
plot(radius,Varr/Darr/a,'-ro',linewidth=lw)
xlabel('r/a',fontsize=fs1)
ylabel('Grad(n)/n',fontsize=fs1)
xticks(fontsize=fs2)
yticks(fontsize=fs2)
subplot(2,2,4)
plot(radius,n_imp[1:],'-ro',linewidth=lw)
xlabel('radius',fontsize=fs1)
ylabel('n_imp(a.u)',fontsize=fs1)
xticks(fontsize=fs2)
yticks(fontsize=fs2)
