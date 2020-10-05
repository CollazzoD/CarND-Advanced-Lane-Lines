import cv2
import numpy as np
import glob

class Camera:
    def __init__(self, chessboard_x = 9, chessboard_y = 6):   
        self._chessboard_x = chessboard_x
        self._chessboard_y = chessboard_y
        self._objpoints = []
        self._imgpoints = []
        self._detectObjpImgp_folder_debug = 'output_debug/output_detectObjpImgp'
        try:
            self._camera_image_folder = 'camera_cal'
            self._camera_images = glob.glob(self._camera_image_folder + '/*.jpg')
        except Exception as e:
            e.message += ' Calibration Init Error'
            raise

    # This function creates the object points and detect the imagepoints
    # on the chessboard images for calibration
    def _detectObjpImgp(self, debug=False):
        objp = np.zeros((self._chessboard_y*self._chessboard_x, 3), np.float32)
        objp[:, :2] = np.mgrid[0:self._chessboard_x, 0:self._chessboard_y].T.reshape(-1, 2)
        for fname in self._camera_images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, (self._chessboard_x, self._chessboard_y), None)
            if ret:
                self._imgpoints.append(corners)
                self._objpoints.append(objp)
                if debug:
                    img = cv2.drawChessboardCorners(img, (self._chessboard_x, self._chessboard_y), corners, ret)
                    outfname = fname.replace(self._camera_image_folder, self._detectObjpImgp_folder_debug)
                    cv2.imwrite(outfname, img)
                    print(fname + " Gray shape ", gray.shape)
                    print(fname + " Image shape ", img.shape)
        self._shape = gray.shape[::-1]
        
    def calibrate(self, debug=False):
        self._detectObjpImgp(debug)
        self._ret, self._mtx, self._dist, self._rvecs, self._tvecs = cv2.calibrateCamera(self._objpoints, self._imgpoints, self._shape, None, None)
        
    def undistort(self, img):
        return cv2.undistort(img, self._mtx, self._dist, None, self._mtx)