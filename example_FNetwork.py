
print('Importng modules')
import torch
import matplotlib.pyplot as plt
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
device='cpu'
 


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
            for pm in self.parameters(): pm.requires_grad=False
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
            return out*mag
 


print('Instantiate networks')
ptopo=ptopo2=None
netp =F(numseq=2,lyr=3,freq=20 ,dim=100,diffe=False,ptopo=ptopo,ptopo2=ptopo2).to(device)  #pos net
ptopo=netp.Topo
ptopo2=netp.Topo2
netd =F(numseq=2,lyr=3,freq=20 ,dim=100,diffe=True,ptopo=ptopo,ptopo2=ptopo2).to(device)  #diff+pos net
print('Load pretrained weights')
d= torch.load(dir_path+'/Japan_GF_network/trainedNet')
netp.load_state_dict( d['pos'] )
netd.load_state_dict( d['diff'] )

srcpos,tarpos,wave=list( torch.load(dir_path+'/Japan_GF_network/sampleTestData').values())


print('Evaluating networks')
out=netd(srcpos,tarpos)
out2=netp(srcpos,tarpos)
fig, ax = plt.subplots(nrows=3, ncols=3,figsize=(8,8)) 

rnd=torch.randperm(wave.abs().max(-1).values.gt(0.01).sum())

print('Plotting results')
for paramidx in range(9):#toviewresults
    row=paramidx//3
    col=paramidx-row*3
    _=ax[row][col].plot(SST[:250]/60, wave[wave.abs().max(-1).values.gt(0.01)][rnd][paramidx] ,label='COMCOT')
    _=ax[row][col].plot(SST[:250]/60, out2[wave.abs().max(-1).values.gt(0.01)][rnd][paramidx] ,label='Pos Net')
    _=ax[row][col].plot(SST[:250]/60, out[wave.abs().max(-1).values.gt(0.01)][rnd][paramidx] ,label='Pos+diff Net')
    _=ax[row][col].set_xlabel( 'Time (min)');_=ax[row][col].set_xlim(0)
    _=ax[row][col].set_ylabel('wave (m)')
    _=ax[row][col].legend() if paramidx==0 else False
    _=ax[row][col].grid()

_=fig.suptitle('Example random samples test waveform  mag>0.01')
_=plt.tight_layout()
_=plt.savefig(dir_path+'/results/F network comparing pos and pos_diff example wave.pdf',bbox_inches = 'tight', dpi=200,pad_inches = 0.01);

plt.figure()
_=plt.scatter(wave,out2,s=2,label='Position only',rasterized=True);plt.scatter(wave,out,s=2,alpha=.8,label='Position+difference',rasterized=True);
rng=[wave.min().item(),wave.max().item()]
_=plt.plot(rng,rng,'--k')
_=plt.xlabel('True wave value (m)')
_=plt.ylabel('Predicted wave value (m)')
_=plt.legend()
_=plt.grid()
_=plt.title('The TEST set performance of networks using \n source-target (ST) positions only, and ST+their difference (S-T)')
print('Showing results')
_=plt.savefig(dir_path+'/results/F network comparing pos and pos_diff overall.pdf',bbox_inches = 'tight', dpi=200,pad_inches = 0.01);
_=plt.show()
print('Demo is completed successfully')


