# Code
Demo code for review
---


## **Requirements**
### Code was tested on Linux using the following software and packages:
- Python version 3.10.14
- Pytorch version (with cuda) 2.1.2+cu121
- Matplotlib version 3.9.0

### Some .py files requires GPU to run at a reasonable speed memory needed is about 13GB it is tested on:
- Quadro RTX 6000 

## **examples**
### demo plotting example GFs from COMCOT
```shell
python /path/to/paper/example_comcot.py 
```
This will plot results that we obtained if no COMCOT application is found. If instead you want to run 
your own simulation (sing our configuration file) you need to provide a COMCOT exe placed in the directory /COMCOT/SOURCE/
and its filename must be COMCOT_app.

You can also set the location of initial source point by providing x and y coordinates e.g., for source (100,80)
```shell
python /path/to/paper/example_comcot.py -x 100 -y 80
```
### demo example running toy dataset networks
```shell
python /path/to/paper/example_toyNetwork.py
```
It will load pretrained models (pos only and
pos+diff nets) and some saved GFs and evaluate the networks then compare
network predictions to the GF using a scatter plot of all points. It will also randomly select
some of the higher magnitude GF waves to plot. So every time you will get a different
wave but the scatter plot is the same. The results are also saved as pdf in the
/results folder. 

### demo example running toy dataset networks
```shell
python /path/to/paper/example_FNetwork.py
```
Runs an example for real data Japan networks again comparing pos and
pos+diff networks. Results will also be saved in results folder.  It will randomly select
some of the higher magnitude GF waves to plot. So every time you will get a different
wave but the scatter plot is the same.

### demo example running inversion on real event
```shell
python /path/to/paper/example_invert.py
```
Here we use F network (pretrained weight is provided) to carry out an inversion of an
event given provided data. Results will be plotted and saved. Requires GPU takes about 2-3 min. Can run on CPU but alot slower 20-30 min.


### demo example training on artificial data
```shell
python /path/to/paper/example_train.py
```
Here we  demonstrate how to train F network as a GF model.  Training data can be provided under the /train directory, and its filename is train_data. It should be a torch.save file using pickle and default protocol. The contents are a dictionary with ordered keys src,tar,wv which are torch tensors of source grid index (flattened comuptational domain index not two dimensional), target grid point index  (flattened comuptational domain index not two dimensional), and corresponding Green's function (must be 250 points long or you can edit code to allow a different size).

If no training data is supplied, the code will invent some aritifical GFs and train on them. Obviously the artificial data is easy and training on it does not reflect the diffculity of training on real GF but serves as a demo.


