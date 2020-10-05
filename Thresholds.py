import cv2
import numpy as np

class Thresholds:
    def __init__(self):
        self._HLS_H_THRESHOLD = (100, 255)
        self._HLS_L_THRESHOLD = (100, 255)
        self._HLS_S_THRESHOLD = (100, 255)
        self._SOBEL_THRESHOLD = (20, 100)
        self._SOBEL_KERNEL = 3
        self._GRAD_MAG_THRESHOLD = (30, 170)
        self._GRAD_DIR_THRESHOLD = (1.5, np.pi/2)

    # Function that filters the H-channel of HLS with a threshold
    def hls_h_select(self, img):
        hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS) 
        h_channel = hls[:,:,0]
        binary_output = np.zeros_like(h_channel)
        binary_output[(h_channel > self._HLS_H_THRESHOLD[0]) & (h_channel <= self._HLS_H_THRESHOLD[1])] = 1
        return binary_output

    # Function that filters the L-channel of HLS with a threshold
    def hls_l_select(self, img):
        hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS) 
        l_channel = hls[:,:,1]
        binary_output = np.zeros_like(l_channel)
        binary_output[(l_channel > self._HLS_L_THRESHOLD[0]) & (l_channel <= self._HLS_L_THRESHOLD[1])] = 1
        return binary_output
        
    # Function that filters the S-channel of HLS with a threshold
    def hls_s_select(self, img):
        hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS) 
        s_channel = hls[:,:,2]
        binary_output = np.zeros_like(s_channel)
        binary_output[(s_channel > self._HLS_S_THRESHOLD[0]) & (s_channel <= self._HLS_S_THRESHOLD[1])] = 1
        return binary_output

    # Function that filters gradient's orientation with a threshold
    def abs_sobel_thresh(self, img, orient='x'):
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply x or y gradient with the OpenCV Sobel() function
        # and take the absolute value
        if orient == 'x':
            abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=self._SOBEL_KERNEL))
        if orient == 'y':
            abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=self._SOBEL_KERNEL))
        # Rescale back to 8 bit integer
        scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
        # Create a copy and apply the threshold
        binary_output = np.zeros_like(scaled_sobel)
        # Here I'm using inclusive (>=, <=) thresholds, but exclusive is ok too
        binary_output[(scaled_sobel >= self._SOBEL_THRESHOLD[0]) & (scaled_sobel <= self._SOBEL_THRESHOLD[1])] = 1

        # Return the result
        return binary_output

    # Function that filters gradient's magnitude with a threshold
    def mag_thresh(self, img):
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Take both Sobel x and y gradients
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=self._SOBEL_KERNEL)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=self._SOBEL_KERNEL)
        # Calculate the gradient magnitude
        gradmag = np.sqrt(sobelx**2 + sobely**2)
        # Rescale to 8 bit
        scale_factor = np.max(gradmag)/255
        gradmag = (gradmag/scale_factor).astype(np.uint8)
        # Create a binary image of ones where threshold is met, zeros otherwise
        binary_output = np.zeros_like(gradmag)
        binary_output[(gradmag >= self._GRAD_MAG_THRESHOLD[0]) & (gradmag <= self._GRAD_MAG_THRESHOLD[1])] = 1

        # Return the binary image
        return binary_output

    # Function that filters gradient's direction with a threshold
    def dir_threshold(self, img):
        # Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Calculate the x and y gradients
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=self._SOBEL_KERNEL)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=self._SOBEL_KERNEL)
        # Take the absolute value of the gradient direction,
        # apply a threshold, and create a binary image result
        absgraddir = np.arctan2(np.absolute(sobely), np.absolute(sobelx))
        binary_output =  np.zeros_like(absgraddir)
        binary_output[(absgraddir >= self._GRAD_DIR_THRESHOLD[0]) & (absgraddir <= self._GRAD_DIR_THRESHOLD[1])] = 1

        # Return the binary image
        return binary_output

    def combine(self, img):
        # Combine thresholding 
        gradx = self.abs_sobel_thresh(img, orient='x')
        mag_binary = self.mag_thresh(img)
        s_binary = self.hls_s_select(img)
        l_binary = self.hls_l_select(img)
        
        combined = np.zeros_like(gradx)
        combined[(gradx == 1) | ((s_binary == 1) & (l_binary == 1))] = 1
        
        return combined