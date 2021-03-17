# Copyright 2018 QIMR Berghofer Medical Research Institute
#
import os
import glob
import types
from collections import Sequence, namedtuple
import numpy as np
import scipy.io as sio
import cv2 as cv

class Error(Exception):
    pass


def normFrame(data):
    """Convert floating point temperature data to 8-bit integer with max range,
    with data stored in memory in C order, as expected by Qt and OpenCV."""
    (dmin, dmax) = (data.min(), data.max())
    frame = np.rint(255.0*(data - dmin)/(dmax - dmin)).astype(np.uint8, 'C')
    return frame


def adjustContrast(frame, clipLimit=2.0, tileGridSize=(8,8)):
    """Improve contrast by Contrast Limited Adaptive Histogram Equalization"""
    # clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    clahe = cv.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
    return clahe.apply(frame)



def fixDeadPixels(data):
    """Remove our camera's known dead pixels from an image.
    Note this is specific to our camera."""
    newdata = data.copy()
    # newdata[638,0] = data[638,1] # copy value from adjacent pixel
    # newdata[639,0] = data[639,1]
    return newdata


class FrameSequence(list):
    """List of frames from a sequence of MAT files, assuming files have
    names of the form MAT123.MAT, where the number of digits may vary. Frames
    are read in and preprocessed lazily when accessed from the list.
    """
    def __init__(self, source=None, fps=5.0):
        """Create a FrameSequence from a directory or from a list of filenames.
        Arguments:
          source (string or list): Either a list of .MAT filenames or
          the name of a directory containing the .MAT files.
          fps (float): Frame rate in frames per second.
        """
        self.fps = fps
        if source is None:
            _filelist = []
        elif isinstance(source, (str,)):
            # Source is a directory name. Sort filenames by their numbers:
            # fl = glob.glob(source + '/MAT*.MAT')
            fl = glob.glob(source + '/*.mat')
            # _filelist = sorted(fl, key=(lambda f: int(f[f.rfind('\\')+4:-4])))
            _filelist = sorted(fl, key=(lambda f: int(f[f.rfind('\\')+1:-4])))
        elif isinstance(source, Sequence) and all(
                isinstance(x, (str,)) for x in source):
            # Source is a list of filenames
            _filelist = list(source)
        else:
            raise TypeError("source should be directory or list of filenames")
        super(FrameSequence, self).__init__(_filelist)

    def __getitem__(self, index):
        res = super(FrameSequence, self).__getitem__(index)
        if type(res) is not list:
            return fixDeadPixels(frameDataFromFile(res))
        else:
            return FrameSequence(res)

    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j, None))

    def __iter__(self):
        for filename in super(FrameSequence, self).__iter__():
            yield fixDeadPixels(frameDataFromFile(filename))

    def __repr__(self):
        return super(FrameSequence, self).__repr__()




def nanMask(roiRadius):
    """An array of ones inside the ROI circle, 'nan' outside the circle"""
    mask = np.ones((2*roiRadius + 1, 2*roiRadius + 1))
    my, mx = np.mgrid[-roiRadius:(roiRadius+1), -roiRadius:(roiRadius+1)]
    mask[mx**2 + my**2 > roiRadius**2] = np.nan
    return mask
