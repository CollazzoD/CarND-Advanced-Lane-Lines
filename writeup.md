## Project's writeup

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[calibration_original]: ./writeup/calibration_original.jpg "Original"
[calibration_undistorted]: ./writeup/calibration_undistorted.jpg "Undistorted"
[road_original]: ./writeup/road_original.jpg "Road Original"
[road_undistorted]: ./writeup/road_undistorted.jpg "Road Undistorted"
[threshold_original]: ./writeup/binary_combo_original.jpg "Original"
[threshold_binary]: ./writeup/binary_combo_example.jpg "Binary Example"
[warped]: ./writeup/warped_straight_lines.jpg "Warp Example"
[image5]: ./examples/color_fit_lines.jpg "Fit Visual"
[image6]: ./examples/example_output.jpg "Output"
[video1]: ./project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

In order to undistort the images, first we need the camera calibration matrix and distortion coefficient. These are found by taking pictures of a chessboard (in our case a 9x6 chessboard) and then applying the function `cv2.calibrateCamera`. 
The chessboard images can be found in the folder `camera_cal`. 
Note that some images are not perfect, and the chessboard is 'cut', thus the function `cv2.findChessboardCorners` cannot find all the corners. All the code that calibrates the camera, and also the function that undistort the image, can be found in the Python class `Camera` (defined in file `Camera.py`)

Original                           |  Undistorted
:---------------------------------:|:---------------------------------:
![alt text][calibration_original]  |  ![alt text][calibration_undistorted]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

To undistort an image simply call the `undistort` function (defined in file `Camera.py`) on the image itself. The result is the following:

Original                           |  Undistorted
:---------------------------------:|:---------------------------------:
![alt text][road_original]  |  ![alt text][road_undistorted]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

Class `Thresholds` (defined in `Thresholds.py`) is responsible to apply color transforms, gradients and other methods to crete a thresholded binary image.

The combination is defined at line #101 of `Thresholds.py`, inside `combine` function.
Here's an example of my output for this step:

Original                           |  Thresholded
:---------------------------------:|:---------------------------------:
![alt text][threshold_original]  |  ![alt text][threshold_binary]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

My perspective transform is implemented in class `BirdEyeView_Transform` (inside `BirdEyeView_Transform.py`). It includes a function called `warp`, which appears in lines 33 through 36 in the file.  The `warp` function takes as inputs an image (`image`) and applies the perspective transform.

I chose to hardcode the source and destination points as class parameters, defined inside the `__init__` function. The points are:

|Point          | Source        | Destination   | 
|:-------------:|:-------------:|:-------------:| 
|Left bottom    | 150, 720      | 320, 720      | 
|Right bottom   | 1250, 720     | 960, 720      |
|Left up        | 590, 450      | 320, 0        |
|Right up       | 700, 450      | 960, 0        |

I tried to apply the `warp` function on a test image with straight lines and I was satisfacted with the result (even though I think it can be improved)

![alt text][warped]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Then I did some other stuff and fit my lane lines with a 2nd order polynomial kinda like this:

![alt text][image5]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I did this in lines # through # in my code in `my_other_file.py`

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in lines # through # in my code in `yet_another_file.py` in the function `map_lane()`.  Here is an example of my result on a test image:

![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  
