import cv2
import numpy as np


class BirdEyeView_Transform:
    def __init__(self):
        SRC_LEFT_BOTTOM = (150, 720)
        SRC_RIGHT_BOTTOM = (1250, 720)
        SRC_LEFT_UP = (590, 450)
        SRC_RIGHT_UP = (700, 450)
        
        DST_LEFT_BOTTOM = (320, 720)
        DST_RIGHT_BOTTOM = (960, 720)
        DST_LEFT_UP = (320, 0)
        DST_RIGHT_UP = (960, 0)    
        
        self._src = np.array([[SRC_LEFT_BOTTOM , SRC_LEFT_UP, SRC_RIGHT_UP, SRC_RIGHT_BOTTOM]], dtype=np.float32)
        self._dst = np.array([[DST_LEFT_BOTTOM , DST_LEFT_UP, DST_RIGHT_UP, DST_RIGHT_BOTTOM]], dtype=np.float32)
        self._M = cv2.getPerspectiveTransform(self._src, self._dst)
        self._Minv = cv2.getPerspectiveTransform(self._dst, self._src)
        
    def roi(self, image):
        mask = np.zeros_like(image)
        ignore_mask_color = 255

        #filling pixels inside the polygon defined by \"vertices\" with the fill color
        cv2.fillPoly(mask, np.int32(self._src), ignore_mask_color)

        #returning the image only where mask pixels are nonzero
        masked_image = cv2.bitwise_and(image, mask)
        return masked_image

    def warp(self, image):
        y = image.shape[0]
        x = image.shape[1]
        return cv2.warpPerspective(image, self._M, (x, y), flags=cv2.INTER_LINEAR)
                             
    def unwarp(self, image):
        y = image.shape[0]
        x = image.shape[1]
        return cv2.warpPerspective(image, self._Minv, (x, y), flags=cv2.INTER_LINEAR)