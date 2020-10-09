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

Inside folder `output_images` you can find different folders containing images from the various steps of the project:

- confront_undistorted : contains the comparison between the chessboard images before and after camera undistortion
- output_detectObjpImgp : contains the chessboard images with the calibration's image points
- output_undistorted : contains the chessboard images undistorted
- test_binary_threshold : contains the test images after applying threshold 
- test_bird_eye_view : contains the test images after applying a perspective transform
- test_final_output : contains the test images after applying all the pipeline
- test_sliding_window : contains the test images after applying lane line identification
- test_undistorted : contains the test images undistorted
- test_undistorted_confront : ontains the comparison between the test images before and after camera undistortion

[//]: # (Image References)

[calibration_original]: ./writeup/calibration_original.jpg "Original"
[calibration_undistorted]: ./writeup/calibration_undistorted.jpg "Undistorted"
[road_original]: ./writeup/road_original.jpg "Road Original"
[road_undistorted]: ./writeup/road_undistorted.jpg "Road Undistorted"
[threshold_original]: ./writeup/binary_combo_original.jpg "Original"
[threshold_binary]: ./writeup/binary_combo_example.jpg "Binary Example"
[warped]: ./writeup/warped_straight_lines.jpg "Warp Example"
[sliding_window]: ./writeup/color_fit_lines.jpg "Fit Visual"
[radius_curvature]: ./writeup/radius_of_curvature.png "Radius of curvature generic"
[poly]: ./writeup/polynomial.png "Polynomial"
[radius_curvature_applied]: ./writeup/radius_of_curvature_applied.png "Radius of curvature applied"
[final_output]: ./writeup/final_output.jpg "Final output"

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

Class `Thresholds` (defined in `Thresholds.py`) is responsible to apply color transforms, gradients and other methods to create a thresholded binary image.

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

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial.

Class `Lanes` defined in `Lanes.py` is the class implemented to find the lane-line pixels and fit their positions with a polynomial. It is divided in the following steps:

1. take the histogram of thresholded and warped image: in order to decide explicitly which pixels are part of the lines and which belong to the left line and which belong to the right line, I took the histogram of where the binary activations from the thresholded and warped image occur
2. sliding window: in the histogram from the previous step, we can see that there are two most prominent peaks; we can use that as a starting point for where to search for the lines, by using a sliding window, placed around the line centers, in order to find and follow the lines up to the top of the frame
3. fit a polynomial: after we found all pixels belonging to each line through the sliding window method, we can use them to fit a polynomial

These three steps are implemented in function `find_lane_pixels`, defined from line #42 to line #114 of `Lanes.py`.

Furthermore, in order to speed up the process of finding lane lines in each frame, I implemented a search that uses the lane found in the previous frame to search for the new lane line position. This search can be found in function `search_around_poly`, defined from line #133 to line #156 of `Lanes.py`.

Function `findLanes` defined at line #30 in `Lanes.py` is a function that, when called the first time, calls `find_lane_pixels`, while it calls `search_around_poly` all the other times.

Here's an example of the procedure described:

![alt text][sliding_window]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

Both radius of curvature and vehicle position are calculated in class `Lanes`, which can be found in file `Lanes.py` (specifically, from line #158 to line #173).

The radius of curvature at any point x of a function x = f(x) is given by :

![alt text][radius_curvature]

but considering that we have a polynomial of type

![alt text][poly]

we get that the radius of curvature is given by:

![alt text][radius_curvature_applied]

The lane curvature is calculated closest to the vehicle, so the formula is evaluated at the y value corresponding to the bottom of the image. In order to calculate the radius of curvature in the real world (and not in pixel world), y value is multiplied for a factor defined in `Lanes.py` at line #18.

To find the vehicle position on the center, the following steps where taken:
- Evaluate the left and right polynomials closest to the vehicle (same y as radius before)
- Find the middle point
- Take the difference with the center of the car (middle of the image) and transform in real world coordinate, by multiplying for a factor define in `Lanes.py` at line #19

The sign between the distance between the lane center and the vehicle center gives if the vehicle is on to the left or the right.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in cell 4 of IPython notebook `Project.ipynb`, in the function `draw_lines_on_road`. I also drew the distance and the curvature on the image by using function `draw_overlay` defined in cell 5.

![alt text][final_output]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

- The `Thresholds`'s class could be improved, by exploring some color transforms and combination more robust to light changes
- The perspective transform defined in `BirdEyeView_Transform`'s class could be improved: in the image above, the lines are not perfectly parallel. With some different transform I could've achieved a better result
- Lane finding defined in `Lane`'s class could be improved by introducing a sanity check, in order to see if the detection makes sense and maybe reset the search if it doesn't, and a smoothing, so as to achieve an output less wobbly
- Find a way to address the case in which one of the two lines is not in the image (harder_challenge_video.mp4 has a case like this near the end of the video). Could be a case where the missing line is artificially placed at default distance during calculation.
