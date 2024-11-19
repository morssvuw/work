
print('Importng modules')
import torch
import matplotlib.pyplot as plt
import os
dir_path = os.path.dirname(os.path.realpath(__file__))






import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-device', type=str , default=None,help='What device to use')
parser.add_argument('-bs', type=int, default=1000,help='batch size for training')
parser.add_argument('-ep', type=int, default=5,help='number of training epochs')
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

bs=args.bs
ep=args.ep
   
 


SSX,SSY,SSZ,SST=torch.load(dir_path+'/COMCOT/domainParameters') 
SSX=SSX.view(1,-1).repeat(295,1).reshape(-1);SSY=SSY.view(-1,1).repeat(1,366).reshape(-1);
SSX=SSX.sub(SSX.min()).div(SSX.max().sub(SSX.min())).sub(.5).mul(2).to(device)
SSY=SSY.sub(SSY.min()).div(SSY.max().sub(SSY.min())).sub(.5).mul(2).to(device)
def pad(x,diffx,diffy):#pad bathymetry data 
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
    class F(torch.nn.Module):#cross attention 
        #dim is size , numseq is number of zeros to fill 
        def __init__(self,numseq=2,lyr=3,freq=20 ,dim=100,diffe=True,ptopo=None,ptopo2=None):#
            super(F, self).__init__()
            #inputFn=torch.nn.Linear 
            self.freq=freq
            self.dim=dim
            self.pos=Seq(L(freq*4,int(dim*1.5)),A(),L(int(dim*1.5),dim))#takes pos
            self.topo=Seq(L(400,int(dim*1.5)),A(),L(int(dim*1.5),dim))#takes topo res
            self.topo2=Seq(L(400,int(dim*1.5)),A(),L(int(dim*1.5),dim))#takes topo res2
            self.diff=Seq(L(freq*4,int(dim*1.5)),A(),L(int(dim*1.5),dim))#takes difference signals 
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
        def sine(self,x):
            freq=self.freq
            x= x.mul(2**torch.arange(0,freq).view(1,-1).to(x.device))
            return torch.cat([x.sin(),x.cos()],dim=1)
        def extract_(self,topo,pos):#get topo cntered patches around given point
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
            seq=torch.cat([srcp,tarp,srct,tart,srct2,tart2,diffo,self.op.to(device).repeat(srcp.shape[0],1,1)],dim=1)#self.op.to(device).repeat(src.shape[0],1,1) 
            pos=self.sinemb(self.Emb.to(srcp.device))
            ze=seq+pos 
            return ze
        def decode(self,z,mask):#z is batch seq dim  mask is old argument in earlier experiments we no longer need it
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
                #et=et+z.square().sum()
            return  z[:,-self.numseq:]
        def forward(self,srcpos,tarpos): 
            z=self.encode(srcpos,tarpos,paddedSSZ,lowrespadded,SSX,SSY)
            final =self.decode(z,None)
            out=self.out(final[:,:-1]).view(final.shape[0],-1)
            mag=self.mag(final[:,-1:]).view(final.shape[0],-1)
            return out,mag
 


print('Instantiate networks')
ptopo=ptopo2=None
nets=[F(numseq=2,lyr=3,freq=20 ,dim=100,diffe=False,ptopo=ptopo,ptopo2=ptopo2).to(device)]
ptopo=nets[0].Topo
ptopo2=nets[0].Topo2
nets.append(  F(numseq=2,lyr=3,freq=20 ,dim=100,diffe=True,ptopo=ptopo,ptopo2=ptopo2).to(device) )

print('preparing training')
names=['Pos','Pos+diff']
opts=[torch.optim.Adam( i.parameters(),lr=1e-3) for i in nets]

def getnorm(x):#normalise wave
   mx=x.abs().max(-1).values.view(-1,1);
   x=x.div(mx.add(mx.eq(0)))
   return x,mx




def corfun(x,y): return  torch.corrcoef(  torch.cat(   [ x.reshape(1,-1).float().detach().cpu(),  y.float().detach().reshape(1,-1).cpu()  ]   )      )[0,1].cpu()


print('Checking train data')
if 'train_data' in os.listdir(dir_path+'/train/'):
   print('Found file loading') 
   srcpos,tarpos,wave=list( torch.load(dir_path+'/train/train_data',map_location='cpu').values())
else:#not found
   print('Data file not found creating artificial data for demo')
   srcpos=torch.randperm(366*295)[:1000].reshape(-1,1).repeat(1,1000).reshape(-1).to(device)
   tarpos=torch.randperm(366*295)[:1000].reshape(1,-1).repeat(1000,1).reshape(-1).to(device)
   freq=SSX[srcpos].abs()*.3
   dist=SSX[srcpos].sub(SSX[tarpos]).square().add(SSY[srcpos].sub(SSY[tarpos]).square()).sqrt()/(8**.5)#distance
   onset=dist*220
   dist=dist.div(-.25).exp()*2
   wave=torch.arange(250).view(1,-1).to(device).mul(freq.view(-1,1)).sin()
   wave=wave*(torch.arange(250).view(1,-1).to(device)>onset.view(-1,1))
   wave=wave*dist.view(-1,1);del dist,onset,freq
   rnd=torch.randperm(wave.shape[0])
   wave=wave[rnd]
   srcpos=srcpos[rnd]
   tarpos=tarpos[rnd]
   
print('Training')
Corr=[[0],[0]]
Err=[[],[]]
cntr=(wave.shape[0]//bs)+1

for e in range(ep):
   corr=[[],[]]
   err=[[],[]]
   for i in range(cntr):
      sp=srcpos[i*bs:i*bs+bs].to(device)
      if sp.shape[0]==0:
         continue
      tp=tarpos[i*bs:i*bs+bs].to(device)
      wv=wave[i*bs:i*bs+bs].to(device)
      wvn,mag=getnorm(wv)
      for n,net in enumerate(nets):
         out,magout=net(sp,tp)
         error=out.sub(wvn).abs().mean()+magout.sub(mag).square().mean()
         error.backward()
         opts[n].step();opts[n].zero_grad();
         metric=corfun(out,wvn)
         metric=0 if torch.isnan(metric)==True else metric
         corr[n].append(metric.item())
         err[n].append(error.item())
         _=print('Epoch %d, Iteration %d/%d, %s net, this_Epoch_corr=%.2f , prev_Epoch_corr=%.2f'%(e,i+1,cntr,names[n],sum(corr[n])/len(corr[n]), sum(Corr[n])/len(Corr[n]) )) if i%100==0 else ''
   for n in range(len(nets)):
      Corr[n].append(sum(corr[n])/len(corr[n]))
      Err[n].append(sum(err[n])/len(err[n]))
         


print('Plotting results')
_=[plt.plot(Corr[n],label=names[n]) for n in range(len(nets))]
_=plt.xlabel('Epoch')
_=plt.ylabel('Correlation with training data')
_=plt.legend()
_=plt.grid()
_=plt.title('Correlation with training data against epochs')
_=plt.figure()
_=[plt.plot(Err[n],label=names[n]) for n in range(len(nets))]
_=plt.xlabel('Epoch')
_=plt.ylabel('Error')
_=plt.legend()
_=plt.grid()
_=plt.title('Error with training data against epochs')
_=plt.show()
print('Demo is completed successfully')


