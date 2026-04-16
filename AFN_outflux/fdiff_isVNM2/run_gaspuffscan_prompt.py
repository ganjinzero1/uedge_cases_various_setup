import os
import numpy as np
import time
startT = time.time()
# fixed parameters
#pin = 1.e6
#frc = 1.e-8
#alb = 0.995
#swit = 13.47263*1.3
#bbb.pcoree = pin/2./swit
#bbb.pcorei = pin/2./swit
#bbb.afracs = frc/100.
#bbb.albdsi[0] = 0.995

# Do gas puff scan
nmin = 2500#1200#300#4500#3600#2800#2000#1600#1100#400#750#550#300#200#230#2.85#1.05#0.68
nmax = 3000#2000#1000#4000#3200#2400#1800#1500#1000#850#700#500#250#1000#3.#2.#1.
nsa = 2#23
n_sample = np.linspace(float(nmin),float(nmax),nsa)# * 10**19

# loop
for isam in range(len(n_sample)):
  #bbb.ncore[0] = n_sample[isam]
  bbb.igaso[2] = n_sample[isam]
  fn = 'igas'+str(round(n_sample[isam],3))
  h5n = 'savedt.hdf5' + '_' + fn

  if os.path.exists(fn) and os.path.exists(h5n):
      print (h5n,' exists, skipped to next one')
      continue
  # run uedge and save files
  bbb.dtreal = 1e-5
  bbb.itermx = 30
  #bbb.nis = 0.999*bbb.nis
  #bbb.icntnunk = 0
  if isam > 0:
      bbb.icntnunk = 0
      bbb.ftol = 1e-5
  bbb.exmain()
  if bbb.iterm == 1:
      print ('before rdcontdt')
      exec(open('rdcontdt_exec.py').read())
      fnrm_old = np.sqrt(sum((bbb.yldot[0:bbb.neq-1]*bbb.sfscal[0:bbb.neq-1])**2))
      if (fnrm_old<bbb.ftol_min):
          exec(open('/home/zml/uedge_new_github/UEDGE/pylib/savedata_standard.py').read())
          savedata(fn)
          #if not os.path.exists(fn):
          #    os.makedirs(fn)
          #if os.path.exists(fn):
          #    shutil.rmtree(fn, ignore_errors=True)
          #    os.rename('data',fn)
          #else:
          #    os.rename('data',fn)
          #os.rename('savedt.hdf5',h5n)
          #hdf5_save(h5n)
          c.save(h5n)
  else:
      print('change ncore')

runT = time.time() - startT
open(str(nmin)+'-'+str(nmax)+'-'+str(nsa)+'_'+str(runT),'a').close()
#exit()
