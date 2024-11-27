
print('Importing libraries')
import torch   
import os
import shutil
import matplotlib.pyplot as plt  
import sys
import time
dir_path = os.path.dirname(os.path.realpath(__file__))

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-x', type=int, default=180,help='The x-coordinate of the source')
parser.add_argument('-y', type=int, default=140,help='The y-coordinate of the source')
args = parser.parse_args()
#to print
sx,sy,sz,_=torch.load(dir_path+'/COMCOT/domainParameters')

PTX=args.x
PTY=args.y
if 'COMCOT_app' in os.listdir(dir_path+'/COMCOT/SOURCE'):
    print('Running COMCOT for a 1 meter uplift at domain location %d, %d which has coordinates (%f,%f) on the world map'%(args.x,args.y,sx.unique()[args.x].item(),sy.unique()[args.y].item()))
    sourceloc=args.x+args.y*sx.unique().shape[0]
    if sz[sourceloc]<0:
        print('WARNING THIS SOURCE YOU CHOSE IS A LAND GRID POINT! No water there')
    
    print('Creating simulation folder')
    
    p=dir_path+'/COMCOT/tempfiles/';p2=dir_path+'/COMCOT/SOURCE/'
    print(p,p2)
    
    try: shutil.rmtree(p);shutil.copytree(p2,p)
    except: shutil.copytree(p2,p)
    
    print('Simulation folder created, preparing files for simulation')
    c=p+'comcot.ctl';u=open(c).read();uu=u.split('\n');
    uu[39]=uu[39][:49]+(p+'upliftTemplate.xyz');      
    o=open(p+'comcot.ctl','w');o.write('\n'.join(uu));o.close()    
    #write initial uplift
    o=open(dir_path+'/COMCOT/upliftTemplate.xyz');u=o.read().split('\n')[:-1];o.close()
    u[sourceloc]='  '.join(u[sourceloc].split()[:2]+[str(format(1,'.5e'))])#
    o=open(p+'upliftTemplate.xyz','w');o.write('\n'.join(u));o.close()    
    print('simulation files prepared, will run COMCOT')
    starttime=time.time()
    #run
    os.chdir(p)
    os.system("cd "+p)
    os.system("ulimit -s unlimited")
    os.system("chmod +x  "+p+"comcot_2021-12-08_Linux")
    os.system("./COMCOT_app")
    starttime=time.time()-starttime
    print('COMCOT simulation is done time taken is %d minutes,%d seconds'%(starttime//60,starttime-(starttime//60)*60))
    print('Now processing simulation output')
    h=os.listdir(p)  
    fls=[h[i] for i in range(len(h)) if 'layer' in h[i] and not 'max' in h[i] and not 'min' in h[i] and not 'ini' in h[i] and not 'BAK' in h[i] and not 'Tide' in h[i] and not 'cmask' in h[i] and not 'wbc' in h[i]]
    fls.sort()
    ax=[fls[i] for i in range(len(fls)) if '_x' in fls[i]]#x,y,and topo (-ve) file names
    ay=[fls[i] for i in range(len(fls)) if '_y' in fls[i]]
    az=[fls[i] for i in range(len(fls)) if not '_' in fls[i]]
    wavf=[h[i] for i in range(len(h)) if 'z_' in h[i]]#names of wave files
    wavf.sort()#water level
    def tensor(nme): yy=open(nme);y=yy.read();y=y.split();yy.close();y=[float(i) for i in y];return torch.tensor(y)#helper to load files convert to tensor
    
    tme=tensor(p+'time.dat');
    wave=torch.cat([tensor(p+i).view(1,-1) for i in wavf])     
    szx=tensor(p+'layer01_x.dat')
    szy=tensor(p+'layer01_y.dat')
    szz=tensor(p+'layer01.dat')
    print('Processing data is done')# now saving')
    mp=wave.view(-1,szy.unique().shape[0],szx.unique().shape[0])[500]
    gf=wave.view(-1,szy.unique().shape[0],szx.unique().shape[0])[:,  PTY-10,PTX-10 ]
else:
    print('COMCOT_app not found will plot pre-saved simulation results')
    tme, szx,szy,szz,mp,gf     =torch.load(dir_path+'/COMCOT/presaved');
    PTX,PTY=180,140

print('Now plotting some examples of the COMCOT simulation output')

_=plt.imshow(mp+szz.view(szy.unique().shape[0],szx.unique().shape[0]).ge(0).log(),origin='lower')#,cmap='seismic')
_=plt.plot(PTX,PTY,'*r')
_=plt.title("Green's function response at time (hrs:min) %d:%d \n due to a 1 meter uplit at the source \n shown by the red asterik"%(tme[500]//3600,(tme[500]-(tme[500]//3600)*3600)//60    )   )
ax=plt.gca()
_=ax.set(xticks=torch.arange(366)[::39], xticklabels=[int(i.item()*10)/10 for i in szx.unique()][::39]);
_=ax.set(yticks=torch.arange(295)[::30], yticklabels=[int(i.item()*10)/10 for i in szy.unique()][::30]);
_=plt.xlabel('Longitude (degrees)');
_=plt.ylabel('Latitude (degrees)');
cb=plt.colorbar();cb.set_label('(meters)')
_=plt.tight_layout()
_=plt.figure()
_=plt.plot(tme,gf)
_=plt.xlabel('Time seconds')
_=plt.ylabel('Wave (m)')
_=plt.title('Response at (%.1f,%.1f) due to \n 1 meter uplit at (%.1f°,%.1f°) as a function of time'%(szx.unique()[args.x-10].item(),szy.unique()[args.y-10].item(),szx.unique()[args.x].item(),szy.unique()[args.y].item()))
_=plt.xlim(0);_=plt.grid();plt.show()
print('Demo example done')
           

