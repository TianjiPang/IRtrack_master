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

## Quickstart

To run with default parameters, simply call

```
python main.py
````

This will by default use the first image as the reference image and do the motion correction for the rest of images sequentially.

User can specify the ID of the subject for motion correction by adding the subject ID in the end of the command. For example:

```
python main.py 6
```

will do the motion correction for the subject 6.

## Note
You should quality check the videos before performing the motion correction. Ideally, subject should face to the camera and all frames should successfully capture the full face of subject. 

By default, the code was written for the data saved in .mat format. The data input are mat file arrays corresponding to each frame of the video. User can change the data loading method according to their own data format.

To do the motion correction, user should select a reference frame and input it in the code. All the other frames will be motion corrected corresponding to this frame. The first frame of the video is set as the reference frame by default. User can change the reference frame by changing the value of the parameter 'frame_ix' in the code.

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
