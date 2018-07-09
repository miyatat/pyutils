# -*- coding: utf-8 -*-

from logging import getLogger

import ipyvolume as ipv
import numpy as np

logger = getLogger(__name__)

if __name__ == '__main__':
    ddd = np.random.random((100, 100, 100))
    ipv.quickvolshow(ddd)

    pass
