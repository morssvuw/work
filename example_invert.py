
print('Importng modules')
import torch
import matplotlib.pyplot as plt
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-device', type=str , default=None,help='What device to use')
parser.add_argument('-sim', type=str, default='yes',help='if True will run simulation if not will plot presaved results')
args = parser.parse_args()
device=args.device
_=print('Checking GPU') if device==None else ''
if torch.cuda.is_available()==True:
   for i in range(torch.cuda.device_count()):
      if not device==None:
         continue
      try:
         _=torch.randn(1,device=torch.device('cuda',i))
         device=torch.device('cuda',i)
         print('Using ',device)
      except:
         print(torch.device('cuda',i),'Not available')
         
device='cpu' if device==None else device
if device=='cpu':
   print("WARNING: NO (spare) GPU WAS FOUND running using CPU will be slower")

if args.sim=='yes':
   sim=True
else:
   sim=False

SSX,SSY,SSZ,SST=torch.load(dir_path+'/COMCOT/domainParameters') 
SSX=SSX.view(1,-1).repeat(295,1).reshape(-1);SSY=SSY.view(-1,1).repeat(1,366).reshape(-1);
SSX=SSX.sub(SSX.min()).div(SSX.max().sub(SSX.min())).sub(.5).mul(2).to(device)
SSY=SSY.sub(SSY.min()).div(SSY.max().sub(SSY.min())).sub(.5).mul(2).to(device)
def pad(x,diffx,diffy):#padded data fun
   x=torch.cat([x[:,:1].repeat(1,diffx//2),x,x[:,-1:].repeat(1,diffx//2)],dim=-1)
   x=torch.cat([x[:1].repeat(diffy//2,1),x,x[-1:].repeat(diffy//2,1)],dim=0)
   return x

paddedSSZ=pad(SSZ.view(-1,366),20,20)
lowrespadded=torch.nn.UpsamplingNearest2d(paddedSSZ.shape)(torch.nn.AvgPool2d(2)(paddedSSZ.unsqueeze(0).unsqueeze(0)    ))[0,0]#torch.Size([335, 406])
paddedSSZ=paddedSSZ.clamp(-10).add(10).div(paddedSSZ.max()+10).sub(.5).mul(2).to(device);
lowrespadded=lowrespadded.clamp(-10).add(10).div(lowrespadded.max()+10).sub(.5).mul(2).to(device);
if True:
    class LN(torch.nn.Module): #layernorm
        def __init__(self, ndf=100, eps=1e-6):
            super(LN, self).__init__()
            self.a_2 = torch.nn.Parameter(torch.ones(ndf))
            self.b_2 = torch.nn.Parameter(torch.zeros(ndf))
            self.eps = eps
        def forward(self, x):
            mean = x.mean(-1, keepdim=True)
            std = x.std(-1, keepdim=True)
            return self.a_2 * (x - mean) / (std + self.eps) + self.b_2  
    CV=torch.nn.Conv1d;CT=torch.nn.ConvTranspose1d; A=torch.nn.LeakyReLU;L=torch.nn.Linear;Seq=torch.nn.Sequential
    class F(torch.nn.Module):# 
        def __init__(self,numseq=2,lyr=3,freq=20 ,dim=100,diffe=True,ptopo=None,ptopo2=None): 
            super(F, self).__init__() 
            self.freq=freq
            self.dim=dim
            self.pos=Seq(L(freq*4,int(dim*1.5)),A(),L(int(dim*1.5),dim))
            self.topo=Seq(L(400,int(dim*1.5)),A(),L(int(dim*1.5),dim))
            self.topo2=Seq(L(400,int(dim*1.5)),A(),L(int(dim*1.5),dim))
            self.diff=Seq(L(freq*4,int(dim*1.5)),A(),L(int(dim*1.5),dim))# 
            self.sinemb=Seq(L(24,int(dim*1.5)),A(),L(int(dim*1.5),dim))
            numseq=numseq+1  
            self.out=Seq(L(dim,250),CV(numseq-1,64,3,1,1),A(),CV(64,16,3,1,1),A(),CV(16,1,3,1,1))  
            self.mag=Seq(L(dim,250),A(),L(250,1))
            self.inn=Seq(CV(1,64,3,1,1),A(),CV(64,16,3,1,1),A(),CV(16,numseq-1,3,1,1),A(),L(250,dim))  
            self.Emb=(torch.arange(numseq+7,device=device).unsqueeze(-1).unsqueeze(-1).mul(2**torch.arange(12).view(1,1,1,-1,1).to(device))).add(torch.arange(2).view(1,1,1,1,-1).eq(1).mul(3.172/2).to(device)).view(1,7+numseq,-1).sin()#24 
            self.lyr=lyr 
            self.numseq=numseq
            self.diffe=int(diffe)
            self.k=torch.nn.ModuleList([Seq(LN(dim),L(dim,int(dim*1.5)),A(),L(int(dim*1.5),dim))   for i in range(lyr)])
            self.v=torch.nn.ModuleList([Seq(LN(dim),L(dim,int(dim*1.5)),A(),L(int(dim*1.5),dim))   for i in range(lyr)])
            self.q=torch.nn.ModuleList([Seq(LN(dim),L(dim,int(dim*1.5)),A(),L(int(dim*1.5),dim))   for i in range(lyr)])
            self.op=torch.nn.Parameter(torch.randn([1,numseq,dim])) 
            self.recovertopo=Seq(L(dim,300),A(),L(300,300),A(),L(300,400))
            self.recovertopo2=Seq(L(dim,300),A(),L(300,300),A(),L(300,400)) 
            idx=torch.arange(366*295)
            self.Topo=self.extract_(paddedSSZ,idx) if ptopo==None else ptopo
            self.Topo2=self.extract_(lowrespadded,idx) if ptopo2==None else ptopo2
            for pm in self.parameters(): pm.requires_grad=False
        def sine(self,x):
            freq=self.freq
            x= x.mul(2**torch.arange(0,freq).view(1,-1).to(x.device))
            return torch.cat([x.sin(),x.cos()],dim=1)
        def extract_(self,topo,pos):#get topo
            posy=pos//366;posx=pos-posy*366;posy=posy+10;posx=posx+10
            return torch.cat([topo[posy[i]-10:posy[i]+10,posx[i]-10:posx[i]+10].reshape(1,-1) for i in range(posy.shape[0])])
        def extract(self,topo,pos):
            return topo[pos]
        def encode(self,srcpos,tarpos,topo,topo2,ssx,ssy):#order is [xe,ye,sxe,sye,te,xd,yd]   
            srcti=self.extract(self.Topo,srcpos)
            srcti2=self.extract(self.Topo2,srcpos)
            tarti=self.extract(self.Topo,tarpos)
            tarti2=self.extract(self.Topo2,tarpos)
            ss=self.sine
            srcp=self.pos(  torch.cat( [ss(ssx[srcpos].view(-1,1)) ,ss(ssy[srcpos].view(-1,1)) ],dim=1)       ).unsqueeze(1)
            tarp=self.pos(   torch.cat( [ss(ssx[tarpos].view(-1,1)) ,ss(ssy[tarpos].view(-1,1)) ],dim=1)     ).unsqueeze(1)
            srct2=self.topo2(srcti2).unsqueeze(1)
            tart2=self.topo2(tarti2).unsqueeze(1)
            srct=self.topo(srcti).unsqueeze(1)
            tart=self.topo(tarti).unsqueeze(1)  
            diffo=self.diff(torch.cat( [ss(ssx[srcpos].sub(ssx[tarpos]).view(-1,1)/2 ),ss(ssy[srcpos].sub(ssy[tarpos]).view(-1,1)/2) ],dim=1)   ).unsqueeze(1)   *self.diffe                                                                             
            seq=torch.cat([srcp,tarp,srct,tart,srct2,tart2,diffo,self.op.to(device).repeat(srcp.shape[0],1,1)],dim=1) 
            pos=self.sinemb(self.Emb.to(srcp.device))
            ze=seq+pos 
            return ze
        def decode(self,z,mask):# 
            shp=z.shape
            for i in range(self.lyr):
                k=self.k[i](z);
                q=self.q[i](z);
                v=self.v[i](z);
                dims=k.shape[-1]//10
                k=k.view(shp[0],shp[1],10,dims).permute(0,2,1,3).reshape(-1,shp[1],dims)
                v=v.view(shp[0],shp[1],10,dims).permute(0,2,1,3).reshape(-1,shp[1],dims)
                q=q.view(shp[0],shp[1],10,dims).permute(0,2,1,3).reshape(-1,shp[1],dims)
                att=torch.matmul( torch.matmul (  q, k.permute(0,2,1)).div(5+self.numseq)  , v) #batch*heads , 1 20
                att=att.reshape(shp[0],-1,shp[1],dims).permute(0,2,1,3).reshape(shp[0],-1,dims*10)
                z=att+ z 
            return  z[:,-self.numseq:]
        def forward(self,srcpos,tarpos): 
            z=self.encode(srcpos,tarpos,paddedSSZ,lowrespadded,SSX,SSY)
            final =self.decode(z,None)
            out=self.out(final[:,:-1]).view(final.shape[0],-1)
            mag=self.mag(final[:,-1:]).view(final.shape[0],-1)
            return out*mag
 


print('Instantiate networks')
ptopo=ptopo2=None
netd =F(numseq=2,lyr=3,freq=20 ,dim=100,diffe=True,ptopo=ptopo,ptopo2=ptopo2).to(device)   
print('Load pretrained weights')
d= torch.load(dir_path+'/Japan_GF_network/trainedNet')
netd.load_state_dict( d['diff'] )



def edge(x,pwe=2,pwv=1,mule=1,mul1=.5,mulf=1):
      farr=torch.zeros([366*295]).to(device)
      farr[SSZ.ge(0)]=x
      dx=farr.view(-1,366)[:,1:].sub(farr.view(-1,366)[:,:-1]).abs().pow(pwe).sum()
      dy=farr.view(-1,366)[1:].sub(farr.view(-1,366)[:-1]).abs().pow(pwe).sum()
      f=torch.fft.rfft(farr.view(1,1,-1,366),norm='ortho')
      return x.abs().pow(pwv).sum()*mul1   +f.real.abs().sum().add(f.imag.abs().sum()).mul(mulf)+(dy+dx).mul(mule)


def wavft(x,y):
    x2=torch.fft.rfft(x.view(1,-1),norm='ortho');y2=torch.fft.rfft(y.view(1,-1),norm='ortho')
    return x2.real.sub(y2.real).square().add(x2.imag.sub(y2.imag).square()).sum()

print('Loading testing data')
import time

[srcidx,srcMO,dmnobs,dmnidx,dmn,T153]=torch.load(dir_path+'/invert/TestingArr',map_location=device)

divr=dmnobs.abs().max().item()#not needed in rl only for easier comprehnd stats


highres=None
EPS=60
Err=torch.zeros([EPS,4])
Preds={}
uplft={}
strt=time.time()
if sim==True:
   for obscnt,obstyp in enumerate([ torch.arange(0,150,3)]):#50 sensors
      srcM=srcMO.detach().clone();srcM.requires_grad=True;opt=torch.optim.Adam([srcM],lr=0.2)
      OBS=dmnobs[:,obstyp].div(divr)
      spc=5#should be adjusted as needed 
      for ep in range(0,EPS):
         if ep<15:#adjust with spc as needed
            act=torch.zeros(366*295).view(-1,366).bool();act[::spc,::spc]=True;act=act[SSZ.ge(0).view(-1,366)]
         else:
            if highres==None:#after initial convergence detailed update
               with torch.no_grad():
                  do=srcM[act].abs().gt(srcM[act].abs().max()*0.1)
                  shpx=torch.arange(0,366,spc).shape[0]
                  shpy=torch.arange(0,295,spc).shape[0]
                  avgx=torch.arange(0,366,spc).to(device).view(1,-1).repeat(shpy,1)[SSZ.ge(0).view(-1,366)[::spc,::spc]].reshape(1,-1).mul(srcM[act].abs())[:,do].sum(-1).div(srcM[act][do].abs().sum(-1)).item()
                  avgy=torch.arange(0,295,spc).to(device).view(-1,1).repeat(1,shpx)[SSZ.ge(0).view(-1,366)[::spc,::spc]].reshape(1,-1).mul(srcM[act].abs())[:,do].sum(-1).div(srcM[act][do].abs().sum(-1)).item()
                  act=torch.arange(366).sub(avgx).view(1,-1).abs().lt(50).mul( torch.arange(295).sub(avgy).view(-1,1) .abs().lt(50)).reshape(-1)[SSZ.ge(0)]
                  highres=True
         pred=torch.zeros(OBS.shape).to(device)
         bs=400#150*23
         srcix=torch.arange(366*295)[SSZ.ge(0)]
         uidx=torch.arange(srcidx.shape[0])[act]
         for i in range(1+(uidx.shape[0]//bs)):
            shp=srcidx[act][bs*i:bs*i+bs].shape[0]
            if shp==0 or srcM[act][bs*i:bs*i+bs].detach().abs().gt(0.0001*srcM[act].detach().abs().max()).view(-1).sum()==0: continue#no need low mag pixels excluded

            srcpos=srcidx[act][bs*i:bs*i+bs].view(1,-1,1).repeat(OBS.shape[1],1,1).reshape(-1)
            tarpos=dmnidx[obstyp].view(-1,1,1).repeat(1,shp,1).reshape(-1)
                          
            out=netd(srcpos,tarpos)
            out_=out.view(OBS.shape[1],shp,1,250).mul(srcM[act][bs*i:bs*i+bs].view(1,shp,1,1)).sum(1).sum(1)
            out_=out_.T
            pred=pred+out_;del out_,out
                
         pred.sub(OBS.to(device)).square().sum().add(
                                wavft(pred,OBS.to(device))*1.1).mul(4).backward()    
         with torch.no_grad():err=pred.to(device).sub(OBS.to(device)).square().mean(dim=[-1,-2]).cpu();
            
         edge(srcM,mule=0.9,mul1=(min(ep,40)*.01-min(50,max(ep,0))*.0079) ,mulf=0).backward()#.02
         opt.step();opt.zero_grad() 
         if ep>19: opt.param_groups[0]['lr']=0.1
         if ep>30: opt.param_groups[0]['lr']=0.05
         if ep>40: opt.param_groups[0]['lr']=0.01
         with torch.no_grad(): 
            corr=torch.corrcoef(  torch.cat(   [ srcM.reshape(1,-1).detach()*divr, dmn.reshape(1,-1)  ]   )      )[0,1].cpu().item()
            err=pred.to(device).sub(OBS.to(device)).square().mean(dim=[-1,-2]).cpu();errsprs=srcM.abs().mul( 1 ).mean(dim=[-1]).cpu()
            print('=========Iteration:%d========'%ep)
            print('Normalised Observation MSE:',round(err.mean().item(),3))
            print('Normalised uplift sparsity:',round(errsprs.mean().item(),3) )
            print('Correlation w.r.t. True uplift:',round(corr,2))
            print('==========%d min:%d s==========='%(int((time.time()-strt)//60) , (time.time()-strt)%60)  )
            print('\n')
            Err[ep,0]=err.item()
            Err[ep,1]=srcM.detach().sub(dmn.div(divr)).abs().mean().item()
            Err[ep,2]=errsprs.item()
            Err[ep,3]=corr 
            if ep%10==0 or ep==EPS-1:
              see=torch.zeros(366*295);see[srcidx]=srcM.cpu().mul(divr).cpu().detach()
              uplft[ep]=see
              pred=torch.zeros(dmnobs.shape[1]).to(device)
              bs=400#150*23
              srcix=torch.arange(366*295)[SSZ.ge(0)]
              uidx=torch.arange(srcidx.shape[0])[act]
              for i in range(1+(uidx.shape[0]//bs)):
                 shp=srcidx[act][bs*i:bs*i+bs].shape[0]
                 if shp==0 or srcM[act][bs*i:bs*i+bs].detach().abs().gt(0.0001*srcM[act].detach().abs().max()).view(-1).sum()==0: continue#exclude low mag
                 srcpos=srcidx[act][bs*i:bs*i+bs].view(1,-1,1).repeat(dmnobs.shape[1],1,1).reshape(-1)
                 tarpos=dmnidx.view(-1,1,1).repeat(1,shp,1).reshape(-1)
                 out=netd(srcpos,tarpos)
                 out_=out.view(dmnobs.shape[1],shp,1,250).mul(srcM[act][bs*i:bs*i+bs].view(1,shp,1,1)).sum(1).sum(1)
                 out_=out_.T
                 pred=pred+out_;del out_,out
              Preds[ep]=pred.cpu() *divr
   
   print('inversion done')
   print('Plotting  results')
   see=torch.zeros(366*295);see[srcidx]=dmn.cpu().cpu().detach() 
else:
   print('Plotting pre-saved results')
   uplft,Preds,Err,see,obstyp,dmnobs=torch.load(dir_path+'/invert/res',map_location='cpu')


_=plt.title('Comparison of uplift')
_=plt.imshow( torch.cat([see.add(SSZ.ge(0).log()).view(-1,366)[30:130,60:130], see.view(-1,366)[30:130,:5].mul(0).log(), uplft[EPS-1].add(SSZ.ge(0).log()).view(-1,366)[30:130,60:130] ] ,dim=1 ) ,origin='lower')
from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(plt.gca())
_=plt.axis('off')
cax = divider.append_axes("right", size="5%", pad=0.02)
cb=plt.colorbar(cax=cax)
_=cb.set_label('(m)')
_=plt.tight_layout()
_=plt.savefig(dir_path+'/results/Comparison of true and predicted uplit for 2011TOHOKU01AMMO using 30 offshore sensors only.pdf',bbox_inches = 'tight', dpi=200,pad_inches = 0.01);


fig, axs = plt.subplots(1, 5,figsize=(5.5,3))

for jdx,j in enumerate([1,11,21,41,60]):
    _=axs[ jdx].set_title('Iter %d'%(((j*10)//100)*10))
    v=axs[jdx].imshow(uplft[j-1].add(SSZ.ge(0).log()).view(-1,366)[30:130,60:130].cpu(),origin='lower',vmin=uplft[EPS-1].min().item(),vmax=uplft[EPS-1].max().item())
    _=axs[jdx].axis('off')

divider = make_axes_locatable(axs[-1])
cax = divider.append_axes("right", size="5%", pad=0.01)
cb=fig.colorbar(v,cax=cax)
_=cb.set_label('(m)')
_=plt.tight_layout()
_=fig.suptitle('Evolution of uplift')
_=plt.savefig(dir_path+'/results/Evolution of predicted uplit for 2011TOHOKU01AMMO using 30 offshore sensors only.pdf',bbox_inches = 'tight', dpi=200,pad_inches = 0.01);

fig, axs = plt.subplots(2, 5,figsize=(5.5,3))
obstypu=[i for i in range(153) if not i in obstyp]
for jdx,j in enumerate([1,11,21,41,60]):
    _=axs[ 0,jdx].set_title('Iter %d'%(((j*10)//100)*10))
    v=axs[0,jdx].scatter(dmnobs[:,obstyp].cpu(),Preds[j-1][:,obstyp].cpu()  ,s=1 ,rasterized=True)
    rng=[dmnobs[:,obstyp].min().item(),dmnobs[:,obstyp].max().item()]
    _=axs[0,jdx].plot( rng,rng,'--k')
    v=axs[1,jdx].scatter(dmnobs[:,obstypu].cpu(),Preds[j-1][:,obstypu].cpu()  ,s=1 ,rasterized=True)
    rng=[dmnobs[:,obstypu].min().item(),dmnobs[:,obstypu].max().item()]
    _=axs[1,jdx].plot( rng,rng,'--k')


_=fig.suptitle('Evolution of seen obs matching (top) and unseen (bottom)')


plt.tight_layout()
_=plt.savefig(dir_path+'/results/Evolution of sensor matching for 2011TOHOKU01AMMO using 30 offshore sensors only.pdf',bbox_inches = 'tight', dpi=200,pad_inches = 0.01);




byname=['N.S1N01', 'N.S1N02', 'N.S1N03', 'N.S1N04', 'N.S1N05', 'N.S1N06', 'N.S1N07', 'N.S1N08', 'N.S1N09', 'N.S1N10', 'N.S1N11', 'N.S1N12', 'N.S1N13', 'N.S1N14', 'N.S1N15', 'N.S1N16', 'N.S1N17', 'N.S1N18', 'N.S1N19', 'N.S1N20', 'N.S1N21', 'N.S1N22', 'N.S2N01', 'N.S2N02', 'N.S2N03', 'N.S2N04', 'N.S2N05', 'N.S2N06', 'N.S2N07', 'N.S2N08', 'N.S2N09', 'N.S2N10', 'N.S2N11', 'N.S2N12', 'N.S2N13A', 'N.S2N14', 'N.S2N15', 'N.S2N16', 'N.S2N17', 'N.S2N18', 'N.S2N19', 'N.S2N20', 'N.S2N21', 'N.S2N22', 'N.S2N23', 'N.S2N24', 'N.S2N25', 'N.S2N26', 'N.S3N01', 'N.S3N02', 'N.S3N03', 'N.S3N04', 'N.S3N05', 'N.S3N06', 'N.S3N07', 'N.S3N08', 'N.S3N09', 'N.S3N10', 'N.S3N11', 'N.S3N12', 'N.S3N13', 'N.S3N14', 'N.S3N15', 'N.S3N16', 'N.S3N17', 'N.S3N18', 'N.S3N19', 'N.S3N20', 'N.S3N21', 'N.S3N22', 'N.S3N23', 'N.S3N24', 'N.S3N25', 'N.S3N26', 'N.S4N01', 'N.S4N02', 'N.S4N03', 'N.S4N04', 'N.S4N05', 'N.S4N06', 'N.S4N07', 'N.S4N08', 'N.S4N09', 'N.S4N10', 'N.S4N11', 'N.S4N12', 'N.S4N13', 'N.S4N14', 'N.S4N15', 'N.S4N16', 'N.S4N17', 'N.S4N18', 'N.S4N19', 'N.S4N20', 'N.S4N21', 'N.S4N22', 'N.S4N23', 'N.S4N24', 'N.S4N25', 'N.S4N26', 'N.S4N27', 'N.S4N28', 'N.S5N01', 'N.S5N02', 'N.S5N03', 'N.S5N04', 'N.S5N05', 'N.S5N06', 'N.S5N07', 'N.S5N08', 'N.S5N09', 'N.S5N10', 'N.S5N11', 'N.S5N12', 'N.S5N13', 'N.S5N14', 'N.S5N15', 'N.S5N16', 'N.S5N17', 'N.S5N18', 'N.S5N19', 'N.S5N20', 'N.S5N21', 'N.S5N22', 'N.S5N23', 'N.S6N01', 'N.S6N02', 'N.S6N03', 'N.S6N04', 'N.S6N05', 'N.S6N06', 'N.S6N07', 'N.S6N08', 'N.S6N09', 'N.S6N10', 'N.S6N11', 'N.S6N12', 'N.S6N13', 'N.S6N14', 'N.S6N15', 'N.S6N16', 'N.S6N17', 'N.S6N18', 'N.S6N19', 'N.S6N20', 'N.S6N21', 'N.S6N22', 'N.S6N23', 'N.S6N24', 'N.S6N25', '28401', '21418', '21419']

kidx=0

fig, axs = plt.subplots(2, 4,figsize=(5,4),sharey='row') 
seen=obstyp
unseen=torch.tensor(obstypu)
seen=seen[torch.randperm(seen.shape[0])]
unseen=unseen[torch.randperm(unseen.shape[0])]
for sndx in range(2): 
   for jdx,j in enumerate([seen[:axs.shape[1]],unseen[:axs.shape[1]]][sndx]):
      _=axs[sndx,jdx].plot(SST[:250].div(60).cpu(),dmnobs[:,j].cpu() )
      _=axs[sndx,jdx].plot(SST[:250].div(60).cpu(),Preds[EPS-1][:,j].cpu())
      _=axs[sndx, jdx].set_title(byname[j]) 
      _=axs[sndx, jdx].grid()

for ax in axs.flat:  _=ax.set(xlabel='Time (min)', ylabel='Wave (m)')
for ax in axs.flat: ax.label_outer()
fig.suptitle('Match for seen (top) and unseen (bottom) sensors')
plt.tight_layout();
_=plt.savefig(dir_path+'/results/Example of network predict sensor waveforms for inverting 2011TOHOKU01AMMO using 30 offshore sensors only.pdf',bbox_inches = 'tight', dpi=200,pad_inches = 0.01);


print('Showing results')
_=plt.show()
print('Demo is completed successfully')            
