import torch
import matplotlib.pyplot as plt
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
device='cpu'
#CODE NOT TESTED FOR DEVICE MAY PRODUCE ERRORS WITH GPU

#longitude and latitude for toy set
MyPosx_=torch.arange(130,130+0.075*51,0.075).view(-1,1).repeat(52,1).view(-1,1).to(device);MyPosy_=torch.arange(30,30+0.075*51,0.075).view(-1,1).repeat(1,51).view(-1,1).to(device);

#define layers
A=torch.nn.LeakyReLU;
S=torch.nn.Sequential
L=torch.nn.Linear
C=torch.nn.Conv1d
CT=torch.nn.ConvTranspose1d   
#functions for features
def getFeaturesnew(src,tar,freqs,offon):#gt source target features for all possibilities
    a,b,c,d=sin(abspos(src,tar,freqs) ),sin(diffxy(src,tar,freqs)), sin(distance(src,tar,freqs)) ,sin(tar2srcang(src,tar,freqs)) 
    return torch.cat([  a,b,c,d ] ,dim=-1)

def sin(x): return torch.cat([  x.sin(),x.cos()],dim=-1)#input freq multiplied embedding returns sin and cos of it

def distance(src,tar,freqs,oned=False):#get distance betwween souce and target, and multiplies by freq 
    src=src.view(-1)
    a=MyPosx_[src].sub(MyPosx_.view(1,-1)).mul(torch.pi/360).sin().square()
    a=a.mul(MyPosy_[src].mul(torch.pi/180).cos()).mul(MyPosy_.view(1,-1).mul(torch.pi/180).cos())
    a=a.add(MyPosy_[src].sub(MyPosy_.view(1,-1)).mul(torch.pi/360).sin().square())
    a=a.sqrt().asin().view(-1,52,51)#N by 2652 connvert to N by 52,51  shared with both 1d and 2d  experiments
    a=torch.cat([a[idx:idx+1,rw//51,tar[idx].view(-1)] for idx,rw in enumerate(src)]) if oned==True else torch.cat([a.view(-1,52*51)[idx:idx+1,tar[idx].view(-1)] for idx,rw in enumerate(src)])#For 1d keep only pixels in same row
    return a.mul(  freqs.view(1,-1 ).to(a.device)  )#

def diffxy(src,tar,freqs,oned=False):#gets difference in x and y 
    src=src.view(-1)
    a=torch.cat([  MyPosx_[src].sub(MyPosx_.view(1,-1)).mul(torch.pi/180).view(-1,52,51,1), MyPosy_[src].sub(MyPosy_.view(1,-1)).mul(torch.pi/180).view(-1,52,51,1) ],dim=-1)
    a=torch.cat([a[idx:idx+1,rw//51,tar[idx].view(-1)] for idx,rw in enumerate(src)]).view(-1,2)  if oned==True else torch.cat([a.view(-1,52*51,2)[idx:idx+1,tar[idx].view(-1)] for idx,rw in enumerate(src)]).view(-1,2)#
    return torch.cat([  a[:,:1].mul(  freqs.view(1,-1 ).to(a.device)  ),  a[:,1:2].mul(  freqs.view(1,-1 ).to(a.device)  )],dim=-1)#

def abspos(src,tar,freqs,oned=False):#gets src tar pos in x and y 
    src=src.view(-1)
    a_=torch.cat([  MyPosx_[src].view(-1,1).mul(torch.pi/180), MyPosy_[src].view(-1,1).mul(torch.pi/180) ],dim=-1).view(-1,2)#N by xy source
    a=torch.cat([  MyPosx_.view(-1,52,51,1).mul(torch.pi/180), MyPosy_.view(-1,52,51,1).mul(torch.pi/180) ],dim=-1).repeat(src.shape[0],1,1,1)
    a=torch.cat([a[idx:idx+1,rw//51,tar[idx].view(-1)] for idx,rw in enumerate(src)]).view(-1,2) if oned==True else torch.cat([a.view(-1,52*51,2)[idx:idx+1,tar[idx].view(-1)] for idx,rw in enumerate(src)]).view(-1,2)
    a=torch.cat([a_,a],dim=1) 
    return torch.cat([a[:,i:i+1].mul(  freqs.view(1,-1 ).to(a.device)  ) for i in range(a.shape[1])],dim=-1)#N by 1 now convert to N by FreqX2 first source x  increasing freq then y then target x and y 

def tar2srcang(src,tar,freqs,oned=False):#bearing from source to target 
    src=src.view(-1)
    a=MyPosy_.view(1,-1).mul(torch.pi/180).cos().mul( MyPosx_[src].sub(MyPosx_.view(1,-1)).mul(torch.pi/180).sin() )
    b=MyPosy_.view(1,-1).mul(torch.pi/180).sin().mul(  MyPosy_[src].view(-1,1).mul(torch.pi/180).cos()  )
    b=b.sub( MyPosy_.view(1,-1).mul(torch.pi/180).cos().mul( MyPosx_[src].sub(MyPosx_.view(1,-1)).mul(torch.pi/180).cos() ).mul(MyPosy_[src].view(-1,1).mul(torch.pi/180).sin()) )
    a=torch.atan2(a,b).view(-1,52,51);del b
    a=torch.cat([a[idx:idx+1,rw//51,tar[idx].view(-1)] for idx,rw in enumerate(src)]).view(-1,1)  if oned==True else torch.cat([a.view(-1,52*51)[idx:idx+1,tar[idx].view(-1)] for idx,rw in enumerate(src)]).view(-1,1)
    return a.mul(  freqs.view(1,-1 ).to(a.device)  )  


 

#define network
print('Initialise networks')
class N(torch.nn.Module):#DONE 
    def __init__(self,device): 
        super(N, self).__init__();
        self.z=S(L(100+10,500),A(),L(500,200),A(),L(200,1));
        self.pos=torch.arange(51).view(1,-1,1).div(50).sub(0.5).mul(2).mul(2**torch.arange(5));
        self.pos=torch.cat([self.pos.sin(),self.pos.cos()],dim=-1); 
    
    def forward(self,x): 
        dev=x.device
        return self.z(  torch.cat([x.repeat(1,51,1),self.pos.to(dev).repeat(x.shape[0],1,1)],dim=-1)).view(-1,1,51)

  

nets=[]
for i in range(2): nets.append(   S(L(160+20*0,100),A(0.01),L(100,100),A(0.01), L(100,100),N(device)).to(device) )

print('Load pretrained weights')
nets[0].load_state_dict(torch.load(dir_path+'/Toy_GF_network/trainedNet')[0]['dict'])
nets[1].load_state_dict(torch.load(dir_path+'/Toy_GF_network/trainedNet')[1]['dict'])

print("Load 50,000 random Green's functions from TEST data (not training)")


srcp,tarp,wve=torch.load(dir_path+'/Toy_GF_network/testData')
print('Calculate embeddings')
emb=getFeaturesnew(srcp,tarp,2**torch.arange(0,20,2),None)
print('Evaluate networks')
with torch.no_grad():
    pos=nets[0](emb.mul(torch.load(dir_path+'/Toy_GF_network/trainedNet')[0]['mask']).unsqueeze(1)).view(-1,51)
    diff=nets[1](emb.mul(torch.load(dir_path+'/Toy_GF_network/trainedNet')[1]['mask']).unsqueeze(1)).view(-1,51)
    print('Plot results')
    _=plt.scatter(wve.cpu()[::3],pos.cpu()[::3],s=1,label='Position only',rasterized=True)
    _=plt.scatter(wve.cpu()[::3],diff.cpu()[::3],s=1,alpha=.5,label='Position + Difference',rasterized=True)
    rng=[wve.min().item(),wve.max().item()]
    _=plt.plot(rng,rng,'--k')
    _=plt.xlabel('True wave value (m)')
    _=plt.ylabel('Predicted wave value (m)')
    _=plt.legend()
    _=plt.grid()
    _=plt.title('The performance of networks using \n source-target (ST) positions only, and ST+their difference (S-T) \n for 16,000 GF wwaveforms')
    _=plt.savefig(dir_path+'/results/Toy network results.pdf',bbox_inches = 'tight', dpi=200,pad_inches = 0.01);
    _=plt.figure()
    rnd=torch.randperm(wve.abs().sum(-1).gt(0.07).sum())
    plt.plot(torch.arange(51).mul(.6),wve[wve.abs().sum(-1).gt(0.07)][rnd[0]].cpu(),linewidth=3,label='True from COMCOT')
    plt.plot(torch.arange(51).mul(.6),pos[wve.abs().sum(-1).gt(0.07)][rnd[0]].cpu(),label='Prediction from position only network')
    plt.plot(torch.arange(51).mul(.6),diff[wve.abs().sum(-1).gt(0.07)][rnd[0]].cpu(),label='Prediction from position + difference network')
    _=plt.legend();_=plt.grid();_=plt.xlabel('Time (min)');_=plt.ylabel('Surface height (m)');_=plt.xlim(0);
    srcloc=[MyPosx_[srcp[wve.abs().sum(-1).gt(0.07)][rnd[0]]].item(),MyPosy_[srcp[wve.abs().sum(-1).gt(0.07)][rnd[0]]].item()]
    tarloc=[MyPosx_[tarp[wve.abs().sum(-1).gt(0.07)][rnd[0]]].item(),MyPosy_[tarp[wve.abs().sum(-1).gt(0.07)][rnd[0]]].item()]
    _=plt.title('Example Greens function waveform \n picked at random from the 50,000 test wwaveforms. \n source at (%.2f°,%.2f°) receiver at (%.2f°,%.2f°)'%(srcloc[0],srcloc[1],tarloc[0],tarloc[1]))
    _=plt.savefig(dir_path+'/results/Toy network waves.pdf',bbox_inches = 'tight', dpi=200,pad_inches = 0.01);
    print('Showing results')
    _=plt.show()
    print('Demo is completed successfully')
