import cv2
import numpy as np
import numpy.polynomial.polynomial as poly

class Lanes:
    def __init__(self):
        # HYPERPARAMETERS
        # Number of sliding windows
        self._NWINDOWS = 9
        # Set the width of the windows +/- margin
        self._WINDOWMARGIN = 100
        # Set minimum number of pixels found to recenter window
        self._MINPIX = 50
        
        # Width of the margin around the previous polynomial to search
        self._POLYMARGIN = 100
        
        self._YM_PER_PIX = 30/720 # meters per pixel in y dimension
        self._XM_PER_PIX = 3.7/700 # meters per pixel in x dimension
        
        self._first = True
        
        self._Y_EVAL = 719 # Evaluate Curvature at car level
        
        self._CENTER_CAR = 640 # Center of the car is approximately 640
        
        self._CURVATURE_THRESHOLD = 200

    
    def findLanes(self, image, debug=False):
        if self._first:
            self.find_lane_pixels(image, debug)
            self._first = False
        else:
            self.search_around_poly(image, debug)
    
    # Code from lessons' material
    def histogram(self, image):
        return np.sum(image[image.shape[0]//2:,:], axis=0)
    
    # Code from lessons' material
    def find_lane_pixels(self, image, debug=False):
        histogram = self.histogram(image)
        self._image_shape = image.shape
        if debug:
            # Create an output image to draw on and visualize the result
            self.out_img = np.dstack((image, image, image))
            
        # Find the peak of the left and right halves of the histogram
        # These will be the starting point for the left and right lines
        midpoint = np.int(histogram.shape[0]//2)
        leftx_base = np.argmax(histogram[:midpoint])
        rightx_base = np.argmax(histogram[midpoint:]) + midpoint

        # Set height of windows - based on nwindows above and image shape
        window_height = np.int(image.shape[0]//self._NWINDOWS)
        # Identify the x and y positions of all nonzero pixels in the image
        nonzero = image.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])
        # Current positions to be updated later for each window in nwindows
        leftx_current = leftx_base
        rightx_current = rightx_base

        # Create empty lists to receive left and right lane pixel indices
        left_lane_inds = []
        right_lane_inds = []

        # Step through the windows one by one
        for window in range(self._NWINDOWS):
            # Identify window boundaries in x and y (and right and left)
            win_y_low = image.shape[0] - (window+1)*window_height
            win_y_high = image.shape[0] - window*window_height
            # Find the four below boundaries of the window
            win_xleft_low = leftx_current - self._WINDOWMARGIN  
            win_xleft_high = leftx_current + self._WINDOWMARGIN  
            win_xright_low = rightx_current - self._WINDOWMARGIN 
            win_xright_high = rightx_current + self._WINDOWMARGIN 

            if debug:
                # Draw the windows on the visualization image
                cv2.rectangle(self.out_img,(win_xleft_low,win_y_low), (win_xleft_high,win_y_high), (0,255,0), 2) 
                cv2.rectangle(self.out_img,(win_xright_low,win_y_low), (win_xright_high,win_y_high), (0,255,0), 2) 

            # Identify the nonzero pixels in x and y within the window
            good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & 
            (nonzerox >= win_xleft_low) &  (nonzerox < win_xleft_high)).nonzero()[0]
            good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & 
            (nonzerox >= win_xright_low) &  (nonzerox < win_xright_high)).nonzero()[0]

            # Append these indices to the lists
            left_lane_inds.append(good_left_inds)
            right_lane_inds.append(good_right_inds)

            # If you found > minpix pixels, recenter next window 
            # (`right` or `leftx_current`) on their mean position 
            if len(good_left_inds) > self._MINPIX:
                leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
            if len(good_right_inds) > self._MINPIX:        
                rightx_current = np.int(np.mean(nonzerox[good_right_inds]))

        # Concatenate the arrays of indices (previously was a list of lists of pixels)
        left_lane_inds = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)
    
        self._leftx = nonzerox[left_lane_inds]
        self._lefty = nonzeroy[left_lane_inds] 
        self._rightx = nonzerox[right_lane_inds]
        self._righty = nonzeroy[right_lane_inds] 
        self.fit_poly()
        
        if debug:
            self.out_img[self._lefty, self._leftx] = [255, 0, 0]
            self.out_img[self._righty, self._rightx] = [0, 0, 255]
    
    def fit_poly(self):
        self._left_fit = np.polyfit(self._lefty, self._leftx, 2)
        self._right_fit = np.polyfit(self._righty, self._rightx, 2)
        self._left_fit_cr = np.polyfit(self._lefty*self._YM_PER_PIX, self._leftx*self._XM_PER_PIX, 2)
        self._right_fit_cr = np.polyfit(self._righty*self._YM_PER_PIX, self._rightx*self._XM_PER_PIX, 2)
    
    def get_poly_plot(self):
        # Generate x and y values for plotting
        ploty = np.linspace(0, self._image_shape[0]-1, self._image_shape[0])
        ### Calc both polynomials using ploty, left_fit and right_fit
        left_fitx = self._left_fit[0]*ploty**2 + self._left_fit[1]*ploty + self._left_fit[2]
        right_fitx = self._right_fit[0]*ploty**2 + self._right_fit[1]*ploty + self._right_fit[2]
        return left_fitx, right_fitx, ploty
    
    # Code from lessons' material
    # Second
    def search_around_poly(self, image, debug=False):
        self._image_shape = image.shape
        # Grab activated pixels
        nonzero = image.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])
        
        # Set the area of search based on activated x-values
        # within the +/- margin of our polynomial function
        left_poly = self._left_fit[0]*(nonzeroy**2) + self._left_fit[1]*nonzeroy + self._left_fit[2]
        right_poly = self._right_fit[0]*(nonzeroy**2) + self._right_fit[1]*nonzeroy + self._right_fit[2]
        left_lane_inds = ((nonzerox > (left_poly - self._POLYMARGIN)) & (nonzerox < (left_poly + self._POLYMARGIN)))
        right_lane_inds = ((nonzerox > (right_poly - self._POLYMARGIN)) & (nonzerox < (right_poly + self._POLYMARGIN)))

        # Again, extract left and right line pixel positions
        self._leftx = nonzerox[left_lane_inds]
        self._lefty = nonzeroy[left_lane_inds] 
        self._rightx = nonzerox[right_lane_inds]
        self._righty = nonzeroy[right_lane_inds] 
        self.fit_poly()
        
        if debug:
            self.out_img = np.dstack((image, image, image))*255
            self.out_img[nonzeroy[left_lane_inds], nonzerox[left_lane_inds]] = [255, 0, 0]
            self.out_img[nonzeroy[right_lane_inds], nonzerox[right_lane_inds]] = [0, 0, 255]
            
    def curvature(self):
        self._left_curverad = ((1 + (2*self._left_fit_cr[0]*self._Y_EVAL*self._YM_PER_PIX + self._left_fit_cr[1])**2)**1.5) / np.absolute(2*self._left_fit_cr[0])
        self._right_curverad = ((1 + (2*self._right_fit_cr[0]*self._Y_EVAL*self._YM_PER_PIX + self._right_fit_cr[1])**2)**1.5) / np.absolute(2*self._right_fit_cr[0])
        return (self._left_curverad + self._right_curverad)/2
    
    def car_center_distance(self):   
        left_fit = np.flip(self._left_fit,0)
        right_fit = np.flip(self._right_fit,0)
        leftl = poly.polyval(self._Y_EVAL, left_fit)
        rightl = poly.polyval(self._Y_EVAL, right_fit)

        # Midpoint Y_EVAL is center of the road
        center_road = (rightl + leftl)/2
        distance  = (self._CENTER_CAR - center_road)*self._XM_PER_PIX

        return distance