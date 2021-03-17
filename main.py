#!/usr/bin/env python


# Python 2/3 compatibility
from __future__ import print_function
import scipy.io as sio
import numpy as np
import cv2 as cv
import os
from IRtrack.IRtrack import (FrameSequence, normFrame, nanMask, adjustContrast, fixDeadPixels)
#import video
from matplotlib import pyplot as plt



def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    cv.polylines(vis, lines, 0, (0, 255, 0))
    for (x1, y1), (_x2, _y2) in lines:
        cv.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis


def draw_hsv(flow):
    h, w = flow.shape[:2]
    fx, fy = flow[:,:,0], flow[:,:,1]
    ang = np.arctan2(fy, fx) + np.pi
    v = np.sqrt(fx*fx+fy*fy)
    hsv = np.zeros((h, w, 3), np.uint8)
    hsv[...,0] = ang*(180/np.pi/2)
    hsv[...,1] = 255
    hsv[...,2] = np.minimum(v*4, 255)
    bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    return bgr


def warp_flow(img, flow):
    h, w = flow.shape[:2]
    # flow = -flow
    flow[:,:,0] += np.arange(w)
    flow[:,:,1] += np.arange(h)[:,np.newaxis]
    res = cv.remap(img, flow, None, cv.INTER_LINEAR)
    return res

if __name__ == '__main__':
    import sys
    print(__doc__)
    try:
        fn = sys.argv[1]
    except IndexError:
        fn = 0

    fileDir = r"/ThermalImaging/Data"
    if len(sys.argv) > 1:
        subject = int(sys.argv[1])
    else:
        subject = 6     # Here you can specify which subject to run.
    A = sys.argv
    fps = 5
    image_dir = fileDir + '/L%02d' % subject + '/IRI_for_stimuli'
    frames = FrameSequence(image_dir, fps)
    initialFrame_index = 0
    initialFrame = fixDeadPixels(frames[initialFrame_index])
    frame_ix = 0
    extract_row = range(106, 604)  # Used to cut the background/boundary area of the image. This can improve the motion correction performance.
    extract_col = range(2, 475)
    initialFrame = initialFrame[extract_row]
    initialFrame = initialFrame[:, extract_col]
    normed_initialFrame = normFrame(initialFrame)
    normed_initialFrame = adjustContrast(normed_initialFrame, clipLimit=2.0, tileGridSize=(8, 8))

    fh, fw = initialFrame.shape
    oldFlow = np.zeros((fh, fw), dtype=np.float32)

    resultDir = r"/ThermalImaging/TBC/corrected_by_newMethod"
    correctedResultDir = resultDir + '/L%02d' % subject + '/correctedFace_gaussianSmoothed'
    # flowResultDir = resultDir + '/L%02d' % subject + '/flowResult_gaussianSmoothed_new'
    os.mkdir(correctedResultDir)
    # os.mkdir(flowResultDir)
    for f in frames[0:]:
        newFrame = f
        newFrame = fixDeadPixels(newFrame)
        newFrame = newFrame[extract_row]
        newFrame = newFrame[:, extract_col]
        Q = 0
        frame_ix += 1
        while True:
            cur_glitch = newFrame.copy()
            normed_newFrame = normFrame(newFrame)
            normed_newFrame = adjustContrast(normed_newFrame, clipLimit=2.0, tileGridSize=(8, 8))
            df = cv.optflow.createOptFlow_DeepFlow()
            flow1 = df.calc(normed_initialFrame, normed_newFrame, oldFlow)
            # vis = draw_hsv(flow1)
            # kernel = np.ones((45, 45), np.float32) / 2025
            # flow1_blurred = cv.filter2D(flow1, -1, kernel)
            flow1_blurred = cv.GaussianBlur(flow1, (145, 145), 45)
            flow1_blurred_copy = flow1_blurred.copy()
            # bgr = draw_hsv(flow1_blurred)
            cur_glitch = warp_flow(cur_glitch, flow1_blurred)
            row, col = np.where(cur_glitch <= 297)
            cur_glitch[row, col] = initialFrame[row, col]
            newFrame = cur_glitch
            Q += 1
            # bgr = draw_hsv(flow1_blurred_copy)
            # cv.imwrite(os.path.join(flowResultDir, '%04d' % frame_ix + '_' + '%03d' % Q + '.jpg'), bgr)
            if np.max(np.abs(flow1_blurred_copy)) < 1 or Q == 100:
                break
        # directionDir = newdir + '/%04d' % frame_ix + '.jpg'
        # cv.imwrite(directionDir, vis)
        sio.savemat(os.path.join(correctedResultDir, '%04d' % frame_ix + '.mat'), {'correctedFace': cur_glitch}
                    , do_compression=True)
        print(frame_ix)