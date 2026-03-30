from uedge import *
from uedge.hdf5 import *

# [based on Tom Rognlien's original run pfboxp8e.64x32]
bbb.mhdgeo=-1		#set cartesian com.geometry
bbb.allocate()
bbb.isfixlb[0]=2		#left boundary as sym. plane no flux at cut
grd.radx = 1.e-2		#outer "radial" wall
grd.radm = 0.		#minimum "radial" position
grd.rad0 = 0.
grd.alfyt=-2.0		#radial nonuniformity factor < 0 => expanding
grd.za0 = 0.		#poloidal symmetry plane location
grd.zaxpt = 1.49
grd.zax = 1.76356		#poloidal location of divertor plate
grd.alfxt=4.0
grd.btfix = 2.		#constant total B-field
grd.bpolfix = 0.146     	#constant poloidal B-field
bbb.ngrid = 1
com.nxleg[0,0]=0
com.nxcore[0,0]=0
com.nxcore[0,1]=80
com.nxleg[0,1]=4*25
com.nycore[0]=0
com.nysol=1

# Finite-difference algorithms (upwind, central diff, etc.)
bbb.methn = 33		#ion continuty eqn
bbb.methu = 33		#ion parallel momentum eqn
bbb.methe = 33		#electron energy eqn
bbb.methi = 33		#ion energy eqn
bbb.methg = 33		#neutral gas continuity eqn

# Parallel neutral momentum equation
bbb.isupgon[0]=1
if (bbb.isupgon[0] == 1):
    bbb.isngon[0]=0
    com.ngsp=1
    com.nhsp=2
    bbb.ziin[com.nhsp-1]=0
    bbb.ineudif = 2

# Boundary conditions
bbb.isnicore = 1                #=1 sets density = ncore
bbb.ncore[0] = 1.e19   #hydrogen ion density on core
bbb.iflcore = 1         #set power to pcoree,i
swit = 13.47263*1.3  #.. real 1D, Sr_core = 15.350872366629881
                 #.. slab Ss_core = 1.1394117647058823
                 #.. the ratio is swit=Sr_core/Ss_core
bbb.pcoree = 0.5e6/swit       #core elec power 
bbb.pcorei = 0.5e6/swit       #core ion power
bbb.tedge = 2.          #fixed wall,pf Te,i if istewcon=1, etc
bbb.recycp[0] = 0.99    #hydrogen recycling coeff at plates
bbb.isnwconi = 0                #=0 for fniy=0
bbb.isnwcono = 0
bbb.isupwo = 2
bbb.isupwi = 2
bbb.lyup = 1.e5
bbb.isupcore = 1		#..zml du/dy = 0
bbb.istewc = 3
bbb.istiwc = 3
bbb.istepfc = 3
bbb.istipfc = 3
bbb.lyte = 1.e5
bbb.lyti = 1.e5
bbb.matwso = 1
bbb.matwsi = 1
bbb.recycw = 1e-10
bbb.recycm = -0.95	#up(nx,,2) = -recycm*up(nx,,1)
bbb.isupss = 1		#=1 allows supersonic BC
#..pumping
bbb.albdsi[0] = 0.995
#..
bbb.ckinfl = 0.
#..bcen
#bbb.recyce = 0.1
#bbb.bcen = 2.*bbb.recyce*4.    #..zml cfalbedo = 2, so bcen=cfalbedo*recyce*(kappal*Te/Ti + 1) approx 2.recyce*4.

# Volumetric neutral particle source
bbb.z0ni = 0                # center on right boundary
bbb.zwni = 0.20             # Gaussian half-width [grd.m]
bbb.r0ni = 5.e-3            # center of bbb.iy=1 cell
bbb.rwni = 1.               # large enough to give uniform in r 
bbb.allocate()                # allocates space for bbb.ivolcur
bbb.ivolcur[0] = 0.	        # ion current in equiv. Amps

# Volumetric power sources
bbb.z0pe = 0.               #Z [axial] position of e- power source
bbb.r0pe = 5.e-3            #R [radial] position of e- power source
bbb.rwpe = 1.               # large enough to give uniform in r 
bbb.zwpe = 0.2              # axial half-width [Gaussian] e- power source
bbb.pvole = 0.0		# elec power in source in W

bbb.z0pi = 0.               #Z [axial] position of ion power source
bbb.r0pi = 5.e-3            #R [radial] position of ion power source
bbb.rwpi = 1.               # large enough to give uniform in r 
bbb.zwpi = 0.2              # axial half-width [Gaussian] ion power source
bbb.pvoli = 0.0		# ion power in source in W

# Transport coefficients [irrelavent]
bbb.difni[0] = 1.               #D for radial hydrogen diffusion
bbb.kye = 1.            #chi_e for radial elec energy diffusion
bbb.kyi = 1.            #chi_i for radial ion energy diffusion
bbb.travis[0] = 1.e-4   #eta_a for radial ion momentum diffusion
bbb.parvis = 1.0                #parallel visc coefficent

# Flux limits
bbb.flalfe = 0.21               #electron parallel thermal conduct. coeff
bbb.flalfi = 1. #0.21               #ion parallel thermal conduct. coeff
bbb.flalfv = 0.5                #ion parallel viscosity coeff
bbb.flalfgx = 1.                #neut. dens in poloidal direction
bbb.flalfgy = 1.                #neut. dens in radial direction
bbb.flalfvgx = 1.               #neut. momentum dens in poloidal direction
bbb.flalfvgy = 1.               #neut. momentum dens in radial direction
bbb.flalftgx = 1.               #neut. energy dens in poloidal direction
bbb.flalftgy = 1.               #neut. energy dens in radial direction
bbb.isplflxl = 0                #=0 turns off Te,i flux limiting at plates

# Background neutral source at very low density
bbb.ngbackg[0] = 1.e9

# Ion-electron recombination
bbb.isrecmon = 1

# Solver package
bbb.svrpkg="nksol"
bbb.iscolnorm = 3
bbb.mfnksol = -3        
#bbb.epscon1 = .005
#bbb.ftol = 1.e-10
bbb.premeth="ilut"
#bbb.runtim=1.e-7
#bbb.rlx=.4
#bbb.lenpfac=50

#..Carbon impurity with fixed fraction
bbb.isimpon = 2
bbb.afracs = 1e-10

# Restart from bbb.a save file
bbb.restart = 1
bbb.allocate()
hdf5_restore('slab1D.hdf5')
#
