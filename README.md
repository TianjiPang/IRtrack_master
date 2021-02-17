# IRtrack_master

Motion correction for faces in infra-red imagery.


This code is the official python implementation of the thermal facial motion correction method used in our paper: Data-driven analysis of facial thermal responses to an emotional movie reveals consistent stimulus-locked physiological changes. Please refer to our paper for more technical details.


The method is based on the DeepFlow method[1][2].

[1] [DeepFlow: Large displacement optical flow with deep matching](https://hal.inria.fr/hal-00873592)

[2] [DeepMatching: Hierarchical Deformable Dense Matching](https://hal.inria.fr/hal-01148432)

## Setup

To run this script, you will need to install Python first.

The ```requirements.txt ```file should list all Python libraries that your notebooks depend on, and they will be installed using:

```
pip install -r requirements.txt
```

## Acknowledgement
If this code is helpful to your research, please consider citing our paper by:
```
@inproceedings{,
    title={Data-driven analysis of facial thermal responses to an emotional movie reveals consistent stimulus-locked physiological changes},
    author={Saurabh Sonkusare, Michael Breakspear, Tianji Pang, Vinh Thai Nguyen, Sascha Frydman, Christine Cong Guo, Matthew J. Aburn},
    year={2021},
    booktitle = {}
}
```
