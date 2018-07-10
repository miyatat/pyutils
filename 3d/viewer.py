# -*- coding: utf-8 -*-

from logging import getLogger

import ipyvolume as ipv
from niwidgets import NiftiWidget
import numpy as np

logger = getLogger(__name__)

if __name__ == '__main__':
    ddd = np.random.random((100, 100, 100))
    ipv.quickvolshow(ddd)

    my_widget = NiftiWidget(fname)
    my_widget.nifti_plotter()


    pass
