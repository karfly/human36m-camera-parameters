# Camera parameters for Human3.6M dataset
This repository contains camera parameters (intrinsics and extrinsics) for [Human3.6M dataset](http://vision.imar.ro/human3.6m/description.php) in handy format. File `camera-parameters.json` stores all parameters extracted from `metadata.npy` (see `metadata.xml` from [official code package](http://vision.imar.ro/human3.6m/code-v1.2.zip)) using `generate.py` script.

## Camera parameters
- **R** - 3x3 rotation matrix
- **t** - 3x1 translation vector
- **calibration_matrix** - 3x3 calibration matrix
- **distortion** - 5 values [k1, k2, p1, p2, k3] (see [this OpenCV article](https://docs.opencv.org/2.4/doc/tutorials/calib3d/camera_calibration/camera_calibration.html))

## Projection (without distortion)
To build projection matrix P just multiply calibration and extrinsics matricies:
```python
P = calibration_matrix @ np.hstack([R, t])
print(P.shape)  # (3, 4)
```
To project 3D point X to image plane:
```python
X = np.random.rand(3)  # random 3D point
X_homo = np.hstack([X, 1.0])  # convert to homogenous

x_homo = P @ X_homo  # project
x = x_homo[:2] / x_homo[2]  # convert back to cartesian (check that x_homo[2] > 0)
```
