# -*- coding: utf-8 -*-
"""
==============================================================================
@author: Nikolaos Giakoumoglou
@date: Sun May 23 13:24:21 2021
==============================================================================
A.2 Multi-region Histogram
==============================================================================
Inputs:
    - f:        image of dimensions N1 x N2
    - mask:     int boolean image N1 x N2 with 1 if pixels belongs to ROI, 
                0 else
    - Ng:       number of gray levels
    - bins:     bins for histogram
    - num_eros: timers of erosion to be performed (default=3)
    - kernel:   kernel where erosion is performed: (default=+)
Outputs:
    - features: histograms of f as vector e.g. [32 x num_eros]
==============================================================================
"""

import numpy as np
from skimage import morphology
import itertools

def multiregion_histogram(f, mask, bins=32, num_eros=3, square_size = 3):

    f2 = f.astype(np.uint8)               
    mask2 = mask.astype(np.uint8)   
    kernel = morphology.square(square_size)
    level_min = 0
    level_max = 255
    features = np.zeros((num_eros,bins), np.double)
    labels = []
    for i in range(num_eros):
        f2 = morphology.erosion(f2, kernel)
        mask2 = morphology.erosion(mask2, kernel)
        f2_ravel = f2.ravel()
        mask2_ravel = mask2.ravel() 
        roi = f2_ravel[mask2_ravel.astype(bool)]
        features[i,:] = np.histogram(roi, bins=bins, range=[level_min, level_max], density=True)[0]
        labels.append(['Histogram_erosion_'+str(i+1)+'_bin_'+str(b) for b in range(bins)])
    
    labels = list(itertools.chain(*labels))
    return features.flatten(), labels
    