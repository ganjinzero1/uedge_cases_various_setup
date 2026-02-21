#
from uedge import *
from uedge.hdf5 import *

# Set the geometry
bbb.mhdgeo = 1 		#use MHD equilibrium
#!rm -f aeqdsk neqdsk		#change names of MHD eqil. files 
#!cp aeqdskd3d aeqdsk		# (Cannot tab or indent these 3 lines)
#!cp neqdskd3d neqdsk
flx.psi0min1 = 0.9999		#normalized flux on core bndry
flx.psi0min2 = 0.9999		#normalized flux on pf bndry
flx.psi0sep = 1.00001	#normalized flux at separatrix
flx.psi0max = 1.015		#normalized flux on outer wall bndry
bbb.ngrid = 1		#number of meshes (always set to 1)
com.nxleg[0,0] = 24*2		#pol. mesh pts from inner plate to x-point
com.nxcore[0,0] = 30*2	#pol. mesh pts from x-point to top on inside
com.nxcore[0,1] = 30*2	#pol. mesh pts from top to x-point on outside
com.nxleg[0,1] = 32*2		#pol. mesh pts from x-point to outer plate
com.nysol[0] = 1		#rad. mesh pts in SOL
com.nycore[0] = 0		#rad. mesh pts in core
#	alfcy = 2.5		#factor concentrating mesh near separatrix
com.nxomit = (59+8)*2		#only consider half-space btwn outer mp & plate
#flx.alfcy = 2.
#..zml moving target
grd.isspnew = 1
grd.istptest = [0, 0]
#grd.rstrike = [1.25931595, 1.71359283]
grd.rstrike = [1.11, 1.838]
#..zml geo modified to avoid cell face crossing around the X-pt
com.nxpt2msh = 2
com.nxpt2psh = 2
#com.dxpt2msh = 0.01  #.. old version
#com.dxpt2psh = 0.01
com.zxpt2msh = 0.01  #.. new version
com.zxpt2psh = 0.01

com.nxpt1msh = 2
com.nxpt1psh = 2
#com.dxpt1msh = 0.01
#com.dxpt1psh = 0.01
com.zxpt1msh = 0.01  #.. new version
com.zxpt1psh = 0.01

# Finite-difference algorithms (upwind, central diff, etc.)
bbb.methn = 33		#ion continuty eqn
bbb.methu = 33		#ion parallel momentum eqn
bbb.methe = 33		#electron energy eqn
bbb.methi = 33		#ion energy eqn
bbb.methg = 33		#neutral gas continuity eqn

# Boundary conditions
bbb.isnicore = 1		#=1 sets density = ncore
bbb.ncore[0] = 0.5e19	#hydrogen ion density on core
bbb.iflcore = 1		#set power to pcoree,i
bbb.pcoree = 1.e6/2.		#core elec power 
bbb.pcorei = 1.e6/2.		#core ion power
bbb.tedge = 2.		#fixed wall,pf Te,i if istewcon=1, etc
bbb.recycp[0] = 0.99 	#hydrogen recycling coeff at plates
bbb.isnwconi = 3		#=0 for fniy=0
bbb.isnwcono = 3
bbb.lyni = 1.e5
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
bbb.isfixlb = 2		#=1 sets symmetry BC at outer midplane (ix=0)
#..pumping
bbb.albdsi[0] = 0.9999
#..
bbb.ckinfl = 0.
#..bcen
#bbb.recyce = 0.1
#bbb.bcen = 2.*bbb.recyce*4.    #..zml cfalbedo = 2, so bcen=cfalbedo*recyce*(kappal*Te/Ti + 1) approx 2.recyce*4.

# Localized Gaussian particle source
bbb.allocate()		#need to generate storage space
bbb.ivolcur[0] = 0. 
bbb.z0ni = 1.69		#outer midplane
bbb.r0ni = 2.32		#outer midplane
bbb.zwni = 0.2		#vertical Gaussian half-width
bbb.rwni = 0.2		#radial Gaussian half-width

# Transport coefficients
bbb.difni[0] = 1.		#D for radial hydrogen diffusion
bbb.kye = 1.		#chi_e for radial elec energy diffusion
bbb.kyi = 1.		#chi_i for radial ion energy diffusion
bbb.travis[0] = 1.e-4	#eta_a for radial ion momentum diffusion
bbb.parvis = 1.0		#parallel visc coefficent

# Flux limits
bbb.flalfe = 0.21		#electron parallel thermal conduct. coeff
bbb.flalfi = 1. #0.21		#ion parallel thermal conduct. coeff
bbb.flalfv = 0.5		#ion parallel viscosity coeff
bbb.flalfgx = 1.		#neut. dens in poloidal direction
bbb.flalfgy = 1.		#neut. dens in radial direction
bbb.flalfvgx = 1.		#neut. momentum dens in poloidal direction
bbb.flalfvgy = 1.		#neut. momentum dens in radial direction
bbb.flalftgx = 1.		#neut. energy dens in poloidal direction
bbb.flalftgy = 1.		#neut. energy dens in radial direction
bbb.isplflxl = 0		#=0 turns off Te,i flux limiting at plates

# Background neutral source at very low density
bbb.ngbackg[0] = 1.e9

# Ion-electron recombination
bbb.isrecmon = 1

# Solver package
bbb.svrpkg = "nksol"	#Newton solver using Krylov method
bbb.premeth = "ilut"	#Solution method for precond. Jacobian matrix
bbb.mfnksol = 3

# Parallel neutral momentum equation
bbb.isupgon[0]=1
if (bbb.isupgon[0] == 1):
    bbb.isngon[0]=0
    com.ngsp=1
    com.nhsp=2
    bbb.ziin[com.nhsp-1]=0
    bbb.ineudif = 2

#..Carbon impurity with fixed fraction
bbb.isimpon = 2
bbb.afracs = 1e-12

#..zml difference from singe version
#bbb.iswflxlvgy = 1
#bbb.iswflxltgy = 1
bbb.cfvgpy[1] = 1.
#bbb.isfdiax2 = 1.

# Restart from a pfb savefile
bbb.restart = 1		#Begin from savefile, not estimated profiles
bbb.allocate()		#allocate space for savevariables
hdf5_restore('pf_1D_outer_sol.hdf5')

#grd.fuzz=2


